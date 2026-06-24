# ============================================================================
# Module: engine.py
# Purpose: Deterministic conversation orchestration for the tax filing assistant
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from __future__ import annotations

from src.conversation.guardrails import is_off_topic
from src.conversation.prompts import (
    DISCLAIMER,
    ask_confirmation,
    ask_correction,
    ask_dependency,
    ask_filing_status,
    ask_w2,
    off_topic_redirect,
)
from src.models.session import ConversationMessage, ConversationSession, ConversationState
from src.tools.generate_1040 import generate_1040
from src.tools.logger import log_observation
from src.tools.validate_w2 import (
    extract_w2_data,
    extract_w2_patch,
    parse_dependency_status,
    parse_filing_status,
)
from src.utils.tax_tables import compute_form_values

MAX_QUESTIONS = 5


class ConversationEngine:
    """State-machine-driven agent harness for the simple tax filing flow."""

    def start_session(self, session: ConversationSession) -> str:
        """Start a session and ask the first budgeted question."""
        self._transition(session, ConversationState.AWAITING_W2)
        response = self._ask(session, ask_w2())
        log_observation(
            session.session_id,
            "session_started",
            {"message": response},
            state=session.state.value,
            question_count=session.question_count,
        )
        return response

    def process_message(self, session: ConversationSession, user_message: str) -> str:
        """Process one user message and return the next agent response."""
        user_message = user_message.strip()
        session.messages.append(ConversationMessage(role="user", content=user_message))
        log_observation(
            session.session_id,
            "user_input_received",
            {"user_message": user_message},
            state=session.state.value,
            question_count=session.question_count,
        )

        if session.state == ConversationState.COMPLETE:
            return self._say(
                session,
                "This session is complete. You can download the form or start a new session.",
            )

        if is_off_topic(user_message):
            log_observation(
                session.session_id,
                "guardrail_redirect",
                {"reason": "off_topic_or_tax_advice"},
                state=session.state.value,
                question_count=session.question_count,
            )
            return self._say(session, off_topic_redirect())

        if session.state == ConversationState.AWAITING_W2:
            return self._handle_w2(session, user_message)
        if session.state == ConversationState.AWAITING_FILING_STATUS:
            return self._handle_filing_status(session, user_message)
        if session.state == ConversationState.AWAITING_DEPENDENCY:
            return self._handle_dependency(session, user_message)
        if session.state == ConversationState.AWAITING_CONFIRMATION:
            return self._handle_confirmation(session, user_message)
        if session.state == ConversationState.AWAITING_CORRECTION:
            return self._handle_correction(session, user_message)

        self._transition(session, ConversationState.AWAITING_W2)
        return self._ask(session, ask_w2())

    def _handle_w2(self, session: ConversationSession, user_message: str) -> str:
        result = extract_w2_data(user_message)
        log_observation(
            session.session_id,
            "tool_execution_completed",
            {
                "tool_name": "validate_w2",
                "success": result.success,
                "message": result.message,
                "warnings": list(result.warnings),
            },
            state=session.state.value,
            question_count=session.question_count,
        )
        if not result.success or result.data is None:
            return self._say(
                session,
                f"I want to get that right. {result.message} Please try again with numbers like 40000 and 2400.",
            )

        session.w2 = result.data
        self._transition(session, ConversationState.AWAITING_FILING_STATUS)
        warning_text = f"\n\nNote: {' '.join(result.warnings)}" if result.warnings else ""
        return self._ask(session, ask_filing_status(result.data) + warning_text)

    def _handle_filing_status(
        self, session: ConversationSession, user_message: str
    ) -> str:
        filing_status = parse_filing_status(user_message)
        if filing_status is None:
            return self._say(
                session,
                "For this prototype, I can support only Single or Married Filing Jointly. Please answer with one of those.",
            )
        session.filing_status = filing_status
        self._transition(session, ConversationState.AWAITING_DEPENDENCY)
        return self._ask(session, ask_dependency())

    def _handle_dependency(
        self, session: ConversationSession, user_message: str
    ) -> str:
        is_dependent = parse_dependency_status(user_message)
        if is_dependent is None:
            return self._say(
                session,
                "I need a yes or no for this one. If a parent or someone else can claim you, answer yes. Otherwise answer no or independent.",
            )
        session.is_dependent = is_dependent
        self._transition(session, ConversationState.AWAITING_CONFIRMATION)
        if session.w2 is None or session.filing_status is None:
            return self._block(session, "The session is missing earlier tax data.")
        return self._ask(
            session,
            ask_confirmation(session.w2, session.filing_status, is_dependent),
        )

    def _handle_confirmation(
        self, session: ConversationSession, user_message: str
    ) -> str:
        normalized = user_message.lower()
        if any(token in normalized for token in ("yes", "correct", "right", "looks good")):
            return self._generate(session)
        if any(token in normalized for token in ("no", "wrong", "fix", "change")):
            self._transition(session, ConversationState.AWAITING_CORRECTION)
            return self._ask(session, ask_correction())
        return self._say(
            session,
            "Please answer yes if everything is correct, or no if one item needs correction.",
        )

    def _handle_correction(
        self, session: ConversationSession, user_message: str
    ) -> str:
        changed = False
        w2_result = (
            extract_w2_patch(user_message, session.w2)
            if session.w2 is not None
            else extract_w2_data(user_message)
        )
        if w2_result.success and w2_result.data is not None:
            session.w2 = w2_result.data
            changed = True

        filing_status = parse_filing_status(user_message)
        if filing_status is not None:
            session.filing_status = filing_status
            changed = True

        dependency = parse_dependency_status(user_message)
        if dependency is not None:
            session.is_dependent = dependency
            changed = True

        if not changed:
            return self._block(
                session,
                "I could not safely apply that correction within the 5-question limit. Please start a new session with the corrected fake W-2 data.",
            )
        return self._generate(session)

    def _generate(self, session: ConversationSession) -> str:
        try:
            values = compute_form_values(session.tax_data())
            pdf_bytes = generate_1040(values)
        except Exception as exc:
            log_observation(
                session.session_id,
                "tool_execution_completed",
                {"tool_name": "generate_1040", "success": False, "error": str(exc)},
                state=session.state.value,
                question_count=session.question_count,
            )
            return self._block(
                session,
                "The form generation tool failed, so I did not create a return. Please try a new session.",
            )

        session.pdf_bytes = pdf_bytes
        session.download_ready = True
        self._transition(session, ConversationState.COMPLETE)
        log_observation(
            session.session_id,
            "tool_execution_completed",
            {
                "tool_name": "generate_1040",
                "success": True,
                "pdf_size_bytes": len(pdf_bytes),
            },
            state=session.state.value,
            question_count=session.question_count,
        )
        return self._say(
            session,
            "Your draft 2025 Form 1040 is ready. Download it here: "
            f"/api/download/{session.session_id}\n\n{DISCLAIMER}",
        )

    def _transition(
        self, session: ConversationSession, new_state: ConversationState
    ) -> None:
        old_state = session.state
        session.state = new_state
        log_observation(
            session.session_id,
            "state_transition",
            {"from": old_state.value, "to": new_state.value},
            state=session.state.value,
            question_count=session.question_count,
        )

    def _ask(self, session: ConversationSession, message: str) -> str:
        if session.question_count >= MAX_QUESTIONS:
            return self._generate(session)
        session.question_count += 1
        log_observation(
            session.session_id,
            "question_count_changed",
            {"question_count": session.question_count},
            state=session.state.value,
            question_count=session.question_count,
        )
        return self._say(session, message)

    def _say(self, session: ConversationSession, message: str) -> str:
        session.messages.append(ConversationMessage(role="agent", content=message))
        log_observation(
            session.session_id,
            "agent_response",
            {"agent_message": message},
            state=session.state.value,
            question_count=session.question_count,
        )
        return message

    def _block(self, session: ConversationSession, message: str) -> str:
        session.error = message
        self._transition(session, ConversationState.BLOCKED)
        return self._say(session, message)

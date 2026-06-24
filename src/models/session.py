# ============================================================================
# Module: session.py
# Purpose: In-memory session state for the tax filing assistant
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from src.models.tax_data import TaxData, W2Data


class ConversationState(str, Enum):
    """Finite states for the deterministic tax filing conversation."""

    START = "start"
    AWAITING_W2 = "awaiting_w2"
    AWAITING_FILING_STATUS = "awaiting_filing_status"
    AWAITING_DEPENDENCY = "awaiting_dependency"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    AWAITING_CORRECTION = "awaiting_correction"
    COMPLETE = "complete"
    BLOCKED = "blocked"


@dataclass
class ConversationMessage:
    """Single chat transcript message."""

    role: str
    content: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class ConversationSession:
    """Mutable session state for one user conversation."""

    session_id: str
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    state: ConversationState = ConversationState.START
    question_count: int = 0
    messages: list[ConversationMessage] = field(default_factory=list)
    w2: W2Data | None = None
    filing_status: str | None = None
    is_dependent: bool | None = None
    pdf_bytes: bytes | None = None
    download_ready: bool = False
    error: str | None = None

    def tax_data(self) -> TaxData:
        """Return complete tax data or raise if the session is incomplete."""
        if self.w2 is None or self.filing_status is None or self.is_dependent is None:
            raise ValueError("Session does not have complete tax data.")
        return TaxData(
            w2=self.w2,
            filing_status=self.filing_status,
            is_dependent=self.is_dependent,
        )


class SessionManager:
    """Simple in-memory session store for the hackathon prototype."""

    def __init__(self) -> None:
        self._sessions: dict[str, ConversationSession] = {}

    def create_session(self) -> ConversationSession:
        """Create and store a new conversation session."""
        session = ConversationSession(session_id=uuid4().hex)
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> ConversationSession | None:
        """Return a session by ID, if present."""
        return self._sessions.get(session_id)

    def require_session(self, session_id: str) -> ConversationSession:
        """Return a session or raise a KeyError for API callers to translate."""
        session = self.get_session(session_id)
        if session is None:
            raise KeyError(f"Unknown session_id: {session_id}")
        return session


AGENTIC TAX-FILING ASSISTANT — PreSearch
0. Scope Statement (1 line)
A conversational AI agent that helps a W-2 earner (~$40k/year) file a 2025 Form 1040 through a friendly chat, within 5 questions, with full observability and guardrails.

1. Domain & Constraints
Use Cases
UC1: User provides W-2 data (Boxes 1, 2, 4, 6)

UC2: User provides filing status (Single/Married) and dependency status

UC3: Agent generates and delivers a completed 2025 Form 1040 PDF

Verification Requirements
Non-negotiable rules:

Max 5 questions asked by agent

Warm, human-like tone

No tax advice given

W-2 data must be validated

PDF must be downloadable

All actions logged for observability

Data Sources
Allowed: W-2 form data provided by user, filing status, dependency status

Forbidden: Real PII, data persistence, external tax data, professional tax advice

2. Scale & Performance
Expected load: Low (hackathon demo, 1-10 concurrent users)

Latency target: <2 seconds per LLM call; <2 minutes total conversation

Cost budget: <$0.10 per conversation (OpenAI GPT-4o-mini)

3. Reliability
Cost of failure: User gets incorrect form; trust is broken

Required guarantees: Deterministic tax computation; validation of all inputs; graceful error recovery

Human-in-loop role: User reviews form before download; judges evaluate system behavior

4. Architecture Decisions
Agent Design
Single / multi-agent: Single orchestration agent with tool calls

State handling: In-memory session state with session ID

LLM Selection
Model: OpenAI GPT-4o-mini (or similar)

Cost: ~$0.01 per conversation

Constraints: Must stay within 5 questions, must maintain warm tone, must call tools deterministically

5. Tool Design
Tool list:

validate_w2: Validates W-2 data structure and types
generate_1040: Computes tax, fills PDF, returns download link
log_observation: Logs agent decisions and actions
Data boundaries: Tools only accept validated, structured data

Error handling: Graceful failures with user-friendly messages

6. Observability
Metrics: Question count, LLM call duration, tool success rate

Logging: Structured JSON logs with session ID, timestamp, event type

Cost tracking: Token usage per LLM call

7. Evaluation Plan
Test types: Unit tests (tax computation, validation), integration tests (end-to-end chat)

Ground truth: Pre-calculated tax returns for sample W-2 data

CI integration: Run tests on push (Pytest)

8. Verification Plan
What is verified: Tax computation accuracy, PDF generation, question budget, tone

How: Automated tests + manual judge review

Failure response: Log error, notify user, allow restart

9. Failure Modes
Failure	Response
Invalid W-2 data	Ask user to correct/re-enter
LLM API failure	Friendly error message, suggest retry
PDF generation failure	Log error, notify user to restart
User goes off-topic	Politely decline, steer back
5-question budget exceeded	Enforce via state machine, end conversation
10. Security
Injection handling: Prompt engineering + state machine prevent off-topic

Data leakage prevention: No persistence, ephemeral session state

Secrets management: Environment variables (.env), .gitignore

11. Testing Strategy
Unit: Tax computation, validation functions, PDF utilities

Integration: End-to-end chat with mock LLM, form generation

Adversarial: Invalid W-2 inputs, off-topic questions, prompt injection attempts

12. Deployment Plan
Hosting: Render (free tier)

Rollback: Git revert and redeploy

Monitoring: Logs via Render dashboard

13. Iteration Plan
Feedback loop: Judge review + user testing

Improvement cycle: Bug fixes and enhancements based on feedback

14. Document Control
Owner: Monica Peters, monigarr@monigarr.com

Version: 1.0 (Final)

Created: 2026-06-24

Last Updated: 2026-06-24
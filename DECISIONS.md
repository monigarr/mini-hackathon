# Agentic Tax-Filing Assistant Decisions

## Deterministic Harness First
The core flow is a finite state machine, not an open-ended LLM chat. This makes the 5-question limit, supported filing statuses, validation, tax math, and tool execution enforceable in code.

## LLM Use
The v1 implementation does not require an LLM call to complete the judged flow. The README and environment keep `OPENAI_API_KEY` available for later conversational polish, but the prototype remains functional without network access or a model outage.

## Tax Scope
The app supports one fake W-2, `Single`, and `Married Filing Jointly`. It rejects complex topics and does not provide tax advice, e-filing, state returns, itemized deductions, or real PII handling.

## 2025 Values
The implementation uses 2025 Form 1040 standard deduction values: `Single = $15,750` and `Married Filing Jointly = $31,500`. Tax is computed with 2025 marginal brackets from IRS Revenue Procedure 2024-40.

## PDF Generation
The local `docs/1040_V2025.pdf` is a fillable AcroForm. The implementation uses `pypdf` to populate a small field map for the lines needed by this prototype.

## Observability
Every session start, user message, state transition, question count update, guardrail redirect, validation result, tool result, and agent response is logged as structured JSON and exposed through `/api/observations/{session_id}`.


# Agentic Tax-Filing Assistant Build Plan

## Current Status

**Status:** Working local prototype implemented
**Last updated:** 2026-06-24
**Primary deliverable:** FastAPI web chat that collects fake W-2 data, enforces a 5-question limit, computes simple 2025 Form 1040 values, generates a downloadable completed PDF, and exposes structured observations for judges.

This file now reflects the implemented repo state, not the original pre-build roadmap.

## Completed Work

| Area | Status | Evidence |
|---|---:|---|
| FastAPI app | Complete | `src/main.py` serves `/`, `/health`, `/api/sessions`, `/api/chat`, `/api/download/{session_id}`, `/api/observations/{session_id}` |
| Web chat UI | Complete | `src/ui/static/index.html`, `style.css`, `app.js` |
| Session state | Complete | `src/models/session.py` in-memory `SessionManager` and `ConversationSession` |
| Deterministic conversation harness | Complete | `src/conversation/engine.py` finite state flow |
| 5-question budget | Complete | `MAX_QUESTIONS = 5`, invalid input and off-topic redirects do not increment |
| W-2 validation | Complete | `src/tools/validate_w2.py` parses Boxes 1, 2, 4, and 6 |
| Filing/dependency parsing | Complete | `parse_filing_status`, `parse_dependency_status` |
| Guardrails | Complete | `src/conversation/guardrails.py`, scoped redirects, no tax advice flow |
| 2025 tax math | Complete | `src/utils/tax_tables.py` uses 2025 standard deductions and brackets |
| PDF generation | Complete | `src/tools/generate_1040.py` overlays visible values on local `docs/1040_V2025.pdf` and flattens the output |
| Observability | Complete | `src/tools/logger.py` structured per-session events exposed by API |
| Sample data | Complete | `data/w2_sample.json` |
| Deployment config | Complete | `render.yaml`, `.env.example`, `requirements.txt` |
| Decision note | Complete | `DECISIONS.md` |
| Test suite | Complete | `tests/` covers validation, tax math, PDF output, conversation, and API |

## Implemented Product Flow

1. User opens the web chat.
2. App creates a session with `POST /api/sessions`.
3. Agent asks Question 1: W-2 Box 1 and Box 2, optionally Box 4 and Box 6.
4. Agent validates W-2 data deterministically.
5. Agent asks Question 2: `Single` or `Married Filing Jointly`.
6. Agent asks Question 3: dependent status.
7. Agent asks Question 4: confirmation.
8. If confirmed, the app computes the return and generates the PDF without asking another question.
9. If correction is needed, Question 5 is used for one correction; no sixth question is asked.
10. User receives `/api/download/{session_id}` and can inspect `/api/observations/{session_id}`.

## Tax And PDF Implementation Notes

- Uses local template: `docs/1040_V2025.pdf`.
- Uses `pypdf` and `reportlab`, not `PyPDF2`.
- Builds a visible overlay for supported Form 1040 lines, merges it onto the local template, and removes form annotations/AcroForm metadata so the result is a flattened PDF.
- Uses 2025 Form 1040 standard deduction values:
  - `Single`: `$15,750`
  - `Married Filing Jointly`: `$31,500`
- Uses 2025 marginal brackets from IRS Revenue Procedure 2024-40.
- For a fake single filer with `$40,000` wages and `$2,400` federal withholding:
  - Standard deduction: `$15,750`
  - Taxable income: `$24,250`
  - Tax: `$2,672`
  - Amount owed: `$272`

## Validation Evidence

Last verified locally on 2026-06-24:

```powershell
python -m py_compile src\main.py src\conversation\engine.py src\conversation\guardrails.py src\conversation\prompts.py src\models\session.py src\models\tax_data.py src\tools\generate_1040.py src\tools\logger.py src\tools\validate_w2.py src\utils\config.py src\utils\tax_tables.py
python -m pytest -q
```

Result:

```text
17 passed
```

Local server smoke evidence:

```powershell
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/health
```

Expected health response:

```json
{"status":"healthy","version":"1.0.0"}
```

## Remaining Work Before Public Submission

| Priority | Work | Owner action |
|---:|---|---|
| 1 | Deploy to Render | Connect repo, set build/start commands from `render.yaml`, deploy |
| 1 | Smoke test public URL | Complete a full browser flow and download PDF from Render |
| 1 | Capture final public URL | Replace local-only deployment notes with the actual URL |
| 2 | Verify PDF visually | Open downloaded PDF and verify populated 1040 lines |
| 3 | Optional LLM polish | Add OpenAI wording layer only if time remains; current judged flow works without it |

## Acceptance Checklist

- [x] Web-based chat interface exists.
- [x] User can provide fake W-2 data.
- [x] Agent asks no more than 5 questions.
- [x] Conversation is warm and scoped.
- [x] Completed 2025 Form 1040 PDF is generated.
- [x] PDF can be downloaded.
- [x] State machine enforces guardrails in code.
- [x] Structured observations are exposed for judges.
- [x] Tests cover core happy path and failure modes.
- [ ] Public Render URL deployed and smoke-tested.
- [ ] Final visual PDF review completed on a downloaded browser artifact.

## Key Files

| File | Purpose |
|---|---|
| `src/main.py` | FastAPI app and API routes |
| `src/conversation/engine.py` | Deterministic conversation orchestration |
| `src/tools/validate_w2.py` | W-2 parsing and validation |
| `src/utils/tax_tables.py` | 2025 tax computation |
| `src/tools/generate_1040.py` | PDF generation |
| `src/tools/logger.py` | Observation logging |
| `tests/` | Automated validation |
| `DECISIONS.md` | Design rationale |
| `render.yaml` | Render deployment config |

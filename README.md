# Agentic Tax-Filing Assistant

A hackathon prototype that helps a simple W-2 earner create a downloadable draft 2025 Form 1040 through a bounded web chat.

This is an educational demo. It is not tax advice, not e-filing, and not a professional tax preparation service. Use fake W-2 data only.

## Status

- Version: `1.0.0`
- Current state: working local prototype
- Public deployment: pending Render deployment
- Local app: `http://127.0.0.1:8000`
- Validation: `16 passed` with `python -m pytest -q`
- CI: `.gitlab-ci.yml` runs Python compile/tests plus GitLab SAST and secret detection

## What Works

- Web chat served by FastAPI.
- Deterministic session state across turns.
- Hard 5-question budget.
- W-2 parsing and validation for Boxes 1, 2, 4, and 6.
- Filing status support for `Single` and `Married Filing Jointly`.
- Dependency status handling.
- 2025 standard deduction and bracket-based tax computation.
- Fillable 2025 Form 1040 PDF generation from `docs/1040_V2025.pdf`.
- Download endpoint for the generated PDF.
- Structured observation trail for judges.
- Render deployment config.
- GitLab CI test/security scan config.
- Root-level `DECISIONS.md`, `BUILD_PLAN.md`, `LICENSE`, and `docs/API.md`.

## Four Pillars

| Pillar | Implementation |
|---|---|
| Chat loop | `src/main.py`, `src/conversation/engine.py`, browser UI in `src/ui/static/` |
| Tools | `validate_w2`, `generate_1040`, `log_observation` |
| Guardrails | Code-enforced question budget, scope checks, input validation, prototype disclaimer |
| Observation | Structured events exposed at `/api/observations/{session_id}` |

## Quick Start

Prerequisite: Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn src.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Sample W-2 input:

```text
Box 1 40000, Box 2 2400, Box 4 40000, Box 6 40000
```

Then answer:

```text
Single
No, I am independent
Yes
```

The app returns a download link for the generated draft Form 1040.

## API

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/` | Web chat UI |
| `GET` | `/health` | Health check |
| `POST` | `/api/sessions` | Create session and receive first question |
| `POST` | `/api/chat` | Send one user message |
| `GET` | `/api/download/{session_id}` | Download generated Form 1040 PDF |
| `GET` | `/api/observations/{session_id}` | View structured session observations |

See [docs/API.md](docs/API.md) for request and response examples.

## Testing

```powershell
python -m py_compile src\main.py src\conversation\engine.py src\conversation\guardrails.py src\conversation\prompts.py src\models\session.py src\models\tax_data.py src\tools\generate_1040.py src\tools\logger.py src\tools\validate_w2.py src\utils\config.py src\utils\tax_tables.py
python -m pytest -q
```

Current test coverage areas:

- W-2 parsing and validation.
- Filing status and dependency parsing.
- 2025 tax computation.
- PDF byte generation and filled field values.
- Conversation happy path.
- Invalid W-2 recovery.
- Off-topic redirect.
- API download and observations.

## CI

GitLab CI is configured in `.gitlab-ci.yml`:

- `python_tests`: installs `requirements.txt`, runs `py_compile`, then runs `pytest`.
- GitLab SAST template.
- GitLab Secret Detection template.

## Deployment

Render config is included in `render.yaml`.

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

Environment variables:

| Variable | Required | Notes |
|---|---:|---|
| `ENVIRONMENT` | No | Defaults to `development`; set `production` on Render |
| `PORT` | No | Render supplies this |
| `OPENAI_API_KEY` | No for v1 | Reserved for optional LLM polish; deterministic flow works without it |

## Data And Safety Boundaries

- Use fake W-2 data only.
- No user accounts.
- No database.
- No e-filing.
- No state tax returns.
- No itemized deductions, self-employment, capital gains, rental income, or multiple W-2s.
- Session state and generated PDFs are in memory only and disappear when the process restarts.
- Observation logs redact/truncate user input and are intended for hackathon judge review.

## Project Structure

```text
.
├── .gitlab-ci.yml
├── src/
│   ├── main.py
│   ├── conversation/
│   ├── models/
│   ├── tools/
│   ├── utils/
│   └── ui/static/
├── tests/
├── docs/
│   ├── 1040_V2025.pdf
│   ├── API.md
│   ├── CLIENT_REQUEST.md
│   ├── PRD.md
│   └── USERS.md
├── data/w2_sample.json
├── BUILD_PLAN.md
├── DECISIONS.md
├── LICENSE
├── render.yaml
└── requirements.txt
```

## Key Decisions

See [DECISIONS.md](DECISIONS.md).

In short:

- State machine first, LLM optional.
- Deterministic validation and tax math.
- No real PII storage.
- No e-filing.
- Fill local IRS PDF with `pypdf`.
- Keep frontend simple because harness quality is the judging priority.

## Known Remaining Work

- Deploy to Render and smoke test the public URL.
- Visually inspect the generated browser-downloaded PDF.
- Decide whether local untracked `docs/1040_V2025_dummy_data.pdf` belongs in the repo.
- Add optional LLM wording polish only if the deterministic judged flow remains stable.

## License

MIT. See [LICENSE](LICENSE).

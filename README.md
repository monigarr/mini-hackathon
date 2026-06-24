# AGENTIC TAX-FILING ASSISTANT

> **Hackathon Challenge — June 24, 2026**  
> *A conversational AI agent that helps W-2 earners file their 2025 Form 1040*

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)
[![Render](https://img.shields.io/badge/Render-Deployed-purple.svg)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [The Four Pillars](#the-four-pillars)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**The Agentic Tax-Filing Assistant** is an AI-native, enterprise-grade prototype designed for the June 24, 2026 Mini Hackathon. It demonstrates how a conversational AI agent can transform a complex, manual process—filing a U.S. federal tax return—into a simple, friendly 5-question conversation.

### Business Objective

- **Problem:** Filing Form 1040 is complex, error-prone, and overwhelming for first-time filers
- **Solution:** A guided, warm conversational experience that collects data and generates a completed form
- **Value:** Proves the viability of agentic systems for step-by-step processes with safety and observability

### Status

- **Version:** 1.0.0 (Production-Ready Prototype)
- **Status:** Active Development
- **Deployment:** [Live Demo](https://agentic-tax-assistant.onrender.com)

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Web Chat Interface** | Simple, accessible chat interface for tax filing |
| **5-Question Budget** | Maximum 5 questions to gather all required data |
| **W-2 Data Collection** | Validates and stores W-2 Boxes 1, 2, 4, and 6 |
| **Filing Status Support** | Handles "Single" and "Married Filing Jointly" |
| **Dependency Status** | Determines if filer can be claimed as dependent |
| **Tax Computation** | Uses 2025 tax tables and standard deduction |
| **PDF Generation** | Populates a 2025 Form 1040 PDF with computed values |
| **Downloadable Output** | Users download their completed form instantly |
| **Full Observability** | Structured JSON logging of all agent decisions |
| **Guardrails** | Prevents off-topic responses and tax advice |
| **Human-Friendly Tone** | Warm, empathetic, and clear communication |

---

## 🏗️ Architecture

### Architectural Style: Modular Monolith with AI Orchestration

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Browser                           │
│               (Web Chat Interface)                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Server                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │   Routes   │  │  Session   │  │   Static   │          │
│  │  (API)     │  │  Manager   │  │   Files    │          │
│  └────────────┘  └────────────┘  └────────────┘          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Orchestration Layer                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               Conversation Engine                    │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐   │  │
│  │  │   State    │  │   Prompt   │  │ Question   │   │  │
│  │  │  Machine   │  │  Builder   │  │  Counter   │   │  │
│  │  └────────────┘  └────────────┘  └────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 LLM Orchestrator                     │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐   │  │
│  │  │   Model    │  │   Prompt   │  │  Response  │   │  │
│  │  │  Router    │  │  Template  │  │  Parser    │   │  │
│  │  └────────────┘  └────────────┘  └────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       Tool Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Validate   │  │   Generate   │  │   Logging    │    │
│  │   W-2 Data   │  │   Form 1040  │  │   Tool       │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                Data & Computation Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Tax        │  │   PDF        │  │   Form       │    │
│  │  Computation │  │  Generator   │  │  Template    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles (M.O.M. + M.I.L.E.)

- **Human Accountability First:** AI accelerates, humans validate
- **Ancient + Human + AI Integration:** Deterministic logic + human-like conversation + LLM orchestration
- **Enterprise from Day One:** Security, maintainability, observability built in
- **Documentation as Infrastructure:** Comprehensive docs for rapid handoff
- **Handoff-Ready Engineering:** Clean interfaces, one-command setup

---

## 🧩 The Four Pillars

This system demonstrates the four essential pillars of agentic systems:

### 1. Chat Loop
- Web-based conversational interface with state management across turns
- Session ID tracking for continuity
- Warm, human-like interaction design

### 2. Tools
- **`validate_w2`**: Validates W-2 data structure and types
- **`generate_1040`**: Computes tax, fills PDF, generates download link
- **`log_observation`**: Logs all agent decisions and actions

### 3. Guardrails
- **5-Question Budget:** Strict counter enforced by state machine
- **Off-Topic Prevention:** Politely declines irrelevant questions
- **No Tax Advice:** Clear disclaimer and prompt constraints
- **Input Validation:** All W-2 data validated before use

### 4. Observation
- Structured JSON logging of all events
- Session ID correlation for audit trails
- Full conversation transcripts
- Tool call logs with inputs and outputs

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key (or compatible LLM provider)
- Git

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/agentic-tax-assistant.git
cd agentic-tax-assistant
```

2. **Set up virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. **Run the application:**
```bash
uvicorn src.main:app --reload
```

6. **Open the chat:**
```
http://localhost:8000
```

---

## 🌐 Deployment

### Deploy to Render (Recommended)

1. **Push your code to GitHub**

2. **Create a new Web Service on Render:**
   - Connect your GitHub repository
   - Use the following settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
     - **Environment Variables:**
       - `OPENAI_API_KEY`: Your OpenAI API key
       - `ENVIRONMENT`: `production`

3. **Deploy:**
   - Render will automatically deploy on push
   - Your app will be available at `https://your-app.onrender.com`

### One-Command Local Run

```bash
OPENAI_API_KEY=your_key_here uvicorn src.main:app --reload
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `ENVIRONMENT` | No | `development` or `production` (default: development) |
| `PORT` | No | Port for server (default: 8000) |

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_tax_computation.py
```

### Test Categories

| Category | Description | File |
|----------|-------------|------|
| **Unit Tests** | Tax computation, validation, PDF utilities | `test_tax_computation.py` |
| **Integration Tests** | End-to-end chat with mock LLM | `test_end_to_end.py` |
| **Edge Cases** | Invalid inputs, married filing, dependent status | `test_validation.py` |

### Sample W-2 Data

Sample data is provided in `data/w2_sample.json` for testing:

```json
{
  "employer_name": "Acme Corporation",
  "employer_ein": "12-3456789",
  "employee_name": "Jane Doe",
  "employee_address": "123 Main St, Anytown, USA",
  "wages": 40000.00,
  "federal_tax_withheld": 2400.00,
  "social_security_wages": 40000.00,
  "social_security_tax": 2480.00,
  "medicare_wages": 40000.00,
  "medicare_tax": 580.00
}
```

---

## 📁 Project Structure

```
agentic-tax-assistant/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── conversation/
│   │   ├── __init__.py
│   │   ├── engine.py           # Conversation orchestration
│   │   ├── state_machine.py    # Question flow state machine
│   │   └── prompts.py          # System prompts and templates
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── validate_w2.py      # W-2 data validation
│   │   ├── generate_1040.py    # Tax computation and PDF generation
│   │   └── logger.py           # Observation logging
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tax_data.py         # Data classes for tax info
│   │   └── session.py          # Session state management
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── static/             # HTML, CSS, JS
│   │   └── templates/          # Jinja2 templates
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Environment configuration
│       └── pdf_utils.py        # PDF generation helpers
├── tests/
│   ├── test_tax_computation.py
│   ├── test_validation.py
│   └── test_end_to_end.py
├── data/
│   ├── w2_sample.json          # Sample W-2 data for testing
│   └── form_1040_template.pdf  # 2025 Form 1040 template
├── docs/
│   ├── ARCHITECTURE.md         # Comprehensive architecture
│   ├── DECISIONS.md            # Design decisions
│   └── API.md                  # API documentation
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── render.yaml                 # Render deployment configuration
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── LICENSE                     # MIT License
```

---

## 🛠️ Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Web Framework** | FastAPI 0.115+ | Async API, auto-docs, lightweight |
| **LLM Provider** | OpenAI GPT-4o-mini | Cost-effective, high-quality conversation |
| **LLM Orchestration** | Direct API or LangChain | Conversational orchestration |
| **PDF Generation** | PyPDF2 / PyMuPDF | Fill existing PDF forms |
| **Frontend** | Vanilla HTML/CSS/JS | Minimal, accessible interface |
| **Deployment** | Render | Free tier, easy deployment |
| **Testing** | Pytest | Standard, comprehensive testing |
| **Environment** | Python 3.10+ | Modern, widely supported |
| **Logging** | Python logging + JSON | Structured observability |

---

## 🔒 Security & Compliance

### Data Protection

- **No PII Storage:** All data is ephemeral; no persistence
- **Environment Variables:** All secrets in `.env`, never in code
- **HTTPS:** Enforced via Render
- **Input Validation:** All user inputs validated before use
- **Session Isolation:** Each session has unique ID

### Compliance

- **Disclaimer:** System explicitly states it's a prototype, not a professional service
- **Educational Use:** Not a real tax preparation service
- **No E-Filing:** System does not transmit to IRS
- **Fake Data Only:** Test data is synthetic; no real filings

### Security Best Practices

- ✅ Prompt injection mitigation
- ✅ Input sanitization
- ✅ Environment-based configuration
- ✅ Dependency scanning (Dependabot)
- ✅ Rate limiting (via Render)
- ✅ Health checks

---

## 📊 Observability

### Logging

All system events are logged in structured JSON format:

```json
{
  "timestamp": "2026-06-24T10:00:00Z",
  "session_id": "abc123",
  "event_type": "llm_call",
  "event_data": {
    "prompt": "...",
    "response": "...",
    "token_usage": { "prompt": 150, "completion": 50 }
  }
}
```

### Metrics Tracked

- LLM call latency
- Token usage per conversation
- Question count
- Tool success/failure rates
- Conversation duration
- Error rates

---

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/your-feature`
3. **Make your changes** (include tests and documentation)
4. **Run tests:** `pytest`
5. **Commit your changes:** `git commit -m "feat: add your feature"`
6. **Push to the branch:** `git push origin feature/your-feature`
7. **Create a Pull Request**

### Coding Standards

- **Style:** PEP 8 with Black formatting
- **Docstrings:** All functions must have docstrings
- **Type Hints:** Use Python type hints
- **Headers:** Include the standard code comment header
- **Tests:** New features must include tests

### Reporting Issues

- Use the GitHub Issues tracker
- Include: steps to reproduce, expected behavior, actual behavior
- For security issues, contact directly

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Monica Peters

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📚 Documentation

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — Comprehensive system architecture
- **[PRD.md](docs/PRD.md)** — Product requirements document
- **[DECISIONS.md](docs/DECISIONS.md)** — Design decisions and rationale
- **[API.md](docs/API.md)** — API documentation
- **[USERS.md](docs/USERS.md)** — User personas and use cases

---

## 🙏 Acknowledgments

- **Hackathon Challenge:** Gauntlet AI for America, Mini Hackathon June 24, 2026
- **Architecture Framework:** MoniGarr Operating Model (M.O.M.) + M.I.L.E.
- **Engineering Standards:** Echelon Enterprise Engineering Protocols

---

## 📞 Contact

**Owner:** Monica Peters  
**Email:** monigarr@monigarr.com  
**GitHub:** [@monigarr](https://github.com/monigarr)  

---

## ⚡ Quick Links

- [Live Demo](https://agentic-tax-assistant.onrender.com)
- [GitHub Repository](https://github.com/yourusername/agentic-tax-assistant)
- [Issue Tracker](https://github.com/yourusername/agentic-tax-assistant/issues)
- [Documentation](docs/)

---

**Built with ❤️ for the Gauntlet AI for America Mini Hackathon Challenge**

*"AI accelerates engineering. Humans remain accountable. Systems remain governable."*
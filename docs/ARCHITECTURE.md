
# ============================================================================
# PROJECT ARCHITECTURE
# ============================================================================
# Project Name: Agentic Tax-Filing Assistant
# Repository: agentic-tax-assistant
# Version: 1.0.0
# Status: Production-Ready Prototype
# Classification: Internal/Educational
# Authors: Monica Peters, monigarr@monigarr.com
# Organization: Gauntlet AI for America, Mini Hackathon June 24th 2026
# Primary Maintainers: Monica Peters
# Created: 2026-06-24
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================
#
# DESCRIPTION
# ----------------------------------------------------------------------------
# High-level architectural definition for an AI-native tax filing assistant
# designed for the June 24th 2026 Mini Hackathon Challenge. This system implements a
# conversational agent that helps users file a 2025 Form 1040 through a
# friendly chat interface, demonstrating the four pillars of agentic systems:
# chat loop, tools, guardrails, and observation.
#
# The system follows:
# - MoniGarr Operating Model (M.O.M.)
# - M.I.L.E. (MoniGarr Intelligence-Led Engineering)
# - Echelon Enterprise Engineering Protocols
#
# This document defines:
# - Architectural intent and tradeoffs
# - Constraints and trust boundaries
# - AI integration strategies
# - Security posture and data governance
# - Operational expectations and failure modes
# - Scalability assumptions and forward path
# - Human accountability structures
#
# ============================================================================

# 1. Executive Summary

## Overview

This system is an AI-native, enterprise-grade prototype platform designed to
demonstrate the viability of agentic systems for complex, step-by-step
processes. Specifically, it provides a conversational interface for filing a
simple U.S. federal tax return (Form 1040) for a W-2 employee earning
approximately $40,000/year.

The system orchestrates an LLM to conduct a guided conversation, collects
structured data through deterministic tool calls, generates a filled PDF
tax form, and provides a downloadable result—all within a 5-question budget
and a warm, human-like interaction.

## Business Objective

- **Primary Problem:** Filing a U.S. federal tax return is complex, manual,
  and error-prone, especially for first-time or infrequent filers.
- **Expected ROI:** Prove the viability of an agentic harness for this task,
  demonstrating that LLMs can transform complex, step-by-step processes into
  accessible, conversational experiences.
- **Strategic Value:** Establish a reference architecture for AI-native
  applications that combines conversation, tools, safety, and observability.
- **Long-Term Operational Intent:** Serve as a foundation for future
  expansion into more complex tax scenarios, multi-turn conversations, and
  production-grade tax preparation services.

## Operational Philosophy

This project follows:

- AI-First Engineering: AI participates in planning, analysis, and execution.
- AI-Native Architecture: LLMs are core orchestration engines, not add-ons.
- Human-in-the-loop accountability: Humans remain accountable for validation
  and final decisions.
- Sovereign engineering principles: Clear ownership, documentation, and
  handoff-readiness.
- Echelon enterprise operational standards: Security, observability, and
  maintainability from day one.
- Scale-adaptive rigor: Appropriate complexity for a hackathon prototype,
  with clear paths to scale.

# 2. MoniGarr Operating Model (M.O.M.)

## Core Engineering Principles

### 2.1 Human Accountability First

AI accelerates execution but does not replace:
- Accountability for final output accuracy
- Governance of data collection and usage
- Validation of tax calculations
- Strategic judgment on system design

Human reviewers (the judges) will validate that the system works correctly,
and users are responsible for reviewing their filled tax form.

### 2.2 Ancient + Human + Artificial Intelligence Integration

This system integrates:
- **Traditional Intelligence:** Deterministic tax computation logic and
  PDF generation tools that ensure mathematical accuracy.
- **Human Contextual Reasoning:** The conversation is designed to feel
  warm and human, gathering information in a natural way.
- **Artificial Intelligence Acceleration:** An LLM orchestrates the
  conversation, interprets user inputs, and guides the interaction.

All three layers are visible and auditable through the observation system.

### 2.3 Enterprise from Day One

All systems support:
- Security: No real PII stored, prompt injection prevention
- Maintainability: Clean separation of concerns, modular architecture
- Observability: Full logging of all agent decisions and actions
- Extensibility: Clear interfaces for adding more tax forms or statuses
- Documentation: Comprehensive ARCHITECTURE.md and DECISIONS.md
- Rapid handoff: One-command local run, clear deployment instructions
- Operational continuity: Deployed to Render for immediate evaluation

No prototype-grade architecture is permitted in the production repository.

### 2.4 Documentation as Infrastructure

Documentation is treated as:
- Operational infrastructure: Guides deployment and maintenance
- Onboarding infrastructure: Enables rapid team handoff
- Governance infrastructure: Defines system boundaries and constraints
- Legal protection infrastructure: Disclaims tax advice and liability
- Continuity infrastructure: Ensures the system can be rebuilt or extended

### 2.5 Handoff-Ready Engineering

Systems are transferable to:
- Engineering teams: Clean architecture, clear interfaces, code headers
- Auditors: Full observability logs, deterministic computation
- Compliance officers: Clear guardrails, disclaimer, data governance
- Executives: High-level architecture, business objective, strategic value
- Subject matter experts: Tax logic is explicit and testable
- External vendors: One-command setup, public URL for evaluation

# 3. System Scope

## In Scope

- Conversational chat interface for collecting tax filing data
- Support for W-2 income (~$40,000/year)
- Support for "Single" and "Married Filing Jointly" statuses
- Determination of dependent status (can be claimed as a dependent)
- Computation of standard deduction, taxable income, and tax liability
- Generation of a filled 2025 Form 1040 PDF
- Downloadable form output
- 5-question maximum conversation budget
- Warm, human-like conversation design
- Full observability logging of all agent actions
- Guardrails: Off-topic prevention, validation, budget enforcement
- Deployment to a public URL on Render

## Out of Scope

- E-Filing or submission to the IRS
- Complex tax situations: self-employment, capital gains, itemized deductions,
  rental income, business income, or other income sources
- Multiple W-2s (designed for single W-2 earner)
- Data persistence across sessions (all data is ephemeral)
- User accounts or authentication
- Mobile native applications (web-based only)
- Professional tax advice (system explicitly disclaims this)
- Real PII or real tax filings (fake test data only)

# 4. STRATA-X Scale Classification

| Level | Description                      |
| ----- | -------------------------------- |
| X0    | Micro modifications              |
| X1    | Local feature                    |
| X2    | Component architecture           |
| X3    | Cross-system architecture        |
| X4    | Institutional systems            |
| X5    | Sovereign / generational systems |

## Current Classification: X2

**Rationale:** This system is a component-level architecture designed for
a specific, bounded use case (simple tax filing). It demonstrates core
agentic patterns (chat, tools, guardrails, observation) that could be
extended to X3 (cross-system) by integrating with e-filing APIs or
X4 (institutional) by supporting multiple tax forms and state returns.
The architecture is designed with X3+ extensibility in mind.

# 5. Architecture Goals

## Functional Goals

1. **Conversational Data Collection:** Gather all required tax data (W-2,
   filing status, dependency status) through a friendly, 5-question chat.
2. **Accurate Tax Computation:** Compute federal income tax correctly
   for the given inputs using 2025 tax tables and standard deduction.
3. **PDF Generation:** Populate a 2025 Form 1040 PDF with the computed
   values and make it downloadable.
4. **Guardrails:** Enforce the 5-question budget, prevent off-topic
   responses, validate input data, and decline to give tax advice.
5. **Observability:** Log all agent decisions, tool calls, and
   question/answer pairs in a format that judges can review.

## Non-Functional Goals

### Security
- No real PII or sensitive data stored
- All user input is ephemeral for the session
- Environment variables for all secrets (API keys)
- Prompt injection mitigation through deterministic state machines

### Privacy
- No data persistence beyond session lifetime
- Session IDs are temporary and not tied to users
- No analytics or tracking of user inputs

### Stability
- Graceful error handling for LLM failures
- Fallback messages for tool failures
- Deterministic computations independent of LLM reliability

### Reliability
- End-to-end happy path success > 95%
- Individual LLM calls < 2 seconds
- Total conversation < 2 minutes

### Performance
- Lightweight web UI with minimal dependencies
- Efficient PDF generation using pre-filled form templates
- Cached LLM responses where appropriate

### Accessibility
- Web chat usable with keyboard and screen reader
- Clear, readable text with sufficient contrast
- Simple, intuitive interface

### Observability
- Structured JSON logging of all system events
- Session ID tracking for auditability
- Tool call logs with inputs and outputs
- LLM interaction logs with prompts and responses

### Maintainability
- Modular, single-responsibility components
- Clear separation: UI, Orchestrator, Tools, Verification
- Comprehensive code headers and documentation
- One-command local development setup

### Scalability
- Stateless architecture (session state in memory)
- Horizontal scalability through stateless API design
- Rate limiting for LLM API calls

### Portability
- Environment-based configuration
- Container-ready architecture
- Can be deployed to any cloud provider or local machine

### Disaster Recovery
- Session state can be recreated from logs
- PDF generation can be re-run from collected data
- Graceful degradation when LLM is unavailable

# 6. High-Level System Architecture

## Architectural Style: Modular Monolith with AI Orchestration

This architecture uses a modular monolith pattern with clear separation
of concerns, making it easy to understand, test, and deploy. The AI
orchestration layer acts as the "brain" that coordinates the conversation
and tool calls, while deterministic modules handle computation and output.

```
┌─────────────────────────────────────────────────────────────────┐
│                          Client Browser                         │
│                    (Web Chat Interface)                         │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI Server                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Routes     │  │  Session     │  │   Static     │         │
│  │  (API)       │  │  Manager     │  │   Files      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Orchestration Layer                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Conversation Engine                    │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │  │
│  │  │   State    │  │   Prompt   │  │ Question   │        │  │
│  │  │  Machine   │  │  Builder   │  │  Counter   │        │  │
│  │  └────────────┘  └────────────┘  └────────────┘        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    LLM Orchestrator                      │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │  │
│  │  │   Model    │  │   Prompt   │  │  Response  │        │  │
│  │  │  Router    │  │  Template  │  │  Parser    │        │  │
│  │  └────────────┘  └────────────┘  └────────────┘        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Tool Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Validate   │  │   Generate   │  │   Logging    │         │
│  │   W-2 Data   │  │   Form 1040  │  │   Tool       │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data & Computation Layer                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Tax        │  │   PDF        │  │   Form       │         │
│  │  Computation │  │  Generator   │  │  Template    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

# 7. AI-Native Engineering Model

## AI-First Philosophy

AI participates in:
- **Planning:** The conversation flow is designed to be natural and adaptive
  based on user responses.
- **Analysis:** User inputs are interpreted and classified by the LLM.
- **Implementation:** The LLM generates human-like responses and guides the
  conversation.
- **Review:** The LLM can ask for clarifications and validate data.
- **Documentation:** System behavior is documented in this architecture.

## AI-Native Capabilities

- **Agents:** The LLM acts as the conversational agent, interpreting user
  inputs and orchestrating the interaction.
- **Workflows:** The conversation follows a state machine that guides the
  user through data collection in a predictable yet flexible manner.
- **Orchestration:** The LLM is prompted to use specific tools (validate_w2,
  generate_1040) at the appropriate time.
- **Retrieval:** System prompts include the tax computation logic and
  form structure, enabling the LLM to understand what data is needed.
- **Cloud Inference:** Uses a hosted LLM via API (e.g., OpenAI, Anthropic,
  or a local model via Ollama).
- **Evaluation:** System behavior is evaluated through end-to-end testing
  and observation logs.

## Human-in-the-Loop Controls

Humans retain authority over:
- **Deployment:** Manual deployment to Render via git push.
- **Security Decisions:** Environment variables for API keys.
- **Architectural Approval:** This document serves as the architectural
  baseline.
- **Compliance:** Disclaimer and data governance defined in PRD.
- **Data Governance:** No real data stored; fake test data only.
- **Final Validation:** Users review the generated form before download.

# 8. Agent Council Review (ACR)

## AI Agent Roles

| Agent               | Responsibility                                           |
| ------------------- | -------------------------------------------------------- |
| Architect Agent     | This document provides architectural review              |
| Security Agent      | Environment variables, prompt injection prevention       |
| Audit Agent         | Observation logs provide compliance review               |
| Verification Agent  | Tax computation validation, W-2 data validation          |
| Documentation Agent | This ARCHITECTURE.md and code headers                    |
| Adversarial Agent   | Testing with edge cases: invalid W-2, off-topic inputs   |
| Performance Agent   | LLM call latency, conversation duration monitoring       |

## Agent Governance Rules

- No autonomous production deployment (manual git push)
- No self-authorizing behavior (tools are called by orchestration)
- All outputs require verification (tax computation is deterministic)
- Human override always available (users can restart the conversation)

# 9. Security Architecture

## Security Philosophy

Security is:
- **Proactive:** Built into the architecture from the start.
- **Layered:** Multiple controls: input validation, prompt engineering,
  environment isolation.
- **Observable:** All actions logged for audit.
- **Continuously Validated:** Tested with adversarial inputs.

## Security Requirements

- **Authentication:** Not required (prototype, no accounts)
- **Authorization:** Not required (single-user session)
- **RBAC:** Not required (no multi-user)
- **Audit Logging:** All interactions logged with session ID
- **Encryption:** HTTPS via Render
- **Secrets Management:** Environment variables for API keys
- **Dependency Scanning:** Standard package versioning
- **Supply Chain Protection:** Only trusted packages
- **AI Prompt Injection Mitigation:** Guardrails prevent off-topic responses
- **Data Isolation:** Each session is isolated with its own state

## Threat Model

### Internal Threats
- **Data Leakage:** Session data is ephemeral, no persistence
- **Privilege Escalation:** Not applicable (no user roles)
- **Misuse of Tools:** Tools are bounded and validated

### External Threats
- **Prompt Injection:** Guardrails and state machine prevent off-topic
- **API Key Exposure:** Environment variables, .gitignore
- **DoS Attacks:** Simple prototype, rate limiting at Render
- **Man-in-the-Middle:** HTTPS via Render

### AI Misuse Risks
- **Hallucination:** Deterministic tax computation overrides LLM
- **Incorrect Advice:** Disclaimer prevents advice-giving
- **Data Fabrication:** LLM can only use tool-provided data

### Operational Threats
- **LLM Outage:** Graceful error messages
- **Infrastructure Failure:** Render handles uptime
- **Corrupted Data:** Input validation prevents injection

### Social Engineering Risks
- **Tax Fraud:** Only fake data, no real filing
- **Phishing:** No data collection beyond necessary tax info

# 10. Privacy & Data Governance

## Data Classification

| Classification | Description                       |
| -------------- | --------------------------------- |
| Public         | Code repository, architecture    |
| Internal       | Session logs, debug data         |
| Confidential   | User-provided tax data (W-2 info)|
| Sovereign      | N/A (no Indigenous data)        |

## Data Handling

- **Collection:** Only W-2 data, filing status, and dependency status
- **Storage:** In-memory session state only; no persistence
- **Retention:** Destroyed at end of session
- **Sharing:** No sharing with third parties
- **Disposal:** Session state garbage-collected

## Sovereign AI Considerations

- Not applicable for this prototype (no Indigenous data or languages)

# 11. Observability Architecture

## Observability Stack

- **Langfuse** (optional) for LLM tracing and analytics
- **Structured JSON Logging** to console for easy parsing
- **Session ID Tracking** to correlate all events
- **Tool Call Logs** with inputs and outputs
- **Conversation Transcript** for full auditability

## Monitoring Goals

- **System Reliability:** Track errors and failures
- **AI Behavior Tracking:** Log prompts, responses, and tool calls
- **Anomaly Detection:** Flag unexpected user inputs or LLM behaviors
- **Regression Visibility:** Test suite ensures no regressions
- **Operational Transparency:** Judges can see the agent's "chain of thought"

## Log Structure

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

# 12. Verification & Evaluation

## Verification Philosophy

All AI outputs are:
- **Untrusted by default:** LLM responses are not used directly for computation
- **Verified before action:** Tax computation is deterministic and testable
- **Traceable:** Every decision is logged with context
- **Reproducible:** Given the same inputs, the output is identical

## Evaluation Categories

### Functional Correctness
- **Unit Tests:** Tax computation, PDF generation, validation
- **Integration Tests:** End-to-end chat flow with mock LLM
- **Happy Path:** Single W-2, single filer, not dependent
- **Edge Cases:** Married filing jointly, dependent status, invalid inputs

### Hallucination Resistance
- **Guardrails:** Off-topic responses are prevented
- **State Machine:** LLM can only ask questions in the allowed order
- **Validation:** All tool inputs are validated before use

### Security Compliance
- **Penetration Testing:** Prompt injection attempts should fail
- **Data Leakage:** No PII or sensitive data in logs
- **API Key Security:** No keys in code

### Adversarial Testing
- **Invalid W-2:** Missing fields, incorrect formats
- **Off-topic:** User asks about stock trading, other tax forms
- **Jailbreak:** User tries to get the agent to give tax advice

### Edge-Case Handling
- **Very low income:** Below standard deduction (tax = 0)
- **Very high W-2:** Within the ~$40k range, but test boundaries
- **Married Filing Jointly:** Standard deduction doubles
- **Dependent status:** Tax computation adjusts

### Regression Testing
- **CI/CD Pipeline:** Run tests on every push
- **Snapshot Testing:** Expected PDF output is compared

# 13. Deployment Architecture

## Environments

| Environment | Purpose            | URL |
| ----------- | ------------------ | --- |
| Local       | Development        | http://localhost:8000 |
| Production  | Live operations    | https://tax-assistant.onrender.com |

## CI/CD Philosophy

- **Automated Validation:** Run tests on push
- **Security Scanning:** Dependabot for dependencies
- **Reproducible Builds:** Requirements.txt or pyproject.toml
- **Rollback Support:** Git revert and redeploy
- **Artifact Traceability:** Git commits map to deployed versions

## Deployment to Render

1. **Dependencies:** Defined in requirements.txt
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables:** Set in Render dashboard
5. **Health Check:** `/health` endpoint

## render.yaml

```yaml
services:
  - type: web
    name: agentic-tax-assistant
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: ENVIRONMENT
        value: production
```

## .env File (Local Development)

```
OPENAI_API_KEY=your_key_here
ENVIRONMENT=development
```

## .gitignore

```
.env
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
dist/
*.egg-info/
node_modules/
*.log
.DS_Store
.coverage
htmlcov/
.pytest_cache/
```

# 14. Scale Considerations

## Performance

- **Response Time:** LLM calls < 2 seconds; total conversation < 2 minutes
- **Concurrency:** Render free tier supports low concurrency (< 10 concurrent)
- **Caching:** Not implemented for prototype (stateless)
- **Database:** None (in-memory session state)

## Cost

- **LLM API Costs:** ~$0.01 per conversation (GPT-4o-mini or similar)
- **Free Tier Limits:** OpenAI $5 free credits, Render free tier
- **Optimization:** Use smaller models, cache prompts

## Concurrency

- **Current Capacity:** ~10 concurrent sessions (Render free tier)
- **Horizontal Scaling:** Stateless design allows multiple instances
- **Session Management:** In-memory with session IDs; can migrate to Redis

# 15. Known Limitations

## Explicit Tradeoffs

### 1. Limited Tax Scope
- **Decision:** Only support W-2 income ~$40k
- **Rationale:** Hackathon constraints; keep it simple
- **Future:** Expand to other income types and forms

### 2. In-Memory Session State
- **Decision:** No database, store state in memory
- **Rationale:** Simple, no persistence needed
- **Future:** Add Redis for production scaling

### 3. Single LLM Provider
- **Decision:** Use OpenAI API
- **Rationale:** Reliable, well-supported
- **Future:** Support multiple providers (Anthropic, local)

### 4. No User Authentication
- **Decision:** No login required
- **Rationale:** Prototype, not production
- **Future:** Add authentication for real deployment

### 5. PDF Generation Method
- **Decision:** Use fillable PDF with PyPDF2/PyMuPDF
- **Rationale:** Simple, no server-side rendering
- **Future:** Use HTML-to-PDF for more flexibility

### 6. Hard-Coded Tax Tables
- **Decision:** Hard-code 2025 tax tables
- **Rationale:** Simple, accurate, no API dependency
- **Future:** Pull from IRS API or updated configs

## Technical Debt

- No comprehensive test suite (basic tests only)
- No rate limiting for API calls
- No monitoring or alerting
- No backup LLM provider

# 16. Forward Path

## Next Capabilities

### Phase 1: Core (Current)
- [x] Chat loop
- [x] Tools (validate_w2, generate_1040)
- [x] Guardrails (5-question budget, off-topic prevention)
- [x] Observation (full logging)
- [x] PDF generation
- [x] Web chat interface
- [x] Deployment to Render

### Phase 2: Enhanced Features
- [ ] Support for additional filing statuses (Head of Household)
- [ ] Support for dependents (Child Tax Credit)
- [ ] Mid-conversation corrections
- [ ] Observation trail in UI
- [ ] W-2 input validation and recovery

### Phase 3: Production Readiness
- [ ] User authentication
- [ ] Session persistence (Redis)
- [ ] Rate limiting
- [ ] Monitoring and alerting (Prometheus/Grafana)
- [ ] Comprehensive test suite
- [ ] Multiple LLM providers with fallback
- [ ] E-filing integration (optional)

## Scaling Roadmap

1. **X2 (Current):** Component architecture for single use case
2. **X3:** Cross-system integration: state returns, multiple W-2s
3. **X4:** Institutional system: full tax preparation, audit trails
4. **X5:** Sovereign system: community-owned, self-hosted tax filing

## Migration Strategies

- **Session State:** Migrate from in-memory to Redis with minimal code changes
- **LLM Provider:** Abstract the LLM client to support multiple providers
- **PDF Generation:** Replace fillable PDF with HTML-to-PDF for more flexibility
- **Data Persistence:** Add database for audit trails and user accounts

# 17. Failure Modes & Recovery

## Failure Expectations

Assume:
- **Network Failures:** User loses connection mid-conversation
- **Model Failures:** LLM API returns an error or times out
- **Hallucinations:** LLM generates unexpected or nonsensical responses
- **Infrastructure Degradation:** Render experiences issues
- **Corrupted Data:** User provides invalid W-2 data
- **Unavailable Services:** LLM API is down

## Recovery Strategies

### Network Failures
- **Behavior:** Session state maintained in memory
- **Recovery:** User can refresh and resume (same session ID)
- **Fallback:** If session lost, restart conversation

### Model Failures
- **Behavior:** Catch LLM API errors
- **Recovery:** Return friendly error message, suggest retry
- **Fallback:** Use deterministic fallback responses

### Hallucinations
- **Behavior:** State machine restricts LLM to allowed actions
- **Recovery:** Validation tools check inputs before use
- **Fallback:** Re-prompt with stronger constraints

### Infrastructure Degradation
- **Behavior:** Render health checks, auto-restart
- **Recovery:** Minimal downtime
- **Fallback:** None (Render single instance)

### Corrupted Data
- **Behavior:** Validation tool checks W-2 data
- **Recovery:** Ask user to correct or re-enter
- **Fallback:** Use default values with warning

### Unavailable Services
- **Behavior:** Detect LLM API failure
- **Recovery:** Notify user and suggest trying later
- **Fallback:** Use a local model (Ollama) if available

## Incident Response

1. **Detection:** Logs and user reports
2. **Classification:** Is it an LLM issue, infrastructure, or user input?
3. **Containment:** Restart service or rollback
4. **Resolution:** Fix and redeploy
5. **Post-Mortem:** Update architecture and tests

# 18. Compliance & Regulatory Considerations

## Applicable Regulations

- **GDPR:** Not applicable (no EU users, no data persistence)
- **HIPAA:** Not applicable (no health data)
- **SOC2:** Not applicable (prototype)
- **IRS Regulations:** The system is not e-filing and does not represent itself
  as a professional tax service. It is an educational prototype.

## Internal Governance Policies

- **Data Protection:** No real PII or tax data stored
- **Ethical AI:** Guardrails prevent off-topic and advice-giving
- **Transparency:** Users are informed it's a prototype, not a professional service

## Disclaimer

The system displays a clear disclaimer:

> "This is an educational prototype for a hackathon challenge. It is not a
> professional tax preparation service and does not provide tax advice.
> The generated form is for demonstration purposes only. Please consult
> a qualified tax professional for your actual tax filing."

# 19. Architecture Position

## System Authority

The system has **bounded authority**:
- **Data Collection:** LLM orchestrates the conversation but is bounded by the
  state machine and guardrails.
- **Computation:** Deterministic tax computation tools perform calculations
  with mathematical accuracy.
- **Output:** Users review the form before download; they are responsible
  for its accuracy.

## AI Role

The AI serves as a **conversational orchestrator**:
- It guides the user through the data collection process.
- It interprets user inputs and adapts the conversation.
- It calls tools at the appropriate time.
- It does NOT make autonomous decisions about computation or output.

## Trust Boundary

| Boundary | Allowed | Forbidden |
|----------|---------|-----------|
| User Input | W-2 data, filing status, dependency status | Off-topic questions, tax advice requests |
| LLM Output | Friendly conversation, guided questions | Computation, form filling, advice |
| Tool Output | Validated data structures, generated PDF | Unvalidated or malformed data |
| System Output | Filled 1040 PDF | Any other tax form or advice |

## Failure Philosophy

**Fail gracefully, fail observably:**
- When an error occurs, the user is informed with a friendly message.
- The error is logged with full context.
- The system remains stable and can be restarted.
- No data is lost or corrupted.

# 20. Final Engineering Position

This system is designed according to:
- **MoniGarr Operating Model (M.O.M.):** Human accountability first,
  ancient + human + artificial intelligence integration, enterprise from
  day one, documentation as infrastructure, handoff-ready engineering.
- **MoniGarr Intelligence-Led Engineering (M.I.L.E.):** Intelligence-led
  decisions, verification before output, bounded data access,
  observability-first, additive integration.
- **Echelon Enterprise Engineering standards:** Security, privacy,
  stability, reliability, performance, accessibility, observability,
  maintainability, scalability, portability, disaster recovery.

The system prioritizes:
- **Human accountability:** Users review their form, judges evaluate the system
- **Sovereign engineering:** Clear ownership, documentation, and handoff
- **Operational continuity:** Deployed and working end-to-end
- **Enterprise reliability:** Tested, verified, and observable
- **Scalable intelligence orchestration:** LLM orchestrates conversation
- **Long-term maintainability:** Clean architecture, comprehensive docs

**AI accelerates engineering.**

**Humans remain accountable.**

**Systems remain governable.**

---

# 21. Document Control

- **Owner:** Monica Peters, monigarr@monigarr.com
- **Version:** 1.0.0 (Final)
- **Created:** 2026-06-24
- **Last Updated:** 2026-06-24
- **Reviewers:** Hackathon Judges
- **Approval:** Monica Peters
- **Distribution:** Public (GitHub)
- **Classification:** Internal/Educational

---

# 22. Appendices

## A. Directory Structure

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
│   ├── ARCHITECTURE.md         # This document
│   ├── DECISIONS.md            # Design decisions
│   └── API.md                  # API documentation
├── .env.example                # Example environment variables
├── .gitignore
├── render.yaml
├── requirements.txt
├── README.md
└── LICENSE
```

## B. Key Technologies

| Component | Technology | Justification |
|-----------|------------|---------------|
| **Web Framework** | FastAPI | Async support, auto-docs, lightweight |
| **LLM Provider** | OpenAI GPT-4o-mini | Good balance of cost and quality |
| **LLM Orchestration** | LangChain or Direct API | Simplicity vs. flexibility tradeoff |
| **PDF Generation** | PyPDF2/PyMuPDF | Fill existing PDF forms |
| **Frontend** | Vanilla HTML/CSS/JS | Minimal, accessible, no framework needed |
| **Deployment** | Render | Free tier, easy deployment |
| **Testing** | Pytest | Standard, simple |
| **Environment** | Python 3.10+ | Modern, widely supported |

## C. Decision Log

| Decision | Alternative | Rationale | Impact |
|----------|-------------|-----------|--------|
| Use OpenAI | Local model | Reliability, quality | API cost, internet dependency |
| In-memory state | Redis | Simplicity | Limited scalability |
| 5 questions | 10 questions | Constraint from spec | Forces tight conversation design |
| Single W-2 | Multiple W-2s | Simplicity | Limited tax scope |
| Vanilla frontend | React/Next.js | Focus on backend | Less polished UI |
| Fillable PDF | Generate from scratch | Simplicity | Limited formatting flexibility |

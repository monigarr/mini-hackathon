# Build Plan: Agentic Tax-Filing Assistant
## Complete Implementation Roadmap

> **Project:** Agentic Tax-Filing Assistant for Form 1040  
> **Deadline:** June 24, 2026 (Hackathon)  
> **Owner:** Monica Peters  
> **Version:** 1.0.0  
> **Last Updated:** 2026-06-24

---

## 📊 Executive Summary

This is a **10-phase implementation plan** to deliver a fully functional agentic tax-filing system that meets all requirements in the CLIENT_REQUEST, PRD, and README.

**Key Metrics:**
- **4 Pillars Required:** Chat Loop ✓ Tools ✓ Guardrails ✓ Observation ✓
- **5-Question Budget:** Hard limit enforced
- **End-to-End Flow:** W-2 input → 5 questions → Completed 1040 download
- **Deployment:** Public URL on Render
- **Quality Gates:** Unit tests (80%+), integration tests (happy path), manual e2e test

---

## 🏗️ Phase Overview

| Phase | Name | Duration | Status | Deliverable |
|-------|------|----------|--------|------------|
| 0 | Foundation & Setup | 2h | ✅ COMPLETE | Project structure, git, customization stack |
| 1 | Core Architecture | 4h | ⏳ NEXT | FastAPI app, session management, state machine |
| 2 | Conversation Engine | 4h | ⏸️ BLOCKED | Prompts, orchestration, question flow |
| 3 | W-2 Validation | 3h | ⏸️ BLOCKED | Input parsing, validation logic, error recovery |
| 4 | Tax Computation | 3h | ⏸️ BLOCKED | 2025 tax tables, standard deduction, calculations |
| 5 | PDF Generation | 3h | ⏸️ BLOCKED | Form population, field mapping, download |
| 6 | Tool Integration | 2h | ⏸️ BLOCKED | LLM tool definitions, response parsing |
| 7 | Guardrails & Safety | 3h | ⏸️ BLOCKED | Question budget, off-topic, validation |
| 8 | Observability | 2h | ⏸️ BLOCKED | Logging, structured JSON, audit trails |
| 9 | Testing & QA | 4h | ⏸️ BLOCKED | Unit tests, integration tests, edge cases |
| 10 | Deployment & Polish | 2h | ⏸️ BLOCKED | Render, CI/CD, final validation |
| **TOTAL** | | **32 hours** | | **Production-Ready System** |

---

## 🎯 Detailed Phase Plan

### **PHASE 0: Foundation & Setup** ✅ COMPLETE
**Status:** Done  
**Time Spent:** 2h  
**Deliverables:**
- ✅ Git repos (GitLab origin + GitHub mirror)
- ✅ `.instructions.md` (master constraints)
- ✅ `skill-tax-filing-orchestration.md` (conversation patterns)
- ✅ `TaxAssistant-Coder.agent.md` (implementation partner)
- ✅ Project structure scaffold

**Exit Criteria Met:**
- [x] All constraints documented
- [x] Code patterns established
- [x] Git ready for collaboration

---

### **PHASE 1: Core Architecture** ⏳ NEXT
**Estimated Time:** 4 hours  
**Goal:** FastAPI skeleton with session management and state machine

**Dependencies:** Phase 0 complete

**Tasks:**

#### 1.1 FastAPI Application Scaffold
**File:** `src/main.py`  
**Requirements:**
- [ ] FastAPI app initialization with CORS
- [ ] Health check endpoint (`/health`)
- [ ] Chat endpoint (`POST /api/chat`)
- [ ] Static file serving (HTML/CSS/JS)
- [ ] Error handling middleware
- [ ] Environment config loading

**Code Template:**
```python
# ============================================================================
# Module: main.py
# Purpose: FastAPI application entry point for tax filing assistant
# ============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agentic Tax-Filing Assistant",
    version="1.0.0",
    description="Help W-2 earners file Form 1040"
)

# CORS for web chat
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="src/ui/static"), name="static")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/chat")
async def chat(session_id: str, user_message: str):
    """Process user message and return agent response."""
    # Implementation in Phase 2
    pass

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

#### 1.2 Data Models
**File:** `src/models/tax_data.py`  
**Requirements:**
- [ ] `TaxData` dataclass (wages, withholding, filing status, dependency)
- [ ] `Session` dataclass (session_id, created_at, messages, collected_data)
- [ ] Type validation in `__post_init__`

**Schema:**
```python
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class W2Data:
    box1_wages: float
    box2_federal_withheld: float
    box4_ss_wages: float
    box6_medicare_wages: float
    
    def __post_init__(self):
        assert self.box1_wages >= 0, "Wages must be non-negative"
        assert self.box2_federal_withheld >= 0, "Withholding must be non-negative"

@dataclass
class TaxData:
    w2: W2Data
    filing_status: str  # "Single" or "MFJ"
    is_dependent: bool
    name: Optional[str] = None
    
    def __post_init__(self):
        assert self.filing_status in ["Single", "MFJ"], "Invalid filing status"

@dataclass
class ConversationMessage:
    role: str  # "user" or "agent"
    content: str
    timestamp: datetime

@dataclass
class ConversationSession:
    session_id: str
    created_at: datetime
    messages: List[ConversationMessage]
    tax_data: Optional[TaxData] = None
    question_count: int = 0
```

#### 1.3 State Machine
**File:** `src/conversation/state_machine.py`  
**Requirements:**
- [ ] 7-state enum (START, W2_PROMPT, W2_VALIDATE, FILING, DEPENDENCY, CONFIRMATION, FORM_GENERATION, COMPLETE)
- [ ] State transition logic with question counter
- [ ] Validation of state transitions
- [ ] Question budget enforcement

**States:**
```
START → W2_PROMPT → W2_VALIDATE → FILING → DEPENDENCY → CONFIRMATION → FORM_GENERATION → COMPLETE
  ↑                      ↓ (if invalid)
  └──────────────────────┘
```

#### 1.4 Session Manager
**File:** `src/models/session.py`  
**Requirements:**
- [ ] In-memory session storage (dict keyed by session_id)
- [ ] Create session
- [ ] Get session
- [ ] Update session
- [ ] Clear session (after completion)

**Methods:**
```python
class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, ConversationSession] = {}
    
    def create_session(self) -> str:
        """Create new session, return session_id"""
        
    def get_session(self, session_id: str) -> ConversationSession:
        """Retrieve session or raise 404"""
        
    def update_session(self, session_id: str, session: ConversationSession):
        """Update session in-memory storage"""
        
    def delete_session(self, session_id: str):
        """Clear session after completion"""
```

#### 1.5 Web Chat UI
**Files:** `src/ui/static/index.html`, `style.css`, `app.js`  
**Requirements:**
- [ ] Simple HTML chat interface
- [ ] Message display (user left, agent right)
- [ ] Input box + send button
- [ ] Session ID management (stored in localStorage)
- [ ] Minimal styling (no design polish needed)

**Features:**
- Display conversation messages with timestamps
- Auto-scroll to latest message
- Disable input while waiting for response
- Show loading indicator
- Download button for completed form (Phase 5)

#### 1.6 Configuration & Logging
**File:** `src/utils/config.py`  
**Requirements:**
- [ ] Load environment variables (OPENAI_API_KEY, ENVIRONMENT, PORT)
- [ ] Validate required vars
- [ ] Set up Python logging with JSON formatter

**Exit Criteria:**
- [ ] `uvicorn src.main:app --reload` starts without errors
- [ ] Health check endpoint returns 200
- [ ] Web chat UI loads at `http://localhost:8000`
- [ ] Session manager creates/retrieves sessions
- [ ] All code has type hints and docstrings

**Testing:**
- [ ] Unit test: SessionManager (create, get, update)
- [ ] Unit test: State machine transitions
- [ ] Integration test: POST to `/api/chat` returns response

---

### **PHASE 2: Conversation Engine**
**Estimated Time:** 4 hours  
**Goal:** LLM orchestration, prompts, question flow

**Dependencies:** Phase 1 complete

**Tasks:**

#### 2.1 OpenAI Integration
**File:** `src/tools/llm.py`  
**Requirements:**
- [ ] Async function `call_llm(system_prompt, user_message) -> str`
- [ ] Error handling (API failures, rate limits)
- [ ] Token counting (for observability)
- [ ] Timeout handling (< 2 seconds target)

#### 2.2 System Prompts
**File:** `src/conversation/prompts.py`  
**Requirements:**
- [ ] System prompt template (core persona)
- [ ] State-specific prompts (7 states × 1 prompt each)
- [ ] Warm tone enforcement
- [ ] 5-question constraint reminder
- [ ] Tax computation output format

**Example System Prompt:**
```
You are TaxGuide, a warm, helpful tax filing assistant for the Agentic 
Tax-Filing Assistant. Your job is to help W-2 earners file a 2025 Form 1040 
through a friendly, guided 5-question conversation.

[Core constraints...]
[Current state context...]
[Expected output format...]

Never provide tax advice. Never ask more than 5 questions total. Always be warm 
and human-like. Confirm data back to the user before proceeding.
```

#### 2.3 Conversation Engine
**File:** `src/conversation/engine.py`  
**Requirements:**
- [ ] Class `ConversationEngine` with method `process_message(session, user_message) -> str`
- [ ] State machine integration
- [ ] Prompt building based on state
- [ ] Tool call detection and routing
- [ ] Response parsing

**Flow:**
```
User Input
  ↓
[Validate & Parse]
  ↓
[Update State Machine]
  ↓
[Check Question Budget]
  ↓
[Build Prompt with Context]
  ↓
[Call OpenAI LLM]
  ↓
[Parse Response]
  ↓
[Execute Tools if Needed]
  ↓
[Log Observation]
  ↓
Response to User
```

#### 2.4 Prompt Templates (All 7 States)
**File:** `src/conversation/prompts.py`  
**Requirements:**
- [ ] START: Greeting, explain process
- [ ] W2_PROMPT: Ask for Box 1, 2
- [ ] FILING: Ask filing status (Single/MFJ)
- [ ] DEPENDENCY: Ask if dependent
- [ ] CONFIRMATION: Summarize, ask confirm
- [ ] FORM_GENERATION: (Agent doesn't ask; just generates)
- [ ] COMPLETE: Provide download link

**Exit Criteria:**
- [ ] `/api/chat` endpoint processes messages end-to-end
- [ ] State transitions happen correctly
- [ ] Questions are warm and human-like
- [ ] LLM responses stay within constraints
- [ ] Question counter increments
- [ ] All responses logged

**Testing:**
- [ ] Unit test: Prompt building for each state
- [ ] Integration test: Full conversation flow (5 turns)
- [ ] Mock test: LLM response parsing

---

### **PHASE 3: W-2 Validation**
**Estimated Time:** 3 hours  
**Goal:** Deterministic W-2 data validation

**Dependencies:** Phase 1 complete, Phase 2 in progress

**Tasks:**

#### 3.1 W-2 Validator Tool
**File:** `src/tools/validate_w2.py`  
**Requirements:**
- [ ] Function `validate_w2_box1(value: str) -> (bool, str, float)`
- [ ] Function `validate_w2_box2(box1: float, box2: str) -> (bool, str, float)`
- [ ] Function `validate_w2(box1, box2, box4, box6) -> (bool, str, W2Data)`
- [ ] Clear error messages for user

**Validation Rules:**
- Box 1 (wages): positive number, typically $10k-$100k range
- Box 2 (withholding): 0 ≤ Box2 ≤ Box1
- Box 4 (SS): typically equals Box 1 (warn if different)
- Box 6 (Medicare): typically equals Box 1 (warn if different)
- All values must be parseable as floats (handle commas, $ signs)

**Error Recovery:**
```python
def validate_w2_box1(value: str) -> tuple[bool, str, Optional[float]]:
    """
    Returns: (success, user_message, parsed_value)
    """
    try:
        # Clean input
        clean = value.replace(',', '').replace('$', '').strip()
        wages = float(clean)
        
        # Validate
        if wages < 0:
            return False, "Wages must be a positive number. Can you check your W-2?", None
        if wages == 0:
            return False, "Wages can't be zero. Is that right?", None
        if wages < 5000 or wages > 500000:
            return False, f"${wages:,.2f} seems unusual. Double-check your W-2?", None
        
        return True, None, wages
    except ValueError:
        return False, "I couldn't understand that number. Can you try again?", None
```

#### 3.2 W-2 Input Extraction
**File:** `src/tools/validate_w2.py` (continued)  
**Requirements:**
- [ ] Parse natural language W-2 input (LLM extracts, we validate)
- [ ] Handle partial data (ask for missing fields)
- [ ] Support file upload fallback (optional stretch)

#### 3.3 Error Recovery Flow
**Requirements:**
- [ ] If validation fails, ask user to re-enter specific field
- [ ] Do NOT increment question count (clarification, not new question)
- [ ] Stay in W2_PROMPT state until valid

**Exit Criteria:**
- [ ] `validate_w2()` correctly validates all scenarios
- [ ] Error messages are friendly and actionable
- [ ] Test data passes validation
- [ ] Invalid data rejected with guidance

**Testing:**
- [ ] Unit test: validate_w2_box1 (valid, invalid, boundary)
- [ ] Unit test: validate_w2_box2 (valid, exceeds wages)
- [ ] Integration test: User enters bad data, recovers correctly

---

### **PHASE 4: Tax Computation**
**Estimated Time:** 3 hours  
**Goal:** Accurate 2025 tax calculations

**Dependencies:** Phase 1 complete

**Tasks:**

#### 4.1 2025 Tax Tables & Rules
**File:** `src/utils/tax_tables.py`  
**Requirements:**
- [ ] Standard deduction amounts (Single, MFJ, Dependent)
- [ ] 2025 tax brackets and rates
- [ ] Helper functions for computation

**2025 IRS Data:**
```python
STANDARD_DEDUCTION_2025 = {
    "Single": 14600,
    "MFJ": 29200,
    "Dependent": 14150,  # Lesser of earned income + $450
}

TAX_BRACKETS_2025 = [
    # (upper_limit, rate)
    (11600, 0.10),      # 10% up to $11,600
    (47150, 0.12),      # 12% from $11,601 to $47,150
    (100525, 0.22),     # 22% from $47,151 to $100,525
    # ... etc
]
```

#### 4.2 Tax Computation Function
**File:** `src/utils/tax_tables.py` (continued)  
**Requirements:**
- [ ] Function `compute_tax(wages: float, filing_status: str, is_dependent: bool) -> float`
- [ ] Returns federal income tax liability (not withholding)
- [ ] Handles all scenarios (Single, MFJ, Dependent)

**Formula:**
```
Taxable Income = max(0, Wages - Standard Deduction)
Tax = Apply brackets to Taxable Income
Refund/Owed = Federal Withholding - Tax
```

#### 4.3 Form Field Computation
**File:** `src/utils/tax_tables.py` (continued)  
**Requirements:**
- [ ] Function `compute_form_values(w2: W2Data, filing_status: str, is_dependent: bool) -> dict`
- [ ] Returns dict with all Form 1040 line items
- [ ] Examples:
  - Line 1a (filing status)
  - Line 1d (total income)
  - Line 12 (federal withholding)
  - Line 15 (standard deduction)
  - Line 16 (taxable income)
  - Line 24 (total tax)
  - Line 33 (refund or amount owed)

**Exit Criteria:**
- [ ] `compute_tax()` returns correct values for test cases
- [ ] All three scenarios tested (Single, MFJ, Dependent)
- [ ] Math verified against IRS Form 1040 instructions
- [ ] No hardcoded values except tax brackets

**Testing:**
- [ ] Unit test: Single filer, $40k wages, $2.4k withheld → correct tax
- [ ] Unit test: MFJ filer → correct standard deduction applied
- [ ] Unit test: Dependent → correct standard deduction applied
- [ ] Unit test: compute_form_values() returns all required fields

**Test Case (Single Filer):**
```
Wages: $40,000
Withholding: $2,400
Filing Status: Single
Dependent: No

Expected:
- Standard Deduction: $14,600
- Taxable Income: $25,400
- Tax (2025 brackets): ~$3,054
- Refund: $2,400 - $3,054 = (-$654) [owes $654]
```

---

### **PHASE 5: PDF Generation**
**Estimated Time:** 3 hours  
**Goal:** Populate 2025 Form 1040 PDF with computed values

**Dependencies:** Phase 4 complete

**Tasks:**

#### 5.1 PDF Field Mapping
**File:** `src/utils/pdf_utils.py`  
**Requirements:**
- [ ] Inspect Form 1040 template PDF for field names
- [ ] Create mapping dict: `form_field_name → (line_number, field_type)`
- [ ] Field types: text, radio (Single/MFJ), checkbox

**Field Mapping Example:**
```python
FORM_1040_FIELDS = {
    "filing_status_single": ("1a", "radio"),
    "filing_status_mfj": ("1a", "radio"),
    "total_income": ("1d", "text"),
    "federal_withholding": ("12", "text"),
    "standard_deduction": ("15", "text"),
    "taxable_income": ("16", "text"),
    "total_tax": ("24", "text"),
    "refund_amount": ("33a", "text"),
    "amount_owed": ("33b", "text"),
}
```

#### 5.2 PDF Population Function
**File:** `src/tools/generate_1040.py`  
**Requirements:**
- [ ] Function `generate_1040(form_values: dict) -> bytes`
- [ ] Load template PDF
- [ ] Populate fields with computed values
- [ ] Save to bytes (in-memory)
- [ ] Return PDF bytes for download

**Implementation:**
```python
from PyPDF2 import PdfReader, PdfWriter

def generate_1040(form_values: dict) -> bytes:
    """
    Generate completed 2025 Form 1040 PDF.
    
    Args:
        form_values: dict with all form line items
    
    Returns:
        bytes: completed PDF in memory
    """
    # Load template
    reader = PdfReader("data/form_1040_template.pdf")
    writer = PdfWriter()
    
    # Copy pages
    for page in reader.pages:
        writer.add_page(page)
    
    # Populate fields (pseudo-code)
    # writer.update_page_form_field_values(...)
    
    # Write to bytes
    output = BytesIO()
    writer.write(output)
    return output.getvalue()
```

#### 5.3 Tool Definition for LLM
**File:** `src/conversation/engine.py`  
**Requirements:**
- [ ] Define `generate_1040` as tool the LLM can call
- [ ] Tool takes collected tax data as input
- [ ] Returns success/failure + download URL or error

**Tool Schema (for LLM):**
```json
{
  "name": "generate_1040",
  "description": "Generate completed Form 1040 PDF",
  "parameters": {
    "type": "object",
    "properties": {
      "wages": {"type": "number"},
      "federal_withholding": {"type": "number"},
      "filing_status": {"type": "string"},
      "is_dependent": {"type": "boolean"}
    },
    "required": ["wages", "federal_withholding", "filing_status"]
  }
}
```

#### 5.4 Download Endpoint
**File:** `src/main.py`  
**Requirements:**
- [ ] Endpoint `GET /api/download/{session_id}`
- [ ] Return PDF file with correct headers
- [ ] Filename: `Form_1040_{session_id}.pdf`

**Exit Criteria:**
- [ ] PDF field mapping complete and verified
- [ ] `generate_1040()` produces valid PDF
- [ ] Download endpoint returns PDF file
- [ ] PDF is readable and can be opened in PDF reader

**Testing:**
- [ ] Unit test: generate_1040() with test data
- [ ] Integration test: User completes conversation, receives PDF
- [ ] Manual test: Download PDF, open in Adobe Reader, verify values populated

---

### **PHASE 6: Tool Integration**
**Estimated Time:** 2 hours  
**Goal:** Wire tools into conversation engine

**Dependencies:** Phase 2, 3, 4, 5 complete

**Tasks:**

#### 6.1 Tool Definitions for LLM
**File:** `src/conversation/engine.py`  
**Requirements:**
- [ ] Define 3 tools in OpenAI format:
  1. `validate_w2` - Validate W-2 data
  2. `generate_1040` - Generate completed form
  3. `log_observation` - Log agent decisions

#### 6.2 Tool Call Detection
**File:** `src/conversation/engine.py`  
**Requirements:**
- [ ] Parse LLM response for tool calls
- [ ] Execute tool
- [ ] Return result to LLM
- [ ] Continue conversation

#### 6.3 Tool Execution
**File:** `src/conversation/engine.py`  
**Requirements:**
- [ ] Validate tool inputs
- [ ] Call appropriate tool function
- [ ] Handle tool failures gracefully
- [ ] Log all tool calls

**Example Tool Execution:**
```python
def execute_tool(tool_name: str, tool_input: dict) -> dict:
    if tool_name == "validate_w2":
        return validate_w2(**tool_input)
    elif tool_name == "generate_1040":
        return generate_1040(**tool_input)
    else:
        return {"error": f"Unknown tool: {tool_name}"}
```

**Exit Criteria:**
- [ ] LLM can call tools via conversation
- [ ] Tool results are returned to LLM
- [ ] All tool calls are logged
- [ ] Conversation flows naturally with tools

**Testing:**
- [ ] Integration test: LLM detects and calls validate_w2
- [ ] Integration test: LLM detects and calls generate_1040
- [ ] Integration test: Tool failures don't crash agent

---

### **PHASE 7: Guardrails & Safety**
**Estimated Time:** 3 hours  
**Goal:** Enforce constraints, prevent off-topic, validate inputs

**Dependencies:** Phase 1-6 complete

**Tasks:**

#### 7.1 Question Budget Enforcer
**File:** `src/conversation/state_machine.py`  
**Requirements:**
- [ ] Track question count per session
- [ ] Prevent asking 6th question
- [ ] Force completion after 5th question
- [ ] Log question count at each step

**Implementation:**
```python
class QuestionBudgetEnforcer:
    MAX_QUESTIONS = 5
    
    @staticmethod
    def should_ask_question(session: ConversationSession) -> bool:
        return session.question_count < QuestionBudgetEnforcer.MAX_QUESTIONS
    
    @staticmethod
    def increment_and_check(session: ConversationSession) -> bool:
        """Increment count, return True if still under budget."""
        session.question_count += 1
        return session.question_count <= QuestionBudgetEnforcer.MAX_QUESTIONS
```

#### 7.2 Off-Topic Prevention
**File:** `src/conversation/prompts.py`  
**Requirements:**
- [ ] System prompt forbids tax advice
- [ ] System prompt forbids discussing out-of-scope topics
- [ ] Test with examples (e.g., "Should I do a 401k?" → redirect)

**System Prompt Constraint:**
```
CRITICAL GUARDRAILS:
- Do NOT provide tax advice, tax planning, or tax optimization strategies
- Do NOT discuss complex scenarios (self-employment, rentals, capital gains)
- Do NOT answer off-topic questions (sports, weather, etc.)
- If user asks off-topic, politely redirect: 
  "That's a great question, but it's outside my scope. Let's focus on 
   filing your 1040. [Continue with next step]"
```

#### 7.3 Input Validation
**File:** `src/tools/validate_w2.py`  
**Requirements:**
- [ ] All W-2 data validated before use
- [ ] Clear error messages guide user
- [ ] No negative numbers
- [ ] No extreme outliers accepted without confirmation
- [ ] Type conversion with safety

#### 7.4 Guardrail Testing
**Requirements:**
- [ ] Test: Agent rejects 6th question attempt
- [ ] Test: Agent redirects off-topic question
- [ ] Test: Agent rejects invalid W-2 data
- [ ] Test: Agent recovers from validation failure

**Exit Criteria:**
- [ ] Question budget is hard-enforced
- [ ] Off-topic questions are handled
- [ ] Invalid inputs are rejected with guidance
- [ ] All guardrails logged for audit

**Testing:**
- [ ] Unit test: QuestionBudgetEnforcer
- [ ] Integration test: 5 questions max
- [ ] Integration test: 6th question triggers completion
- [ ] Integration test: Off-topic question redirected
- [ ] Integration test: Invalid W-2 rejected

---

### **PHASE 8: Observability & Logging**
**Estimated Time:** 2 hours  
**Goal:** Structured JSON logging of all agent decisions

**Dependencies:** Phase 1-7 complete

**Tasks:**

#### 8.1 Logging Infrastructure
**File:** `src/tools/logger.py`  
**Requirements:**
- [ ] Structured JSON logging
- [ ] Function `log_observation(event_type: str, data: dict)`
- [ ] Timestamp, session_id, event_type, event_data
- [ ] Write to stdout + optional file

**Log Example:**
```json
{
  "timestamp": "2026-06-24T10:00:00Z",
  "session_id": "abc123xyz",
  "event_type": "agent_response",
  "question_number": 1,
  "agent_message": "Hi! I'd love to help...",
  "state": "W2_PROMPT"
}
```

#### 8.2 Logging Points
**File:** All modules  
**Requirements:**
- [ ] Log at every state transition
- [ ] Log every LLM call (prompt summary, response summary)
- [ ] Log every tool call (name, input, output)
- [ ] Log every validation (pass/fail)
- [ ] Log every error
- [ ] Log session start/end

**Logging Checklist:**
```python
# At start of each turn:
log_observation("user_input_received", {
    "session_id": session_id,
    "state": current_state,
    "question_count": question_count,
    "user_message": user_message[:100]
})

# Before LLM call:
log_observation("llm_call_initiated", {
    "session_id": session_id,
    "model": "gpt-4o-mini",
    "question_count": question_count
})

# After LLM response:
log_observation("llm_response_received", {
    "session_id": session_id,
    "response": agent_response,
    "latency_ms": elapsed_time
})

# Before tool call:
log_observation("tool_call_initiated", {
    "session_id": session_id,
    "tool_name": tool_name,
    "input": tool_input
})

# After tool execution:
log_observation("tool_execution_completed", {
    "session_id": session_id,
    "tool_name": tool_name,
    "success": success,
    "output": tool_output
})

# State transition:
log_observation("state_transition", {
    "session_id": session_id,
    "from": old_state,
    "to": new_state,
    "question_count": question_count
})
```

#### 8.3 Audit Trail
**File:** `src/tools/logger.py` (continued)  
**Requirements:**
- [ ] All logs indexed by session_id
- [ ] Judge can trace full conversation flow
- [ ] All decisions visible and traceable

**Exit Criteria:**
- [ ] All critical points logged
- [ ] Logs are readable and structured
- [ ] Judge can understand agent decisions from logs
- [ ] Performance metrics are captured

**Testing:**
- [ ] Integration test: Run full conversation, verify all events logged
- [ ] Manual test: Read logs, trace conversation flow

---

### **PHASE 9: Testing & Quality Assurance**
**Estimated Time:** 4 hours  
**Goal:** Comprehensive test coverage, edge cases, manual verification

**Dependencies:** Phase 1-8 complete

**Tasks:**

#### 9.1 Unit Tests
**Files:** `tests/test_*.py`  
**Requirements:**
- [ ] Test all core functions
- [ ] Minimum 80% code coverage for tax logic
- [ ] Target: 90% overall

**Test File Structure:**
```
tests/
├── test_tax_computation.py      # Tax math
├── test_validation.py            # W-2 validation
├── test_state_machine.py         # State transitions
├── test_pdf_generation.py        # PDF population
├── test_conversation.py          # Message flow
└── conftest.py                   # Fixtures
```

**Test Categories:**

**A. Tax Computation Tests:**
```python
# test_tax_computation.py
def test_single_filer_tax():
    """Single filer, $40k wages, $2.4k withheld."""
    wages = 40000.0
    tax = compute_tax(wages, "Single", False)
    assert tax == pytest.approx(3054.0, abs=1.0)

def test_married_filing_jointly():
    """MFJ filer with higher standard deduction."""
    wages = 40000.0
    tax = compute_tax(wages, "MFJ", False)
    assert tax < compute_tax(wages, "Single", False)

def test_dependent_lower_std_ded():
    """Dependent gets lower standard deduction."""
    wages = 20000.0
    std_ded_independent = compute_std_deduction("Single", False)
    std_ded_dependent = compute_std_deduction("Single", True)
    assert std_ded_dependent < std_ded_independent
```

**B. Validation Tests:**
```python
# test_validation.py
def test_valid_w2_wages():
    """Valid wage amount."""
    success, msg, value = validate_w2_box1("40000")
    assert success
    assert value == 40000.0

def test_negative_wages_rejected():
    """Negative wages rejected."""
    success, msg, value = validate_w2_box1("-100")
    assert not success

def test_withholding_exceeds_wages():
    """Withholding cannot exceed wages."""
    success, msg = validate_w2_box2(40000, "50000")
    assert not success

def test_cleanup_formatting():
    """Accept wages with commas and dollar signs."""
    success, msg, value = validate_w2_box1("$40,000.00")
    assert success
    assert value == 40000.0
```

**C. State Machine Tests:**
```python
# test_state_machine.py
def test_state_transitions():
    """Verify state transitions flow correctly."""
    session = ConversationSession(...)
    sm = StateMachine(session)
    
    sm.transition(START, W2_PROMPT)
    assert sm.current_state == W2_PROMPT
    assert session.question_count == 1

def test_question_budget_enforcement():
    """5-question budget is enforced."""
    for i in range(5):
        sm.increment_question_count()
    
    with pytest.raises(ValueError):
        sm.increment_question_count()
```

**D. PDF Generation Tests:**
```python
# test_pdf_generation.py
def test_generate_1040_valid():
    """Generate PDF from valid form values."""
    form_values = {
        "filing_status": "Single",
        "wages": 40000.0,
        ...
    }
    pdf_bytes = generate_1040(form_values)
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b"%PDF")  # PDF magic bytes

def test_pdf_fields_populated():
    """Verify PDF fields are actually populated."""
    # Manual inspection step: open PDF, verify values
    pass
```

#### 9.2 Integration Tests
**File:** `tests/test_end_to_end.py`  
**Requirements:**
- [ ] Full conversation flow (happy path)
- [ ] All three scenarios (Single, MFJ, Dependent)
- [ ] Error recovery flows

**Happy Path Test:**
```python
# test_end_to_end.py
def test_single_filer_happy_path():
    """Complete conversation: Single filer → completed 1040."""
    # Setup
    session = create_test_session()
    engine = ConversationEngine()
    
    # Turn 1: User provides W-2
    response = engine.process_message(session, "My W-2 shows $40,000 wages and $2,400 withheld")
    assert "confirm" in response.lower()
    
    # Turn 2: User confirms filing status
    response = engine.process_message(session, "I'm single")
    assert session.tax_data.filing_status == "Single"
    
    # Turn 3: User confirms dependency
    response = engine.process_message(session, "I'm independent")
    assert not session.tax_data.is_dependent
    
    # Turn 4: User confirms all data
    response = engine.process_message(session, "Yes, that's all correct")
    assert "form" in response.lower() or "generate" in response.lower()
    
    # Turn 5: Form generated
    assert session.current_state == "COMPLETE"
    assert session.pdf_url is not None
```

#### 9.3 Edge Case Tests
**File:** `tests/test_edge_cases.py`  
**Requirements:**
- [ ] Invalid inputs (negative, zero, extreme)
- [ ] Missing data (user skips input)
- [ ] Off-topic questions
- [ ] Timeout scenarios
- [ ] API failures

**Edge Case Examples:**
```python
def test_zero_wages_rejected():
    """$0 wages rejected with guidance."""
    success, msg, value = validate_w2_box1("0")
    assert not success
    assert "zero" in msg.lower()

def test_extreme_wage_amount():
    """Very high wages trigger warning."""
    success, msg, value = validate_w2_box1("1000000")
    # Should accept but maybe with warning
    assert success or "unusual" in msg.lower()

def test_off_topic_question_redirected():
    """Agent redirects off-topic question."""
    session = create_test_session()
    engine = ConversationEngine()
    response = engine.process_message(session, "What's the weather?")
    assert "off-topic" in response.lower() or "help you file" in response.lower()

def test_missing_w2_field():
    """If user skips providing withholding."""
    session = create_test_session()
    engine = ConversationEngine()
    response = engine.process_message(session, "My wages are $40,000")
    # Agent should ask for withholding
    assert "withhold" in response.lower() or "box 2" in response.lower()
```

#### 9.4 Manual Testing Checklist
**Requirements:**
- [ ] Run app locally with sample data
- [ ] Test all three scenarios manually (Single, MFJ, Dependent)
- [ ] Download PDF, verify it opens and values are correct
- [ ] Check web UI renders properly
- [ ] Verify logs show complete conversation flow

**Manual Test Script:**
```bash
# Start app
OPENAI_API_KEY=sk-... uvicorn src.main:app --reload

# Visit http://localhost:8000
# Scenario 1: Single filer
  - W-2: $40,000 wages, $2,400 withholding
  - Filing: Single
  - Dependent: No
  - Download PDF, verify

# Scenario 2: Married filing jointly
  - W-2: $40,000 wages, $2,400 withholding
  - Filing: Married Filing Jointly
  - Dependent: No
  - Download PDF, verify

# Scenario 3: Can be claimed as dependent
  - W-2: $20,000 wages, $500 withholding
  - Filing: Single
  - Dependent: Yes
  - Download PDF, verify
```

**Exit Criteria:**
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Coverage >= 80%
- [ ] Manual testing successful (all 3 scenarios)
- [ ] PDFs generated and verified
- [ ] Logs complete and readable

---

### **PHASE 10: Deployment & Polish**
**Estimated Time:** 2 hours  
**Goal:** Deploy to Render, final validation, documentation

**Dependencies:** Phase 1-9 complete

**Tasks:**

#### 10.1 Render Deployment
**Requirements:**
- [ ] Create Render account (free tier)
- [ ] Create new Web Service
- [ ] Connect GitHub repository
- [ ] Configure environment variables (OPENAI_API_KEY)
- [ ] Deploy

**Render Configuration:**
```yaml
# render.yaml
services:
  - type: web
    name: agentic-tax-assistant
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        scope: build,run
        sync: false
      - key: ENVIRONMENT
        value: production
```

#### 10.2 Environment Configuration
**File:** `.env.example` + `.env` (gitignored)  
**Requirements:**
- [ ] `.env.example` with all required vars (no secrets)
- [ ] `.env` with actual values (gitignored)
- [ ] Config loader validates all vars present

**`.env.example`:**
```
OPENAI_API_KEY=sk-your-key-here
ENVIRONMENT=production
PORT=8000
```

#### 10.3 Final Validation
**Requirements:**
- [ ] Deploy to Render
- [ ] Test public URL (chat, conversation, download)
- [ ] Verify all 4 pillars visible in running system
- [ ] Check logs are being generated

**Validation Checklist:**
- [ ] `/health` endpoint returns 200
- [ ] Web chat loads and is responsive
- [ ] Can complete full conversation
- [ ] PDF downloads successfully
- [ ] Logs are structured JSON and readable
- [ ] Question budget is enforced
- [ ] Tax computation is correct

#### 10.4 Documentation
**Requirements:**
- [ ] Update README with deployment URL
- [ ] Create DECISIONS.md (design choices)
- [ ] Ensure all code has docstrings
- [ ] One-command local run instructions

**DECISIONS.md (template):**
```markdown
# Design Decisions

## 1. LLM Provider: OpenAI GPT-4o-mini
**Why:** Cost-effective ($0.01-0.02 per conversation), high quality, 
reliable for conversation tasks, excellent tool support.

## 2. State Machine: 7-state deterministic flow
**Why:** Clear enforcement of 5-question budget, predictable conversation 
arc, easy to debug, auditable.

## 3. Validation: Deterministic Python, not LLM-based
**Why:** Tax calculations must be reliable and repeatable. LLMs can hallucinate 
numbers. Deterministic logic is verifiable against IRS tables.

## 4. PDF: PyPDF2 form field population
**Why:** IRS Form 1040 is a standard PDF form with named fields. PyPDF2 
can populate fields directly. Simple, reliable.

## 5. Deployment: Render
**Why:** Free tier supports Python/FastAPI, auto-deploys from GitHub, 
no credit card required, simple environment variable management.

## 6. Question Budget: State machine enforcement, not LLM promise
**Why:** LLM cannot guarantee constraint. Hard-coded state transition 
ensures it's unbreakable.
```

#### 10.5 README Updates
**Requirements:**
- [ ] Add live demo URL
- [ ] Add deployment status
- [ ] Update quick start instructions
- [ ] Add architecture diagram reference

**Exit Criteria:**
- [ ] App deployed and publicly accessible
- [ ] All functionality works on live URL
- [ ] Full conversation flow tested
- [ ] All 4 pillars demonstrated
- [ ] Logs show complete audit trail
- [ ] Documentation complete

---

## 🎯 Success Criteria (End-to-End)

### Functional Requirements ✅
- [ ] Web-based chat interface
- [ ] User provides W-2 data
- [ ] Agent asks ≤ 5 questions
- [ ] Conversation is warm and human
- [ ] Completed 2025 Form 1040 PDF generated
- [ ] PDF is downloadable
- [ ] System deployed to public URL

### The Four Pillars ✅
- [ ] **Chat Loop:** Stateful conversation maintained across turns
- [ ] **Tools:** `validate_w2`, `generate_1040`, `log_observation` all called by agent
- [ ] **Guardrails:** 5-question budget enforced, off-topic rejected, inputs validated
- [ ] **Observation:** All decisions logged in structured JSON; judge can trace flow

### Code Quality ✅
- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] All files have comment headers
- [ ] PEP 8 compliant
- [ ] 80%+ test coverage (critical paths)

### Testing ✅
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Manual e2e tests pass (all 3 scenarios)
- [ ] Edge cases handled

---

## 📅 Timeline

| Phase | Task | Est. Hours | Actual |
|-------|------|-----------|--------|
| 0 | Foundation & Setup | 2 | 2 ✅ |
| 1 | Core Architecture | 4 | ? |
| 2 | Conversation Engine | 4 | ? |
| 3 | W-2 Validation | 3 | ? |
| 4 | Tax Computation | 3 | ? |
| 5 | PDF Generation | 3 | ? |
| 6 | Tool Integration | 2 | ? |
| 7 | Guardrails & Safety | 3 | ? |
| 8 | Observability | 2 | ? |
| 9 | Testing & QA | 4 | ? |
| 10 | Deployment & Polish | 2 | ? |
| **TOTAL** | | **32 hours** | **?** |

---

## 🚀 Getting Started: Next Steps

### Immediate Actions (Next 30 minutes):
1. ✅ Read this entire plan
2. Start **PHASE 1** → Create FastAPI skeleton
3. Use `TaxAssistant-Coder` agent for implementation guidance
4. Reference `.instructions.md` for code standards
5. Commit progress to git as you go

### Daily Workflow:
```bash
# Morning: Review plan, pick next task
# Code: Follow patterns in skill-tax-filing-orchestration
# Test: Run unit tests frequently
# Commit: Push daily progress
# Evening: Update this plan with actual times
```

### Blockers/Questions:
- Use `TaxAssistant-Coder` agent for code help
- Use `TaxAssistant-Architect` for design decisions
- Reference `.instructions.md` for project constraints
- Check `docs/PRD.md` and `docs/USERS.md` for requirements

---

## 📊 Phase Dependencies

```
Phase 0 ✅
   ↓
Phase 1 (FastAPI, Session, State Machine)
   ├→ Phase 2 (LLM, Prompts, Orchestration)
   │  ├→ Phase 6 (Tool Integration)
   │  │  └→ Phase 7 (Guardrails)
   │  │     └→ Phase 8 (Logging)
   │  │
   ├→ Phase 3 (W-2 Validation)
   │
   ├→ Phase 4 (Tax Computation)
   │  └→ Phase 5 (PDF Generation)
   │
   └→ Phase 9 (Testing)
      └→ Phase 10 (Deployment)
```

**Critical Path:** 0 → 1 → 2 → 6 → 7 → 8 → 9 → 10  
**Can work in parallel:** 3, 4, 5 while 2 is in progress

---

## 📝 Document Control

- **Owner:** Monica Peters
- **Version:** 1.0.0
- **Created:** 2026-06-24
- **Last Updated:** 2026-06-24
- **Status:** Ready for Phase 1 implementation
- **Audience:** Developer (Monica) + Judges + Future Maintainers

---

## Quick Reference: Key Files

| File | Purpose | Phase |
|------|---------|-------|
| `.instructions.md` | Project constraints & standards | All |
| `skills/skill-tax-filing-orchestration.md` | Conversation patterns | 2 |
| `agents/TaxAssistant-Coder.agent.md` | Implementation help | All |
| `docs/PRD.md` | Requirements | Reference |
| `docs/CLIENT_REQUEST.md` | Challenge definition | Reference |
| `src/main.py` | FastAPI entry | 1 |
| `src/conversation/engine.py` | Orchestration | 2 |
| `src/tools/validate_w2.py` | Validation | 3 |
| `src/utils/tax_tables.py` | Tax computation | 4 |
| `src/tools/generate_1040.py` | PDF generation | 5 |
| `tests/test_*.py` | All tests | 9 |

---

**Ready to build? Start with Phase 1. Good luck! 🚀**

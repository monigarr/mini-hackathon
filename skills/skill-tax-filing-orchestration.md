# SKILL: Tax Filing Orchestration

> **Expertise Domain:** Conversational agent orchestration for the Agentic Tax-Filing Assistant  
> **Version:** 1.0 • **Last Updated:** 2026-06-24  
> **Owner:** Monica Peters

---

## 🎯 Skill Summary

This skill teaches you how to architect and implement the **conversation orchestration layer** of the tax filing assistant. It covers:

- Chat loop patterns (request → agent → response → state update)
- State machine design for 5-question constraint
- Prompt engineering for warm, guidance-focused conversation
- Tool integration patterns (when to call which tool)
- Error recovery patterns (handling invalid input, off-topic questions)
- Observability integration (logging every decision)

**When to use this skill:**
- Building or debugging the core conversation engine
- Designing the interaction flow for new data collection scenarios
- Implementing question counter/budget enforcement
- Crafting prompts that maintain warm tone while staying on task
- Integrating new tools into the conversation loop

---

## 📐 Architecture Pattern: Request-Response Loop

Every turn in the conversation follows this pattern:

```
User Input
    ↓
[1] Validate & Parse Input
    ↓
[2] Update State Machine
    ↓
[3] Check Question Budget
    ↓
[4] Build Agent Prompt
    ↓
[5] Call LLM (GPT-4o-mini)
    ↓
[6] Parse LLM Response
    ↓
[7] Execute Tools (if needed)
    ↓
[8] Log Observation
    ↓
[9] Return Response to User
```

### Example: First Turn (Question 1)

```python
# User sends: "Hello, I need to file my taxes"

# [1] Validate Input
input_valid = len(user_message) > 0 and len(user_message) < 2000
# Result: True

# [2] Update State Machine
state_machine.transition("START", "W2_PROMPT")
state_machine.question_count = 1

# [3] Check Budget
if state_machine.question_count <= 5:  # True
    # Continue to step 4

# [4] Build Prompt
system_prompt = """You are a warm, helpful tax filing assistant...
    Current question count: 1/5
    Next question should ask about W-2 data (Box 1 and Box 2)."""
    
user_prompt = f"User said: {user_message}"

# [5] Call LLM
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    system_prompt=system_prompt,
    messages=[{"role": "user", "content": user_prompt}]
)

# [6] Parse Response
agent_message = response.choices[0].message.content
# Result: "Hi! I'd be happy to help you file your 2025 Form 1040. 
#         To get started, could you share the total wages (Box 1) 
#         from your W-2 form?"

# [7] Execute Tools
# (No tools called yet; LLM just asks question)

# [8] Log Observation
log_observation("agent_response", {
    "question_number": 1,
    "agent_message": agent_message,
    "state": "W2_PROMPT"
})

# [9] Return to User
send_to_chat(agent_message)
```

---

## 🔄 State Machine Design

The conversation progresses through 7 defined states:

```
┌─────────────────────────────────────────────┐
│ START: Agent greets, explains process       │
│ - Warm, friendly introduction               │
│ - Set expectations (5 questions, form gen)  │
│ - Transition: → W2_PROMPT                   │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ W2_PROMPT: Ask for W-2 Boxes 1, 2           │
│ - Natural language, warm tone               │
│ - Explain what Box 1 is (wages, largest #)  │
│ - Transition: → W2_VALIDATE (if valid)      │
│             or → W2_REPROMPT (if invalid)   │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ W2_VALIDATE: Call validate_w2 tool          │
│ - Check format (numbers, positive)          │
│ - Check logic (Box1 ≥ Box2)                 │
│ - If OK: Store data, transition → FILING    │
│ - If invalid: Explain error, re-ask (count) │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ FILING: Ask filing status (Single/MFJ)      │
│ - Simple yes/no or choice                   │
│ - Explain why it matters (std deduction)    │
│ - Transition: → DEPENDENCY                  │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ DEPENDENCY: Ask if can be claimed dependent │
│ - Yes/No question                           │
│ - Clarify if unclear                        │
│ - Transition: → CONFIRMATION                │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ CONFIRMATION: Summarize all data            │
│ - Confirm wages, filing status, dependency  │
│ - Ask user to validate (yes/no)             │
│ - Transition: → FORM_GENERATION             │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ FORM_GENERATION: Call generate_1040 tool    │
│ - Pass all collected data                   │
│ - Tool computes tax, fills PDF              │
│ - Transition: → COMPLETE                    │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ COMPLETE: Provide download link             │
│ - Show filled form                          │
│ - Add disclaimer                            │
│ - Allow restart or exit                     │
└─────────────────────────────────────────────┘
```

### Implementation Pattern

```python
from enum import Enum
from dataclasses import dataclass

class ConversationState(Enum):
    START = "start"
    W2_PROMPT = "w2_prompt"
    W2_VALIDATE = "w2_validate"
    W2_REPROMPT = "w2_reprompt"
    FILING = "filing"
    DEPENDENCY = "dependency"
    CONFIRMATION = "confirmation"
    FORM_GENERATION = "form_generation"
    COMPLETE = "complete"

@dataclass
class ConversationContext:
    session_id: str
    current_state: ConversationState
    question_count: int
    w2_data: dict  # {box1, box2, box4, box6}
    filing_status: str  # "Single" or "MFJ"
    is_dependent: bool
    created_at: datetime
    
    def transition(self, new_state: ConversationState):
        """Move to next state, incrementing question count if asking a question."""
        if new_state in [ConversationState.W2_PROMPT, 
                        ConversationState.FILING,
                        ConversationState.DEPENDENCY,
                        ConversationState.CONFIRMATION]:
            self.question_count += 1
        
        self.current_state = new_state
        log_observation("state_transition", {
            "from": self.current_state.value,
            "to": new_state.value,
            "question_count": self.question_count
        })
```

---

## 🎤 Prompt Engineering: Warm & Guided Conversation

### Core Principles

1. **No Jargon:** Never assume tax knowledge. Explain Box numbers, filing status, etc.
2. **Confirmatory:** Frequently summarize what you heard.
3. **Reassuring:** Acknowledge user's anxiety; promise clarity.
4. **One Thing at a Time:** Ask one question per turn; don't overwhelm.
5. **Give Context:** Why are you asking this? How does it help?

### System Prompt Template

```
You are TaxGuide, a warm, friendly tax filing assistant designed to help 
W-2 earners file a simple 2025 Form 1040.

## Your Role
- Guide the user through exactly 5 questions to collect their tax data
- Ask about W-2 information, filing status, and dependency status
- Compute tax and generate a completed Form 1040 PDF
- Explain what you're doing in simple, clear language
- Build trust through warmth and reassurance

## Constraints (Non-Negotiable)
- NEVER provide tax advice, tax planning, or tax optimization
- NEVER ask more than 5 questions total
- ALWAYS maintain a warm, conversational tone
- ALWAYS confirm data back to user before moving forward
- NEVER discuss complex tax scenarios (capital gains, self-employment, etc.)

## Current Context
- Question Count: {question_count}/5
- User's Collected Data: {collected_data_summary}
- Next Step: {next_step}

## Tone Guidelines
- Use "I" and "we" (collaborative, not interrogative)
- Use contractions ("I'd love to help", not "I would like to assist")
- Acknowledge user's effort ("Thanks for having that ready")
- Validate their information ("That matches what I expected")
- Keep sentences short and clear

## Example Good Responses
✅ "I see you have your W-2 ready—that's great! The number I need first 
   is the total wages (that's Box 1, usually the largest number on the form). 
   What's that amount?"

✅ "Just to make sure I have this right: you earned $40,000 and had $2,400 
   taken out for federal taxes. Is that correct?"

✅ "Perfect! That helps me understand your situation. One more quick question: 
   Can anyone claim you as a dependent, or are you independent?"

## Example Bad Responses
❌ "Provide W-2 Box 1 value."
❌ "To optimize your tax liability, consider..."
❌ "What is your income, filing status, W-2 boxes 1-6, and dependent status?"
❌ (Too technical jargon, off-topic, too many at once)
```

### Prompt for Each State

**W2_PROMPT State:**
```
You are now in question {question_count} of 5. Ask the user for their W-2 
Box 1 (wages) and Box 2 (federal tax withheld).

Be warm and encouraging. Explain what Box 1 is in simple terms. 
Offer examples if helpful.

Do NOT ask about Box 4 or 6 yet; those are optional follow-ups.
```

**FILING State (Question 2):**
```
You now have the user's W-2 data. Move to question {question_count}: 
Ask about filing status.

Use simple language: "Are you filing as Single or Married Filing Jointly?"

Explain briefly why: "This determines your standard deduction, which reduces 
your taxable income."

If user asks "What's the difference?", briefly explain:
- Single: You're unmarried on December 31, 2025
- MFJ: You're married and filing together
```

**DEPENDENCY State (Question 3):**
```
Ask question {question_count}: "Can anyone claim you as a dependent?"

If confused, clarify: "For example, if your parents claim you on their tax 
return, you'd be a dependent. Otherwise, you're independent."

Keep it simple; this is a yes/no question.
```

**CONFIRMATION State (Question 4-5):**
```
Summarize everything:

"Let me confirm what I have:
- Wages: ${wages}
- Federal tax withheld: ${withholding}
- Filing status: {filing_status}
- Dependency: {'Dependent' if is_dependent else 'Independent'}

Is all of this correct?"

If user says yes, move immediately to form generation without asking another 
question. If no, ask which part needs correction.
```

---

## 🔧 Tool Integration Pattern

### When to Call Tools

```python
class ConversationEngine:
    async def process_user_input(self, user_message: str) -> str:
        """Process user input and return agent response."""
        
        # Determine if tools need to be called based on state
        
        if self.state == ConversationState.W2_VALIDATE:
            # Tool: validate_w2
            tool_result = await validate_w2(user_message)
            if tool_result["success"]:
                self.context.w2_data = tool_result["data"]
                self.state = ConversationState.FILING
            else:
                self.state = ConversationState.W2_REPROMPT
            return tool_result["message"]
        
        elif self.state == ConversationState.FORM_GENERATION:
            # Tool: generate_1040
            tool_result = await generate_1040({
                "w2": self.context.w2_data,
                "filing_status": self.context.filing_status,
                "is_dependent": self.context.is_dependent
            })
            if tool_result["success"]:
                self.state = ConversationState.COMPLETE
                return f"Your form is ready! Download: {tool_result['download_link']}"
            else:
                return "Sorry, form generation failed. Please try again."
        
        else:
            # No tools; just call LLM for conversation
            return await call_agent_llm(user_message)
```

---

## ⚠️ Error Recovery Patterns

### Pattern 1: Invalid W-2 Data

```
User input: "forty thousand"

[1] validate_w2 tool fails: "Could not parse as number"

[2] Agent responds:
    "I want to make sure I get this right. I didn't understand 'forty thousand' 
     as a number. Can you enter it as digits? For example: 40000"

[3] Question count: NOT incremented (same question, just clarifying)

[4] State remains: W2_PROMPT (stay in same state, re-ask)

[5] Next turn: User enters "40000" → validation succeeds
```

### Pattern 2: Off-Topic Question

```
User input: "Can I deduct my home office?"

[1] LLM detects off-topic in system prompt

[2] Agent responds:
    "Great question! But that's beyond the scope of what I do here. I'm 
     specifically for filing your basic 2025 Form 1040. For home office 
     deductions, I'd recommend consulting a tax professional.
     
     Let's get back to your filing—I still need your W-2 Box 1 amount."

[3] Question count: NOT incremented (redirect, not a new question)

[4] State: Remains W2_PROMPT (no progress)

[5] Logging: Record off-topic attempt for observability
```

### Pattern 3: Exceeding Question Budget

```
User asks question 6 (budget is 5)

[1] Check: if question_count >= 5:

[2] Agent response:
    "Thank you for all that information. I have everything I need. 
     Let me generate your completed Form 1040..."

[3] Immediately call generate_1040 tool WITHOUT asking another question

[4] State transition: FORM_GENERATION → COMPLETE

[5] Logging: Record budget exceeded + automatic completion
```

---

## 📊 Observable Logging Integration

Every state transition and decision should be logged:

```python
from src.tools.logger import log_observation

# At start of user turn
log_observation("user_input_received", {
    "session_id": session_id,
    "current_state": current_state.value,
    "question_count": question_count,
    "user_message": user_message[:100]  # First 100 chars
})

# Before LLM call
log_observation("llm_call_initiated", {
    "session_id": session_id,
    "model": "gpt-4o-mini",
    "system_prompt_summary": system_prompt[:50],
    "question_count": question_count
})

# After LLM response
log_observation("llm_response_received", {
    "session_id": session_id,
    "response": agent_response,
    "tokens_used": token_count,
    "latency_ms": elapsed_time
})

# Before tool call
log_observation("tool_call_initiated", {
    "session_id": session_id,
    "tool_name": "validate_w2",
    "input": w2_data
})

# After tool execution
log_observation("tool_execution_completed", {
    "session_id": session_id,
    "tool_name": "validate_w2",
    "success": True,
    "output": tool_result
})

# State transition
log_observation("state_transition", {
    "session_id": session_id,
    "from_state": previous_state.value,
    "to_state": new_state.value,
    "question_count": question_count
})
```

---

## 🧮 Question Budget Enforcement

The 5-question budget is non-negotiable. Here's how to enforce it:

```python
class QuestionBudgetEnforcer:
    """Ensures we never exceed 5 questions."""
    
    MAX_QUESTIONS = 5
    
    @staticmethod
    def should_ask_question(context: ConversationContext) -> bool:
        """Return True if we can ask another question."""
        return context.question_count < QuestionBudgetEnforcer.MAX_QUESTIONS
    
    @staticmethod
    def increment_question_count(context: ConversationContext):
        """Increment question counter safely."""
        context.question_count += 1
        if context.question_count > QuestionBudgetEnforcer.MAX_QUESTIONS:
            raise ValueError("Question budget exceeded!")
    
    @staticmethod
    def remaining_questions(context: ConversationContext) -> int:
        """Return number of questions left."""
        return max(0, QuestionBudgetEnforcer.MAX_QUESTIONS - context.question_count)

# Usage in conversation loop
if QuestionBudgetEnforcer.should_ask_question(context):
    # Ask the question
    state = next_question_state
    QuestionBudgetEnforcer.increment_question_count(context)
else:
    # Jump to form generation
    state = ConversationState.FORM_GENERATION
```

---

## 🚀 Implementation Checklist

When building this skill into code:

- [ ] State machine enum defined with all 7 states
- [ ] ConversationContext dataclass with all required fields
- [ ] Prompt templates for each state created
- [ ] Tool integration points identified
- [ ] Question counter logic implemented
- [ ] Error recovery patterns coded
- [ ] Logging calls at every transition
- [ ] Question budget enforcer tested
- [ ] Warm tone verified in all prompts
- [ ] Off-topic guardrail tested
- [ ] Unit tests written for state transitions
- [ ] Integration test written for happy path

---

## 📚 Related Documentation

- [`.instructions.md`](.instructions.md) — Project-wide constraints
- [`docs/DREAM_AGENT_TEAM.md`](docs/DREAM_AGENT_TEAM.md) — Agent design
- [`docs/USERS.md`](docs/USERS.md) — User personas and use cases
- [FastAPI docs](https://fastapi.tiangolo.com) — Web framework

---

## ✅ Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-24 | Initial release |

**Owner:** Monica Peters  
**License:** MIT

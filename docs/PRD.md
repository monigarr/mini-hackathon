Based on your CLIENT_REQUEST.md as the source of truth and the provided templates, here is a completed PRD for your Hackathon project.

This PRD is fully aligned with the hackathon challenge, focusing on creating a functional, well-architected agentic system that meets all specified requirements and constraints.

---

# Agentic Tax-Filing Assistant — Product Requirements Document (PRD)

## 0. Executive Summary
- **Problem:** Filing a U.S. federal tax return (Form 1040) is a complex, manual, and error-prone process, especially for first-time or simple filers. Users are often overwhelmed by the form itself, the instructions, and the fear of making a mistake.
- **User:** A W-2 employee earning roughly $40,000/year who has a simple tax situation and needs to file their 2025 federal return.
- **Context:** This is a hackathon project to build a prototype agentic system that demonstrates key AI engineering pillars: a chat loop, tool use, guardrails, and observability.
- **Why now:** The rise of LLMs enables a new, conversational paradigm for complex, step-by-step processes. The goal is to prove the viability of an agentic harness for this task, not to replace existing tax software.
- **Success definition:** A user can have a short, friendly conversation with an agent and, within 5 questions, receive a completed and downloadable 2025 Form 1040 based on their W-2 and filing status. The agent's behavior must be observable, bounded, and reliable.

## 1. Problem Definition
- **Core problem:** The IRS Form 1040 is complicated, and the process of filling it out correctly requires navigating dense instructions to determine which lines apply to a specific, simple financial situation.
- **Current workaround(s):** People either spend hours reading instructions and filling out forms by hand, or they pay for expensive tax software or a professional preparer for a simple tax return.
- **Why existing solutions fail:** Off-the-shelf software can be overkill, expensive, or have poor user experience, especially for simple returns. A human preparer is costly and unnecessary for a simple W-2 earner. The agentic system fills the gap by providing a free, guided, and human-like experience for a common, low-complexity filing scenario.

## 2. Target User (Narrow)
- **Role:** A first-time or infrequent tax filer who receives a W-2 from a single employer, with an annual income of approximately $40,000.
- **Environment:** The user is at home with a stable internet connection and has their W-2 and basic personal information available. They are comfortable using a web browser but not necessarily tech-savvy.
- **Constraints:** The user is likely anxious about taxes. They have limited knowledge of tax forms and terminology. They need a simple, reassuring, and friendly experience.
- **Workflow moment this product enters:** When the user receives their W-2 and needs to file their federal taxes but wants guidance without the complexity of traditional tax software or the cost of a professional.

## 3. Core Use Cases (Traceable)
| ID | Use Case | Moment | Why Agent (vs UI/dashboard) |
|----|----------|--------|-----------------------------|
| UC1 | User provides W-2 data to the agent | User has their W-2 form ready and needs to enter this data into the system. | A simple form upload would be fragile. An agent can interpret the data via a tool, ask clarifying questions, and guide the user, making the process more resilient and human-like. |
| UC2 | User provides filing status and personal details | The agent needs to know if the user is single, married, etc., and if they can be claimed as a dependent. | The agent can have a natural conversation to gather this information, rather than presenting a rigid form, ensuring a warmer experience within the tight question budget. |
| UC3 | Agent computes and fills the 1040 form | The agent has all the required data and must generate the completed form. | This is a deterministic, data-to-output mapping task. The agent is orchestrated to call a tool that performs this calculation and generation, ensuring accuracy and reliability. |

## 4. Requirements

### Functional
- [x] **Chat Loop:** Implement a web-based chat interface that maintains conversation state across turns.
- [x] **Tools:** Provide at least one tool, e.g., `generate_1040`, that populates a 1040 PDF and prepares it for download.
- [x] **Guardrails:** Enforce the 5-question limit and prevent the agent from answering off-topic questions or giving tax advice beyond what is strictly necessary for data collection.
- [x] **Observation:** Log all agent decisions, tool calls, and question/answer pairs in a format that is easily viewable by a judge.
- [x] **W-2 Input:** Allow the user to provide the W-2 data. This can be via a file upload or via chat. The agent must extract the necessary information (Boxes 1, 2, 4, 6, etc.).
- [x] **1040 Generation:** Use the provided `1040_V2025.pdf` as the base template. Populate the correct fields (e.g., Filing Status, Wages, Federal Tax Withheld, Standard Deduction, Taxable Income, Tax, Overpayment/Amount Owed) based on the data.
- [x] **Download:** Provide a link for the user to download the completed `1040_V2025.pdf` after the chat is complete.
- [x] **Filing Status Handling:** Support both "Single" and "Married Filing Jointly" filing statuses, adjusting the standard deduction and tax tables accordingly.
- [x] **Question Budget:** Design the conversation to gather all necessary data in exactly 5 questions. This will require careful prompt engineering and a deterministic conversation flow.
- [x] **Tone:** The agent's responses must be warm, friendly, and empathetic, using human-like language and avoiding robotic or interrogative phrasing.

### Non-Functional (Echelon Enterprise)
- **Latency target:** The total conversation should take under 2 minutes to complete. Individual LLM calls should be < 2 seconds.
- **Reliability target:** The system should successfully complete the end-to-end flow for the happy path > 95% of the time.
- **Security baseline:** No real PII or tax data will be stored or used in a production context. All user input is ephemeral for the session.
- **Accessibility:** The web chat should be usable with a keyboard and screen reader.
- **Observability:** The system will log all steps, decisions, and tool calls with sufficient detail for a judge to understand the agent's chain of thought.

## 5. Constraints
- **Legal / compliance:** This is a prototype for educational purposes only. It is not a tax preparation service, and it is not a substitute for professional tax advice. The tool will display a disclaimer to this effect.
- **Data limitations:** The agent is strictly limited to the data provided in the W-2 and the user's filing status/dependency status. It will not incorporate other income, deductions, or credits.
- **System limitations:** The system must be deployable on a free service like Render. Costs associated with LLM usage must be controlled and can be capped.
- **Team / time constraints:** This is a single-person hackathon project with a limited timeframe. The architecture must be simple and straightforward.

## 6. Success Metrics
- **User success:** The user can complete the conversation in 5 questions and download a filled 1040 form that is mathematically correct for their given inputs.
- **System performance:** The entire interaction is completed within a reasonable time (under 2 minutes).
- **Cost constraints:** The total cost of LLM API calls to complete one filing is less than $0.10.
- **Failure tolerance:** If an error occurs (e.g., invalid input), the agent can gracefully recover and guide the user to provide correct information.

## 7. Failure Modes (Explicit)
| Failure | Impact | Expected Behavior |
|--------|--------|------------------|
| User provides incorrect/incomplete W-2 data | Incorrect form output | The agent validates the data (e.g., check for number format, required fields) and asks the user to re-enter or correct it. |
| LLM fails or returns an error | Conversation stalls | System catches the error and displays a friendly "Something went wrong, please try again" message to the user. |
| Tool fails to generate the PDF | Form is not downloadable | The system logs the error and surfaces it to the user to restart. |
| User asks a question beyond the agent's scope | Agent is derailed from its core task | The agent must be prompted/guardrailed to politely decline and steer the conversation back to tax filing data collection. |
| 5-question budget is exceeded | User is asked too many questions | The agent must have a strict internal counter and use a tool or state transition to guarantee the conversation ends after the 5th question. |

## 8. Out of Scope
- **E-Filing:** The system will not transmit the return to the IRS.
- **Complex Tax Situations:** It will not handle self-employment, capital gains, itemized deductions, rental income, or other complex tax scenarios.
- **Data Persistence:** It will not save or store user data after the session ends.
- **User Accounts:** No login or user management is required.
- **Error Correction:** While the agent can ask for corrections, a comprehensive "edit your answer" feature is a stretch goal.
- **Multiple W-2s:** The solution is designed for a single W-2 earner.
- **Mobile App:** The solution is a web chat, not a native mobile application.

## 9. Delivery Phases
| Phase | Scope | Exit Criteria |
|------|------|---------------|
| 1 - Core Harness & Data Collection | Set up the web chat (FastAPI/Streamlit), implement the chat loop, and build the conversation logic to collect W-2 data and filing status. | Agent can successfully complete a conversation, collecting all required data within 5 questions. |
| 2 - PDF Generation & Tool Implementation | Implement the `generate_1040` tool. This includes parsing the base PDF, filling fields, and computing the tax. | The tool can take the collected data and output a correctly filled PDF. |
| 3 - Observability & Guardrails | Add logging for all agent actions, enforce the 5-question limit, and implement the "off-topic" guardrail. | A judge can see a clear log of the agent's decisions, and the agent cannot ask more than 5 questions. |
| 4 - Deployment & Testing | Deploy the application to Render. Write a basic test suite for the end-to-end flow. | The application is live at a public URL and passes the smoke test. |

## 10. Document Control
- **Owner:** Monica Peters
- **Version:** 1.0 (Final)
- **Last Updated:** June 24, 2026
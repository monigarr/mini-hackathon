AGENTIC TAX-FILING ASSISTANT — USERS
0. Source of Truth
All features MUST map to a defined use case below.

1. Target User (Single Persona First)
Role: First-time or infrequent tax filer, W-2 employee earning ~$40,000/year

Experience level: Low to moderate tax knowledge; may be anxious about filing

Environment: At home or personal workspace with stable internet connection

Technical context: Comfortable using a web browser; not necessarily tech-savvy

Constraints: Limited time (needs quick filing), high cognitive load (tax confusion), risk-averse (fear of mistakes)

2. Day-in-the-Life Workflow
Before system interaction: User receives their W-2 from employer. They know they need to file taxes but dread the complexity. They may have used tax software before and found it overwhelming, or they're doing this for the first time.

Interaction moment: User opens the web chat. They're greeted warmly and guided through exactly 5 questions. They provide their W-2 data, filing status, and dependency status. The agent provides clear, friendly confirmations and guidance.

After interaction: User receives a link to download their completed 2025 Form 1040. They're confident the form is correct because the conversation was guided and the agent confirmed each piece of data. They can file or review the form with confidence.

3. Core Needs
Need 1: Simplicity and Guidance. User needs to be led through the process step-by-step without being overwhelmed by tax jargon or form complexity.

Need 2: Reassurance and Accuracy. User needs to feel confident they've done it correctly. The agent should confirm data and provide a finished product they can trust.

4. Use Cases
UC1 — Provide W-2 Data
Moment: User has their W-2 form in hand and is ready to enter data.

Need: To input wages, federal tax withheld, and other W-2 fields correctly.

Why conversational / AI-first: A simple form upload would be fragile. An agent can interpret the data via a tool, ask clarifying questions, and guide the user, making the process more resilient and human-like.

Success outcome: User's W-2 data is validated and stored accurately.

Failure risk: User provides incorrect or incomplete data; validation catches and requests correction.

UC2 — Provide Filing Status and Personal Details
Moment: After W-2 data, the agent needs to know the user's filing status and if they can be claimed as a dependent.

Need: To determine which standard deduction applies and ensure accurate tax computation.

Why conversational / AI-first: The agent can have a natural conversation to gather this information, rather than presenting a rigid form, ensuring a warmer experience within the tight question budget.

Success outcome: Filing status and dependency status are stored correctly.

Failure risk: User misunderstands filing status options; agent clarifies with simple language.

UC3 — Generate Completed 1040
Moment: After all data is collected, the agent generates the final form.

Need: To receive a completed, downloadable 2025 Form 1040.

Why conversational / AI-first: This is a deterministic, data-to-output mapping task. The agent is orchestrated to call a tool that performs this calculation and generation, ensuring accuracy and reliability.

Success outcome: User can download the filled PDF form.

Failure risk: Tool fails to generate PDF; error is logged and user is notified to restart.

5. UX Entry Point
Where in system: The web chat interface, accessible at the public URL.

Trigger action: User opens the URL and sees a friendly greeting from the agent.

Expected response time: Agent replies within 2 seconds; total conversation under 2 minutes.

Acceptable friction: User may need to find their W-2; minimal friction beyond that.

6. Trust Expectations
What must never happen: Agent giving tax advice, storing real PII, exceeding 5 questions, generating an incorrect form without validation.

What uncertainty looks like: User is unsure which filing status to choose; agent clarifies with simple examples.

What builds trust: Warm tone, clear confirmations, validation of inputs, finished form ready for download.

7. Out of Scope Users
High-income earners with complex tax situations (self-employment, rental income, capital gains)

Users with multiple W-2s

Users who need state tax returns

Users who need e-filing

8. Traceability Matrix
Use Case	Required Data	Risk if Wrong	Mitigation
UC1	W-2 Box 1 (Wages), Box 2 (Fed Withholding), Box 4 (Social Security), Box 6 (Medicare)	Incorrect tax computation	Validation tool checks data; asks for correction if invalid
UC2	Filing status (Single/Married), dependency status	Wrong standard deduction, incorrect tax	Clear questions with examples; state machine guides choices
UC3	All collected data	Wrong form output	Deterministic tax computation; PDF generation tool
9. Document Control
Owner: Monica Peters, monigarr@monigarr.com

Version: 1.0 (Final)

Created: 2026-06-24

Last Updated: 2026-06-24
CODE COMMENT HEADER — TAX ASSISTANT
python
"""
===============================================================================
FILE: [filename].py
AUTHOR: Monica Peters, monigarr@monigarr.com
CREATED: 2026-06-24
LICENSE: MIT

PURPOSE:
[Brief description of what this file does in the tax assistant system]

USAGE:
    # Example usage
    from src.[module] import [class/function]
    result = [function]([args])

ENTERPRISE LEVEL:
* security: No PII stored; environment variables for secrets
* privacy: Ephemeral session state only
* accessibility: Clear, human-readable responses
* reusability: Modular design with clear interfaces
* performance: LLM calls < 2 seconds; PDF generation < 1 second
* stability: Graceful error handling; deterministic computation
* maintainability: Single responsibility; clear separation of concerns
* observability: Structured JSON logging of all actions
* extensibility: Easy to add new tax forms, tools, or LLM providers
* documentation: Comprehensive code headers and architecture docs
* rapid handoff: One-command local run; clean interfaces
* operational continuity: Deployed to Render; health checks

DESIGN PATTERN:
* [e.g., snake_case for functions, CamelCase for classes]

ARCHITECTURE:
Part of the Agentic Tax-Filing Assistant system.
- Layer: [e.g., Orchestration, Tool, Model, Utility]
- Depends on: [list dependencies]
- Called by: [list callers]
- Data flow: [describe data in/out]

===============================================================================
"""
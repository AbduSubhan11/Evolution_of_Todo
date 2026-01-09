---
id: 1
title: "auth-api-integration-spec"
stage: spec
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: auth-api-integration
branch: auth-api-integration
user: user
command: "/sp.specify This is Phase II, Spec 2: named \"Authentication & API integration for the Todo app.\""
labels: ["specification", "authentication", "api", "todo-app"]
links:
  spec: "specs/auth-api-integration/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/auth-api-integration/spec.md"
  - "specs/auth-api-integration/checklists/requirements.md"
tests: []
---

# Prompt

```
This is Phase II, Spec 2: named "Authentication & API integration for the Todo app."

Scope of this specification:
- Integrate Better Auth on the Next.js frontend
- Implement JWT-based authentication for API requests
- Create Next.js API routes for Todo operations
- Backend is abstracted but connected to Neon Serverless PostgreSQL
- Data ownership must be enforced per authenticated user
- Must follow all Phase II rules from the Constitution

Instructions:
- Treat the Constitution as the single source of truth
- Specify all frontend authentication behavior:
  - Sign-up, sign-in, sign-out
  - JWT acquisition
  - Attaching JWT to API requests
- Specify API route behavior and contracts:
  - RESTful endpoints (`/api/{user_id}/tasks`)
  - Request headers and expected responses
  - Data filtered by authenticated user
  - Authorization failure responses
- Specify Neon DB usage only as the data layer for user and task records
- Define system responsibilities in a step-by-step manner
```

# Response

Created specification for Authentication & API integration for the Todo app, including user scenarios, functional requirements, key entities, and success criteria. The specification was refined to be technology-agnostic while preserving the core requirements for authentication and API integration.

# Outcome

Specification document created at specs/auth-api-integration/spec.md with validation checklist at specs/auth-api-integration/checklists/requirements.md. The specification is ready for the planning phase.
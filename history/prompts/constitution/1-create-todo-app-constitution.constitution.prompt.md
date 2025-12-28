---
id: 1
title: Create Todo App Constitution
stage: constitution
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-app
branch: master
user: user
command: /sp.constitution Todo App Constitution
labels: [constitution, todo-app, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
Todo App Constitution
The Evolution of Todo – Spec-Driven & AI-Native Development

Core Principles
I. Project Scope (Phase I)
Goal: Build a console-based Todo application with a interactive cli UI with all operation like Add Task – Create new todo items
Delete Task – Remove tasks from the list
Update Task – Modify existing task details
View Task List – Display all tasks
Mark as Complete – Toggle task completion status and Search & Filter – Search by keyword; filter by status, priority, or date

Constraint: Development MUST follow a single, well-defined phase without skipping architectural steps.
 Non-Negotiable: The design must remain compatible with future evolution, without implementing future features now.



Tooling Rules
Python version: 3.12+ (or 3.13 if available locally)


Package manager: uv (mandatory)


Environment isolation: uv-managed virtual environment


No global installs

II. Development Methodology (Strict)
Spec-Driven Development is mandatory


Claude Code MUST generate all implementation


Humans may only author:


Constitution


Specs


Constraints




III. Architecture (Non-Negotiable)
Clear separation between:


Domain logic


State management


Interaction layer


Domain behavior MUST NOT depend on storage or UI technology


Architecture must remain simple, deterministic, and inspectable



IV. Test-First Approach
Behavior must be specified before implementation


Specs define acceptance criteria


Implementation must satisfy specs exactly


Refactoring is allowed only if specs remain unchanged



V. Data Management (Phase I Rule)
State is stored ONLY in system memory


In-memory collections (e.g., arrays/lists of Todos) are the single source of truth


No persistence across application restarts


File systems, databases, and external services are strictly forbidden



VI. Code Quality Standards
Deterministic behavior


Predictable outputs


Clear error handling


Type safety where applicable


Readable and inspectable structure



VII. Interaction Model
User
```

## Response snapshot

Created the Todo App constitution file at `.specify/memory/constitution.md` with all the specified principles and governance rules. The constitution includes:
- Project scope and constraints
- Development methodology requirements
- Architecture principles
- Test-first approach
- Data management rules
- Code quality standards
- Interaction model
- Tooling requirements
- Development workflow
- Governance rules

## Outcome

- ✅ Impact: Constitution file created at .specify/memory/constitution.md with all specified principles
- 🧪 Tests: none
- 📁 Files: 1 file created (.specify/memory/constitution.md)
- 🔁 Next prompts: Proceed with spec creation for the Todo app
- 🧠 Reflection: Constitution provides clear governance framework for the Todo app development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create the spec file based on the constitution
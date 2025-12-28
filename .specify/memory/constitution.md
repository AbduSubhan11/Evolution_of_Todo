<!-- SYNC IMPACT REPORT:
Version change: N/A (initial creation) → 1.0.0
Modified principles: N/A
Added sections: All sections (initial constitution creation)
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending (check for agent-specific references)
Follow-up TODOs: None
-->
# Todo App Constitution
The Evolution of Todo – Spec-Driven & AI-Native Development

## Core Principles

### I. Project Scope (Phase I)
Goal: Build a console-based Todo application with a interactive cli UI with all operation like Add Task – Create new todo items; Delete Task – Remove tasks from the list; Update Task – Modify existing task details; View Task List – Display all tasks; Mark as Complete – Toggle task completion status; and Search & Filter – Search by keyword; filter by status, priority, or date. Constraint: Development MUST follow a single, well-defined phase without skipping architectural steps. Non-Negotiable: The design must remain compatible with future evolution, without implementing future features now.

### II. Development Methodology (Strict)
Spec-Driven Development is mandatory. Claude Code MUST generate all implementation. Humans may only author: Constitution, Specs, and Constraints.

### III. Architecture (Non-Negotiable)
Clear separation between: Domain logic, State management, and Interaction layer. Domain behavior MUST NOT depend on storage or UI technology. Architecture must remain simple, deterministic, and inspectable.

### IV. Test-First Approach
Behavior must be specified before implementation. Specs define acceptance criteria. Implementation must satisfy specs exactly. Refactoring is allowed only if specs remain unchanged.

### V. Data Management (Phase I Rule)
State is stored ONLY in system memory. In-memory collections (e.g., arrays/lists of Todos) are the single source of truth. No persistence across application restarts. File systems, databases, and external services are strictly forbidden.

### VI. Code Quality Standards
Deterministic behavior. Predictable outputs. Clear error handling. Type safety where applicable. Readable and inspectable structure.

### VII. Interaction Model
User interaction occurs through a console-based CLI interface with clear, intuitive commands for all operations.

## Tooling Rules
Python version: 3.12+ (or 3.13 if available locally). Package manager: uv (mandatory). Environment isolation: uv-managed virtual environment. No global installs.

## Development Workflow
All implementation must follow Spec-Driven Development (SDD) methodology. Specifications must be complete before any implementation begins. Claude Code is responsible for all code generation. Human developers are limited to creating constitution, specifications, and constraints only.

## Governance

Constitution governs all development activities and supersedes any conflicting practices. Amendments require explicit documentation, approval, and migration plan if applicable. All implementation must remain compatible with future evolution without implementing future features prematurely. Development must follow the prescribed architectural separation of concerns.

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
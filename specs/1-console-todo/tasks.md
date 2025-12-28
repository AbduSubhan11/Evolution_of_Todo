---
description: "Task list for Console Todo Application implementation"
---

# Tasks: Console Todo Application

**Input**: Design documents from `/specs/1-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included based on functional requirements and edge cases from the specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/, tests/
- [x] T002 Initialize Python project with requirements.txt and pyproject.toml
- [x] T003 [P] Configure linting and formatting tools (black, flake8, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Todo model in src/models/todo.py
- [x] T005 Create TodoList collection in src/models/todo.py
- [x] T006 Create TodoService in src/services/todo_service.py
- [x] T007 Configure in-memory storage mechanism for TodoList
- [x] T008 [P] Setup basic CLI structure in src/cli/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items and view their list of todos

**Independent Test**: Can be fully tested by adding several todos and viewing the complete list, delivering the basic value of task tracking.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T009 [P] [US1] Unit test for Todo creation in tests/unit/models/test_todo.py
- [x] T010 [P] [US1] Unit test for TodoList operations in tests/unit/models/test_todo.py
- [x] T011 [P] [US1] Integration test for adding and viewing todos in tests/integration/test_todo_operations.py

### Implementation for User Story 1

- [x] T012 [P] [US1] Implement Todo model with all required attributes in src/models/todo.py
- [x] T013 [P] [US1] Implement TodoList collection with add and get_all methods in src/models/todo.py
- [x] T014 [US1] Implement add_todo method in TodoService in src/services/todo_service.py
- [x] T015 [US1] Implement get_all_todos method in TodoService in src/services/todo_service.py
- [x] T016 [US1] Implement CLI interface for adding todos in src/cli/main.py
- [x] T017 [US1] Implement CLI interface for viewing todos in src/cli/main.py
- [x] T018 [US1] Add input validation for todo description in src/services/todo_service.py
- [x] T019 [US1] Add basic console menu system in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Update and Delete Todos (Priority: P2)

**Goal**: Enable users to update and delete existing todos so that they can keep their task list current and relevant

**Independent Test**: Can be tested by creating a todo, updating its details, and verifying the changes are saved, then deleting it and confirming it's removed.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T020 [P] [US2] Unit test for updating todo details in tests/unit/services/test_todo_service.py
- [x] T021 [P] [US2] Unit test for deleting todos in tests/unit/services/test_todo_service.py

### Implementation for User Story 2

- [x] T022 [US2] Implement update_todo method in TodoService in src/services/todo_service.py
- [x] T023 [US2] Implement delete_todo method in TodoService in src/services/todo_service.py
- [x] T024 [US2] Implement CLI interface for updating todos in src/cli/main.py
- [x] T025 [US2] Implement CLI interface for deleting todos in src/cli/main.py
- [x] T026 [US2] Add validation for todo updates in src/services/todo_service.py
- [x] T027 [US2] Add error handling for operations on non-existent todos in src/services/todo_service.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Todos Complete/Incomplete (Priority: P3)

**Goal**: Enable users to mark todos as complete or incomplete so that they can track their progress and see what still needs to be done

**Independent Test**: Can be tested by marking todos as complete and incomplete, verifying the status changes are reflected in the display.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T028 [P] [US3] Unit test for toggling todo completion status in tests/unit/services/test_todo_service.py

### Implementation for User Story 3

- [x] T029 [US3] Implement toggle_completion method in TodoService in src/services/todo_service.py
- [x] T030 [US3] Implement CLI interface for marking todos as complete/incomplete in src/cli/main.py
- [x] T031 [US3] Update Todo model to support completion status toggling in src/models/todo.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Search and Filter Todos (Priority: P4)

**Goal**: Enable users to search and filter their todos by keyword, status, priority, or date so that they can quickly find specific tasks

**Independent Test**: Can be tested by searching/filtering with different criteria and verifying the correct subset of todos is displayed.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [x] T032 [P] [US4] Unit test for search functionality in tests/unit/services/test_search_filter.py
- [x] T033 [P] [US4] Unit test for filter functionality in tests/unit/services/test_search_filter.py

### Implementation for User Story 4

- [x] T034 [US4] Implement search_todos method in TodoService in src/services/todo_service.py
- [x] T035 [US4] Implement filter_todos method in TodoService in src/services/todo_service.py
- [x] T036 [US4] Implement CLI interface for searching todos in src/cli/main.py
- [x] T037 [US4] Implement CLI interface for filtering todos in src/cli/main.py
- [x] T038 [US4] Add search and filter options to console menu in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T039 [P] Documentation updates in README.md
- [x] T040 Input validation and error handling across all operations in src/services/todo_service.py
- [x] T041 Handle edge cases from specification (empty lists, invalid IDs, etc.) in src/services/todo_service.py
- [x] T042 [P] Additional unit tests in tests/unit/
- [x] T043 Error message consistency and user-friendly messages in src/cli/main.py
- [x] T044 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Todo creation in tests/unit/models/test_todo.py"
Task: "Unit test for TodoList operations in tests/unit/models/test_todo.py"
Task: "Integration test for adding and viewing todos in tests/integration/test_todo_operations.py"

# Launch all models for User Story 1 together:
Task: "Implement Todo model with all required attributes in src/models/todo.py"
Task: "Implement TodoList collection with add and get_all methods in src/models/todo.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
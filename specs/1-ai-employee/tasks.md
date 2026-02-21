---

description: "Task list template for feature implementation"
---

# Tasks: Personal AI Employee

**Input**: Design documents from `/specs/1-ai-employee/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python project with uv and requirements.txt
- [ ] T003 [P] Configure linting and formatting tools (black, flake8, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Setup base watcher class in src/watchers/base_watcher.py
- [ ] T005 [P] Implement audit logging framework in src/utils/audit_logger.py
- [ ] T006 [P] Setup configuration loader in src/utils/config_loader.py
- [ ] T007 Create retry handler utility in src/utils/retry_handler.py
- [ ] T008 Configure credential management system for secure storage
- [ ] T009 Setup Obsidian vault structure with required folders

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Personal Affairs Management (Priority: P1) 🎯 MVP

**Goal**: Build core functionality for AI employee to monitor and respond to personal affairs (Gmail, WhatsApp, banking)

**Independent Test**: System can independently detect an important email, WhatsApp message, or financial transaction and either handle it automatically (within defined rules) or escalate to the user for approval

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T010 [P] [US1] Contract test for email MCP server in tests/contract/test_email_mcp.py
- [ ] T011 [P] [US1] Integration test for email processing workflow in tests/integration/test_email_workflow.py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create PersonalAffair model in src/models/personal_affair.py
- [ ] T013 [P] [US1] Create CompanyHandbookRule model in src/models/company_handbook_rule.py
- [ ] T014 [US1] Implement Gmail watcher in src/watchers/gmail_watcher.py
- [ ] T015 [US1] Implement WhatsApp watcher in src/watchers/whatsapp_watcher.py
- [ ] T016 [US1] Implement filesystem watcher in src/watchers/filesystem_watcher.py
- [ ] T017 [US1] Create email skills for Claude in src/skills/email_skills.py
- [ ] T018 [US1] Create finance skills for Claude in src/skills/finance_skills.py
- [ ] T019 [US1] Implement rule evaluation service in src/services/rule_evaluator.py
- [ ] T020 [US1] Add email processing logic to orchestrator.py
- [ ] T021 [US1] Add WhatsApp processing logic to orchestrator.py
- [ ] T022 [US1] Add financial transaction processing logic to orchestrator.py
- [ ] T023 [US1] Add validation and error handling for personal affairs
- [ ] T024 [US1] Add logging for personal affairs operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Business Task Automation (Priority: P1)

**Goal**: Enable AI employee to manage business tasks including social media posting, payments, project tracking, and generating reports

**Independent Test**: System can independently handle business tasks like scheduling social media posts, processing routine payments, and generating weekly business summaries

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US2] Contract test for payment MCP server in tests/contract/test_payment_mcp.py
- [ ] T026 [P] [US2] Integration test for business task workflow in tests/integration/test_business_task_workflow.py

### Implementation for User Story 2

- [ ] T027 [P] [US2] Create BusinessTask model in src/models/business_task.py
- [ ] T028 [P] [US2] Create WeeklyReport model in src/models/weekly_report.py
- [ ] T029 [US2] Implement social media MCP server in src/mcp-servers/social-mcp/
- [ ] T030 [US2] Implement payment MCP server in src/mcp-servers/payment-mcp/
- [ ] T031 [US2] Create social skills for Claude in src/skills/social_skills.py
- [ ] T032 [US2] Implement business task scheduler in src/services/task_scheduler.py
- [ ] T033 [US2] Implement weekly report generator in src/services/report_generator.py
- [ ] T034 [US2] Add social media posting logic to orchestrator.py
- [ ] T035 [US2] Add payment processing logic to orchestrator.py
- [ ] T036 [US2] Add report generation logic to orchestrator.py
- [ ] T037 [US2] Add validation and error handling for business tasks
- [ ] T038 [US2] Add logging for business task operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Human-in-the-Loop Safeguards (Priority: P2)

**Goal**: Implement file-based approval system to prevent unwanted automated actions for critical operations

**Independent Test**: System creates approval request files for sensitive actions and waits for human intervention before proceeding

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T039 [P] [US3] Contract test for approval workflow in tests/contract/test_approval_workflow.py
- [ ] T040 [P] [US3] Integration test for approval request handling in tests/integration/test_approval_handling.py

### Implementation for User Story 3

- [ ] T041 [P] [US3] Create ApprovalRequest model in src/models/approval_request.py
- [ ] T042 [US3] Implement approval request creator in src/services/approval_request_creator.py
- [ ] T043 [US3] Implement approval request processor in src/services/approval_request_processor.py
- [ ] T044 [US3] Add approval workflow to orchestrator.py
- [ ] T045 [US3] Create approval request file templates in templates/
- [ ] T046 [US3] Add validation and error handling for approval requests
- [ ] T047 [US3] Add logging for approval request operations

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Local-First Architecture (Priority: P2)

**Goal**: Ensure all data and processing remains on local machine by default with external services used only when necessary

**Independent Test**: System stores all personal data locally in Obsidian vault and only connects to external services when performing specific required actions

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T048 [P] [US4] Contract test for local data storage in tests/contract/test_local_storage.py
- [ ] T049 [P] [US4] Integration test for local-first processing in tests/integration/test_local_processing.py

### Implementation for User Story 4

- [ ] T050 [US4] Implement local data storage service in src/services/local_data_service.py
- [ ] T051 [US4] Implement file-based state management in src/services/file_state_manager.py
- [ ] T052 [US4] Add local vault synchronization to orchestrator.py
- [ ] T053 [US4] Implement offline mode handling in src/services/offline_handler.py
- [ ] T054 [US4] Add validation and error handling for local storage
- [ ] T055 [US4] Add logging for local storage operations

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T056 [P] Documentation updates in docs/
- [ ] T057 Code cleanup and refactoring
- [ ] T058 Performance optimization across all stories
- [ ] T059 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T060 Security hardening
- [ ] T061 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

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
Task: "Contract test for email MCP server in tests/contract/test_email_mcp.py"
Task: "Integration test for email processing workflow in tests/integration/test_email_workflow.py"

# Launch all models for User Story 1 together:
Task: "Create PersonalAffair model in src/models/personal_affair.py"
Task: "Create CompanyHandbookRule model in src/models/company_handbook_rule.py"
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
# Implementation Plan: Personal AI Employee

**Branch**: `1-ai-employee` | **Date**: 2026-02-10 | **Spec**: /specs/1-ai-employee/spec.md
**Input**: Feature specification from `/specs/1-ai-employee/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a "Digital FTE" (Full-Time Equivalent) - an AI agent powered by Claude Code and Obsidian that proactively manages personal and business affairs 24/7. The system will use Python watcher scripts to monitor Gmail, WhatsApp, and filesystems, with Claude Code as the reasoning engine and MCP servers for external actions. The architecture emphasizes local-first processing, human-in-the-loop safety for critical actions, and file-based state management in Obsidian vault.

## Technical Context

**Language/Version**: Python 3.13 (for watcher scripts and orchestrator), JavaScript/TypeScript (for MCP servers), Markdown (for Obsidian vault)
**Primary Dependencies**: Claude Code (reasoning engine), Obsidian (knowledge base), Google APIs Client Library (Gmail integration), Playwright (WhatsApp Web automation), Watchdog (filesystem monitoring), Node.js (MCP servers)
**Storage**: Local filesystem (Obsidian vault in Markdown format), with temporary logs and state files
**Testing**: pytest (for Python components), with integration tests for end-to-end workflows
**Target Platform**: Cross-platform desktop application (Windows, macOS, Linux) with local execution
**Project Type**: Single project with modular components
**Performance Goals**: Sub-second response to file system events, continuous monitoring with <5% CPU usage during idle periods
**Constraints**: All data remains local by default, external API calls only when necessary, human approval required for sensitive actions
**Scale/Scope**: Single-user system, designed for individual productivity enhancement

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Local-First Architecture**: Solution keeps data and processing on user's local machine by default - COMPLIANT (Obsidian vault, local Claude Code execution)
- **Human-in-the-Loop Safety**: Critical actions require explicit human approval through file-based workflows - COMPLIANT (approval request files in /Pending_Approval/)
- **Agentic Autonomy with Guardrails**: AI operates autonomously within well-defined boundaries - COMPLIANT (Company Handbook rules, permission boundaries)
- **File-Based State Management**: All system state represented as files in Obsidian vault - COMPLIANT (Needs_Action, Plans, Done, Logs folders)
- **Modular Component Architecture**: Components are modular, interchangeable, and independently testable - COMPLIANT (separate watcher, MCP, orchestrator modules)
- **Security-First Design**: Security measures are foundational, not afterthoughts - COMPLIANT (credential management, audit logging, permission boundaries)

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-employee/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── watchers/            # Python watcher scripts (Gmail, WhatsApp, File System)
│   ├── base_watcher.py
│   ├── gmail_watcher.py
│   ├── whatsapp_watcher.py
│   └── filesystem_watcher.py
├── orchestrator/        # Main orchestrator and watchdog processes
│   ├── orchestrator.py
│   └── watchdog.py
├── mcp-servers/         # MCP server implementations
│   ├── email-mcp/
│   ├── browser-mcp/
│   └── filesystem-mcp/
├── skills/              # Claude Code agent skills
│   ├── email_skills.py
│   ├── finance_skills.py
│   └── social_skills.py
└── utils/               # Utility functions and helpers
    ├── audit_logger.py
    ├── config_loader.py
    └── retry_handler.py

tests/
├── unit/
│   ├── test_watchers/
│   ├── test_orchestrator/
│   └── test_utils/
├── integration/
│   ├── test_end_to_end.py
│   └── test_mcp_integration.py
└── contract/
    └── mcp_contracts/
```

**Structure Decision**: Selected single project structure with modular components organized by functionality. This approach allows for independent development and testing of each component (watchers, orchestrator, MCP servers) while maintaining a cohesive system. The modular design supports the constitutional requirement for modular component architecture.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (None) | | |

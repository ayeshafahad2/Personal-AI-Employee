<!-- 
SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.0.0 (initial version)
Modified principles: 6 principles added
Added sections: Core Principles, Architecture Requirements, Development Workflow, Governance
Removed sections: None
Templates requiring updates: N/A (initial constitution)
Follow-up TODOs: None
-->

# Personal AI Employee Hackathon Constitution

## Core Principles

### I. Local-First Architecture
All data and processing must remain on the user's local machine by default. External services should only be used when absolutely necessary for functionality (e.g., sending emails via Gmail API). Obsidian serves as the primary knowledge base and dashboard, ensuring privacy and control remain with the user.

### II. Human-in-the-Loop Safety
Critical actions (payments, sensitive communications, irreversible operations) must require explicit human approval through file-based approval workflows. The system should create approval request files in `/Pending_Approval/` that humans must move to `/Approved/` or `/Rejected/` to proceed.

### III. Agentic Autonomy with Guardrails
AI employees should operate autonomously using Claude Code as the reasoning engine, but within well-defined boundaries. The "Ralph Wiggum" loop pattern ensures tasks continue until completion, while permission boundaries prevent unauthorized actions.

### IV. File-Based State Management
All system state, tasks, plans, and logs must be represented as files in the Obsidian vault. This creates an auditable trail and enables deterministic state management. Folder structure (`/Needs_Action/`, `/Plans/`, `/Done/`, `/Logs/`) defines the workflow lifecycle.

### V. Modular Component Architecture
The system must be built with modular, interchangeable components: Watchers (Gmail, WhatsApp, File System), MCP servers (Email, Browser, Calendar), and Claude Code reasoning engine. Components should be independently testable and replaceable.

### VI. Security-First Design
Credential management, audit logging, and permission boundaries are foundational requirements, not afterthoughts. All credentials must be stored securely using environment variables or dedicated secret managers, never in plain text or the Obsidian vault.

## Architecture Requirements

### Technology Stack
- **Knowledge Base**: Obsidian (local Markdown vault)
- **Reasoning Engine**: Claude Code with file system tools
- **Perception**: Python Watcher scripts (Gmail, WhatsApp, File System)
- **Action**: Model Context Protocol (MCP) servers
- **Orchestration**: Python-based Orchestrator and Watchdog processes

### Security Requirements
- Never store credentials in plain text or in the Obsidian vault
- Use environment variables or secure credential managers
- Implement comprehensive audit logging for all actions
- Apply permission boundaries based on action sensitivity
- Encrypt sensitive data at rest when possible

### Performance Standards
- Watcher scripts must run continuously with health monitoring
- Claude Code must process tasks within reasonable timeframes
- MCP servers must respond reliably to action requests
- System must handle transient failures gracefully with retry logic

## Development Workflow

### Tiered Development Approach
Projects must follow a tiered development approach with clear milestones:
- **Bronze Tier**: Foundation (8-12 hours) - Basic vault structure, one watcher, Claude integration
- **Silver Tier**: Functional Assistant (20-30 hours) - Multiple watchers, MCP server, approval workflows
- **Gold Tier**: Autonomous Employee (40+ hours) - Full integration, audit features, comprehensive logging
- **Platinum Tier**: Production Deployment (60+ hours) - Cloud deployment, advanced synchronization

### Quality Gates
- All functionality must be implemented as Agent Skills
- Proper error handling and recovery mechanisms required
- Comprehensive audit logging for all actions
- Security measures must be implemented according to guidelines
- Documentation and demo video required for submission

### Review Process
- Functionality (30%): Core features must work correctly
- Innovation (25%): Creative solutions and novel integrations
- Practicality (20%): Daily usability and real-world applicability
- Security (15%): Proper credential handling and safeguards
- Documentation (10%): Clear setup instructions and architecture overview

## Governance

This constitution governs all development activities within the Personal AI Employee Hackathon. All participants must adhere to these principles and requirements. Amendments to this constitution require documentation of the change, approval from hackathon organizers, and a migration plan for existing projects.

All projects must use Claude Code as the primary reasoning engine and implement proper human-in-the-loop safeguards. The architecture must follow the local-first, security-first principles outlined herein.

**Version**: 1.0.0 | **Ratified**: 2026-02-10 | **Last Amended**: 2026-02-10

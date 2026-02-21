# Research: Personal AI Employee

## Decision: Technology Stack Selection
**Rationale**: Selected Python 3.13 for watcher scripts and orchestrator due to strong ecosystem for file system monitoring, API integration, and automation. Node.js for MCP servers as it's the standard runtime for Claude Code MCP implementations. Obsidian for knowledge management due to its local-first architecture and Markdown-based storage.

**Alternatives considered**:
- Using Node.js for all components: Rejected because Python has superior libraries for file system monitoring and API integrations
- Using a database instead of Obsidian: Rejected because it violates the local-first principle and adds complexity

## Decision: Architecture Pattern
**Rationale**: Chose file-based state management with Obsidian vault as the central hub to comply with the local-first and security-first principles. The folder structure (Needs_Action, Plans, Done, Logs) provides a clear workflow lifecycle that's auditable and deterministic.

**Alternatives considered**:
- Database-backed state management: Rejected because it violates the local-first principle
- Cloud-synced storage: Rejected because it compromises privacy and control

## Decision: Human-in-the-Loop Implementation
**Rationale**: Implemented file-based approval workflow where sensitive actions create files in /Pending_Approval/ that require human intervention. This provides clear audit trail and maintains human control over critical actions.

**Alternatives considered**:
- Interactive prompts during Claude Code execution: Rejected because it breaks the autonomous operation principle
- Email notifications for approvals: Rejected because it adds external dependencies

## Decision: Watcher Implementation Strategy
**Rationale**: Created a base watcher class with specific implementations for different services (Gmail, WhatsApp, filesystem). This satisfies the modular component architecture requirement while allowing for standardized monitoring patterns.

**Alternatives considered**:
- Single monolithic watcher: Rejected because it violates modularity principles
- External monitoring services: Rejected because it violates local-first principle

## Decision: MCP Server Design
**Rationale**: Designed MCP servers to handle specific external actions (email, browser automation, file system) to maintain separation of concerns and satisfy the modular architecture requirement.

**Alternatives considered**:
- Single general-purpose MCP server: Rejected because it reduces modularity and increases complexity
- Direct API calls from Claude Code: Rejected because it bypasses proper abstraction layers

## Decision: Security Implementation
**Rationale**: Implemented credential management using environment variables and OS-level credential storage, with comprehensive audit logging for all actions. This addresses security-first design principle.

**Alternatives considered**:
- Storing credentials in Obsidian vault: Rejected because it violates security principles
- Minimal logging: Rejected because it doesn't provide sufficient audit capability
# Data Model: Personal AI Employee

## Key Entities

### PersonalAffair
Represents personal communications or events (emails, messages, transactions) that require attention

**Fields**:
- id: Unique identifier for the affair
- source: Source of the affair (Gmail, WhatsApp, File System, etc.)
- content: Raw content of the communication/event
- timestamp: When the affair was detected
- priority: Priority level (high, medium, low)
- status: Current status (pending, escalated, resolved)
- actions_taken: List of actions taken on this affair

**Validation rules**:
- Must have a valid source
- Must have a timestamp
- Priority must be one of the defined values

### BusinessTask
Represents business-related activities (social posts, payments, project updates) that need processing

**Fields**:
- id: Unique identifier for the task
- type: Type of business task (payment, social_post, report_generation, etc.)
- description: Detailed description of the task
- due_date: When the task is due
- status: Current status (pending, in_progress, completed, failed)
- assigned_to: Who the task is assigned to (human or AI)
- dependencies: Other tasks this task depends on

**Validation rules**:
- Must have a valid type
- Due date must be in the future if set
- Status must be one of the defined values

### ApprovalRequest
Represents actions that require human approval before execution

**Fields**:
- id: Unique identifier for the approval request
- action_type: Type of action requiring approval (payment, email_send, file_delete, etc.)
- details: Detailed information about the action
- requested_by: Who requested the action (AI or human)
- created_at: When the request was created
- expires_at: When the request expires
- status: Current status (pending, approved, rejected)
- approved_by: Who approved the request (when approved)

**Validation rules**:
- Must have a valid action type
- Created at must be before expires at
- Status must be one of the defined values

### CompanyHandbookRule
Represents user-defined rules for how the AI should handle different types of requests

**Fields**:
- id: Unique identifier for the rule
- trigger: Condition that triggers the rule (keyword, sender, etc.)
- action: Action to take when triggered (auto_reply, escalate, ignore, etc.)
- priority: Priority of the rule (higher number means higher priority)
- enabled: Whether the rule is currently active
- created_at: When the rule was created
- last_modified: When the rule was last modified

**Validation rules**:
- Must have a valid trigger and action
- Priority must be a positive integer
- Enabled must be boolean

### WeeklyReport
Represents the generated CEO briefing with business metrics and insights

**Fields**:
- id: Unique identifier for the report
- period_start: Start date of the reporting period
- period_end: End date of the reporting period
- generated_at: When the report was generated
- revenue_summary: Summary of revenue for the period
- completed_tasks: List of completed tasks
- bottlenecks: Identified bottlenecks during the period
- proactive_suggestions: Suggestions for improvements
- upcoming_deadlines: Upcoming deadlines and events

**Validation rules**:
- Period start must be before period end
- Generated at must be within the reporting period
- Revenue summary must be a valid monetary amount if present

## State Transitions

### PersonalAffair State Transitions
- `pending` → `escalated` when AI determines human intervention needed
- `pending` → `resolved` when AI handles automatically
- `escalated` → `resolved` when human handles

### BusinessTask State Transitions
- `pending` → `in_progress` when processing starts
- `in_progress` → `completed` when task finishes successfully
- `in_progress` → `failed` when task encounters an error
- `failed` → `pending` when retry is initiated

### ApprovalRequest State Transitions
- `pending` → `approved` when human approves
- `pending` → `rejected` when human rejects
- `pending` → `expired` when request expires

## Relationships

- PersonalAffair may generate BusinessTask (e.g., an email requesting an invoice creates a task to generate and send invoice)
- CompanyHandbookRule applies to PersonalAffair (rules determine how to handle affairs)
- ApprovalRequest may be created by BusinessTask (when task requires human approval)
- WeeklyReport aggregates data from multiple BusinessTask and PersonalAffair instances
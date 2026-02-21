# Personal AI Employee - Silver Tier Implementation

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

A comprehensive autonomous AI agent system that proactively manages personal and business affairs 24/7 using **Qwen** or **Claude Code** as the reasoning engine and Obsidian as the management dashboard.

## 🏆 Silver Tier Status: ✅ COMPLETE

This implementation satisfies all **Silver Tier** requirements for the Personal AI Employee Hackathon:

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| All Bronze requirements | ✅ Complete | Vault, watchers, AI integration |
| Two+ Watcher scripts | ✅ Complete | Gmail + FileSystem watchers |
| LinkedIn auto-posting | ✅ Complete | Integrated with vault logging |
| AI reasoning + Plan.md | ✅ Complete | Orchestrator creates plans |
| MCP server for external actions | ✅ Complete | Email + Browser + LinkedIn MCPs |
| HITL approval workflow | ✅ Complete | Pending_Approval + HITL processor |
| Scheduling (cron/Task Scheduler) | ✅ Complete | scheduler.py with auto-install |

## 🤖 AI Backend Support

The system supports multiple AI backends:

| AI Backend | Configuration | Use Case |
|------------|---------------|----------|
| **Qwen API** | `AI_COMMAND=qwen` | Cloud-based, pay-per-use |
| **Claude Code CLI** | `AI_COMMAND=claude` | Local CLI tool |

**Default:** Qwen API (configured in `.env`)

See `QWEN_SETUP.md` for detailed Qwen configuration.

## 📁 Project Structure

```
Hackathon-0/
├── AI_Employee_Vault/          # Obsidian vault
│   ├── Inbox/                  # Drop folder for files
│   ├── Needs_Action/           # Items awaiting processing
│   ├── Plans/                  # Claude's planning documents
│   ├── Done/                   # Completed items
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Approved actions
│   ├── Rejected/               # Rejected actions
│   ├── Logs/                   # System logs
│   ├── Briefings/              # CEO briefings
│   ├── Dashboard.md            # Real-time status dashboard
│   ├── Company_Handbook.md     # Rules of engagement
│   └── Business_Goals.md       # Q1 2026 objectives
│
├── watchers/
│   ├── base_watcher.py         # Base class for all watchers
│   ├── gmail_watcher.py        # Gmail monitoring
│   └── filesystem_watcher.py   # File system monitoring
│
├── mcp_*.py                    # MCP Servers
│   ├── mcp_email_server.py     # Email actions MCP
│   ├── mcp_browser_server.py   # Browser automation MCP
│   └── mcp_linkedin_server.py  # LinkedIn posting MCP
│
├── orchestrator.py             # Master orchestration (creates Plan.md)
├── agent_skills.py             # Reusable agent skills
├── hitl_processor.py           # Human-in-the-loop processor
├── scheduler.py                # Task scheduler (cron/Windows)
├── ralph_wiggum.py             # Autonomous loop pattern
│
├── auto_post_manager.py        # LinkedIn + WhatsApp automation
├── linkedin_auto_publisher.py  # LinkedIn API publisher
├── whatsapp_notifier.py        # Twilio WhatsApp notifications
│
├── requirements.txt            # Python dependencies
├── mcp.json                    # MCP configuration for Claude Code
├── .env                        # Environment variables
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install mcp  # For MCP servers
playwright install  # For browser automation
```

### 2. Configure Environment

Update `.env` with your credentials:

```env
# AI Assistant Configuration
AI_COMMAND=qwen                    # 'qwen' for Qwen API, 'claude' for CLI
DASHSCOPE_API_KEY=sk-your-key      # Get from https://dashscope.console.aliyun.com/

# Gmail
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_TOKEN_PATH=token.json

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
WHATSAPP_RECIPIENT_NUMBER=whatsapp:+923298374240

# LinkedIn
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_secret
LINKEDIN_ACCESS_TOKEN=your_token
```

### 3. Authenticate Services

```bash
# Gmail OAuth
python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault

# Twilio WhatsApp - send this message:
# join <sandbox-code> to +14155238886
```

### 4. Configure MCP Servers (Optional)

If using MCP servers with Qwen, add to your AI configuration:

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["E:\\Hackathon-0\\mcp_email_server.py"]
    },
    "browser": {
      "command": "python",
      "args": ["E:\\Hackathon-0\\mcp_browser_server.py"]
    },
    "linkedin": {
      "command": "python",
      "args": ["E:\\Hackathon-0\\mcp_linkedin_server.py"]
    }
  }
}
```

Or use the provided `mcp.json` as reference.

### 5. Install Scheduler (Optional)

**Windows:**
```bash
python scheduler.py --install
# Then run the PowerShell scripts as Administrator
```

**Linux/Mac:**
```bash
python scheduler.py --install
# Then: crontab install_cron_jobs.txt
```

## 📋 Component Overview

### Perception Layer (Watchers)

| Watcher | File | Purpose |
|---------|------|---------|
| Gmail | `watchers/gmail_watcher.py` | Monitor unread emails |
| FileSystem | `watchers/filesystem_watcher.py` | Monitor drop folder |

### Reasoning Layer (Claude Code)

| Component | File | Purpose |
|-----------|------|---------|
| Orchestrator | `orchestrator.py` | Process items, create plans |
| Ralph Wiggum | `ralph_wiggum.py` | Autonomous loop until done |
| Agent Skills | `agent_skills.py` | Reusable capabilities |

### Action Layer (MCP Servers)

| MCP Server | File | Capabilities |
|------------|------|--------------|
| Email | `mcp_email_server.py` | send_email, draft_email, search_emails |
| Browser | `mcp_browser_server.py` | navigate, click, fill, screenshot |
| LinkedIn | `mcp_linkedin_server.py` | publish_post, publish_from_file |

### Human-in-the-Loop

| Component | File | Purpose |
|-----------|------|---------|
| HITL Processor | `hitl_processor.py` | Execute approved actions |
| Approval Folders | `Pending_Approval/`, `Approved/` | Workflow management |

### Scheduling

| Component | File | Purpose |
|-----------|------|---------|
| Scheduler | `scheduler.py` | cron/Task Scheduler integration |

## 🎯 Usage Examples

### Process Needs_Action Folder

```bash
python orchestrator.py --process --vault AI_Employee_Vault
```

### Run Autonomous Loop

```bash
python ralph_wiggum.py "Process all emails and create weekly report" \
  --vault AI_Employee_Vault \
  --max-iterations 5
```

### Process Approved Actions

```bash
python hitl_processor.py --process --vault AI_Employee_Vault
```

### Generate CEO Briefing

```bash
python orchestrator.py --briefing --vault AI_Employee_Vault
```

### Start Watchers

```bash
# Gmail Watcher
python watchers/gmail_watcher.py --vault AI_Employee_Vault

# FileSystem Watcher
python watchers/filesystem_watcher.py --vault AI_Employee_Vault
```

### Run All Tasks Now

```bash
python scheduler.py --run
```

### Post to LinkedIn with WhatsApp Notification

```bash
python auto_post_manager.py --post "Your post content here"
```

## 🔄 Workflow Examples

### Email Processing Flow

```
1. Gmail Watcher detects new unread email
2. Creates action file in Needs_Action/
3. Orchestrator picks up action file
4. Creates Plan.md in Plans/
5. Claude Code processes with MCP tools
6. If approval needed → Pending_Approval/
7. If auto-approved → Execute via MCP
8. Move to Done/ when complete
```

### Approval Workflow

```
1. Claude creates approval request in Pending_Approval/
2. Human reviews file
3. Human moves file to Approved/
4. HITL Processor detects approved file
5. Executes the approved action
6. Moves file to Done/
7. Updates Dashboard
```

### LinkedIn Auto-Post Flow

```
1. Create post content file in Needs_Action/
2. Orchestrator creates Plan.md
3. Claude reviews against Company_Handbook.md
4. Creates approval request
5. Human approves (moves to Approved/)
6. MCP LinkedIn server publishes
7. WhatsApp notification sent
8. Logged to vault Dashboard
```

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SOURCES                         │
│  Gmail  │  WhatsApp  │  LinkedIn  │  Bank APIs  │  Files   │
└────┬────────────┬─────────────┬───────────┬────────┬────────┘
     │            │             │           │        │
     ▼            ▼             ▼           ▼        ▼
┌─────────────────────────────────────────────────────────────┐
│                    PERCEPTION LAYER                         │
│  ┌────────────┐ ┌─────────────┐ ┌──────────────────────┐   │
│  │Gmail Watcher│ │File Watcher │ │LinkedIn Auto-Poster  │   │
│  └─────┬──────┘ └──────┬──────┘ └──────────┬───────────┘   │
└────────┼────────────────┼──────────────────┼────────────────┘
         │                │                  │
         ▼                ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT                           │
│  /Needs_Action  │  /Plans  │  /Done  │  /Pending_Approval  │
│  Dashboard.md   │  Company_Handbook.md  │  Business_Goals.md│
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    REASONING LAYER                          │
│                    CLAUDE CODE                              │
│         Read → Create Plan → Think → Act → Approve          │
└─────────────────────────┬───────────────────────────────────┘
                          │
              ┌───────────┴────────────┐
              ▼                        ▼
┌──────────────────────┐    ┌──────────────────────────────────┐
│  HUMAN-IN-THE-LOOP   │    │         ACTION LAYER (MCP)       │
│  Review & Approve    │    │  ┌────────────────────────────┐  │
│  /Pending_Approval   │    │  │ email: send, draft, search │  │
│  /Approved           │    │  │ browser: navigate, click   │  │
│  /Rejected           │    │  │ linkedin: publish_post     │  │
│                      │    │  │ filesystem: read, write    │  │
└──────────────────────┘    │  └────────────────────────────┘  │
                            └──────────────────────────────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │    SCHEDULER         │
                          │  cron / Task Scheduler│
                          │  - Every 5 min: process│
                          │  - Every 2 min: HITL  │
                          │  - Mon 8 AM: briefing │
                          └──────────────────────┘
```

## 🔒 Security

### Credential Management

- **Never commit `.env`** - Contains API keys and tokens
- **Use environment variables** - All credentials via `.env`
- **Rotate credentials monthly** - Especially for production use

### Human-in-the-Loop Approval Matrix

| Action Category | Auto-Approve | Require Approval |
|-----------------|--------------|------------------|
| Email replies | Known contacts | New contacts, bulk sends |
| Payments | < $50 recurring | All new payees, > $100 |
| LinkedIn posts | Draft only | All posts (review required) |
| File operations | Create, read | Delete, move outside vault |
| Browser actions | Read-only | Form fills, clicks, payments |

### Audit Logging

All actions logged to `Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-02-17T10:30:00Z",
  "action_type": "email_send",
  "actor": "mcp_email_server",
  "parameters": {"to": "client@email.com", "subject": "Invoice"},
  "result": "success"
}
```

## 🛠️ Troubleshooting

### MCP Servers Not Working

```bash
# Test MCP server directly
python mcp_email_server.py

# Check MCP SDK installed
pip install mcp

# Verify Claude Code configuration
# ~/.config/claude-code/settings.json
```

### Gmail Watcher Not Working

```bash
# Re-authenticate
python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault

# Check token exists
ls token.json
```

### Scheduler Not Running

**Windows:**
1. Open Task Scheduler
2. Check "AI_Employee" folder
3. Verify tasks are enabled
4. Check task history for errors

**Linux:**
```bash
# Check cron logs
grep CRON /var/log/syslog

# Verify crontab
crontab -l
```

### Claude Code Not Found

```bash
# Install Claude Code
npm install -g @anthropic/claude-code

# Or set custom path
export CLAUDE_COMMAND=/path/to/claude
```

## 📈 Tier Progress

| Tier | Status | Components |
|------|--------|------------|
| **Bronze** | ✅ Complete | Vault, Gmail Watcher, FS Watcher, Claude integration |
| **Silver** | ✅ Complete | MCP servers, HITL workflow, Scheduler, Plan.md |
| **Gold** | ⬜ Pending | Odoo integration, Facebook/Instagram/Twitter, Accounting |
| **Platinum** | ⬜ Pending | Cloud deployment, 24/7 operation, Synced vault |

## 🎓 Learning Resources

- [Claude Code Fundamentals](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Server Examples](https://github.com/anthropics/mcp-servers)
- [Twilio WhatsApp Docs](https://www.twilio.com/docs/whatsapp)
- [Gmail API Quickstart](https://developers.google.com/gmail/api/quickstart)
- [Playwright Docs](https://playwright.dev/)

## 📝 Hackathon Submission

### Submission Requirements

- ✅ GitHub repository with all code
- ✅ README.md with setup instructions (this file)
- ✅ Demo video (5-10 minutes)
- ✅ Security disclosure (credentials handled via .env)
- ✅ Tier declaration: **Silver Tier**

### Demo Video Outline

1. Show Obsidian vault structure (1 min)
2. Demonstrate Gmail Watcher creating action files (2 min)
3. Show Claude Code processing with Plan.md creation (2 min)
4. Demonstrate HITL approval workflow (2 min)
5. Show MCP servers in action (1 min)
6. Show scheduler installation (1 min)
7. Show LinkedIn auto-posting + WhatsApp notification (1 min)

## 🔧 Development

### Adding New MCP Servers

1. Create `mcp_<name>_server.py` following existing pattern
2. Define tools with `@server.list_tools()`
3. Implement tool calls with `@server.call_tool()`
4. Add to `mcp.json` configuration
5. Update Claude Code settings

### Adding New Watchers

1. Create `watchers/<name>_watcher.py`
2. Inherit from `BaseWatcher`
3. Implement `check_for_updates()` and `create_action_file()`
4. Add to orchestrator watcher list

### Customizing Approval Rules

Edit `hitl_processor.py`:
- Modify approval matrix in `_execute_approval()`
- Add new action type handlers
- Adjust expiry time via `APPROVAL_EXPIRY_HOURS` env var

## 📄 License

MIT License - See LICENSE file

---

**Built with ❤️ for Personal AI Employee Hackathon 0**

*Your Digital FTE working 24/7*

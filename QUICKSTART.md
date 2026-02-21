# Quickstart Guide: Personal AI Employee

## Welcome to Your Personal AI Employee! 🤖💼

Transform your life and business with an autonomous AI employee that works 24/7. This guide will help you set up your "Digital FTE" in under 30 minutes.

## Prerequisites

### Software Requirements
- **Python 3.13+** - For watcher scripts and orchestrator
- **Node.js v24+ LTS** - For MCP servers
- **Claude Code** - Pro subscription (reasoning engine)
- **Obsidian** - v1.10.6+ (knowledge base & dashboard)

### Hardware Requirements
- **Recommended**: 8GB+ RAM, 4+ core CPU, SSD storage
- **Internet**: Stable connection (10+ Mbps recommended)

## Step 1: Download & Setup

1. Clone or download this repository to your computer
2. Navigate to the project directory:
   ```bash
   cd Hackathon-0
   ```

## Step 2: Install Dependencies

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browsers (needed for WhatsApp automation):
   ```bash
   playwright install msedge
   ```

3. Install Node.js dependencies for MCP servers:
   ```bash
   cd src/mcp-servers/email-mcp
   npm install
   cd ../../..
   ```

## Step 3: Configure Your Credentials

1. The `.env` file is already configured with the provided Gmail credentials:
   ```
   GMAIL_CLIENT_ID=YOUR_GMAIL_CLIENT_ID.apps.googleusercontent.com
   GMAIL_CLIENT_SECRET=GOCSPX-YOUR_GMAIL_SECRET_HERE
   GMAIL_PROJECT_ID=mcp-gmail-agent-487020
   GMAIL_REDIRECT_URI=http://localhost
   ```

2. **Important**: The first time you run the Gmail watcher, you'll need to authenticate with Google. This will open a browser window where you'll log in and grant permissions.

## Step 4: Configure LinkedIn Integration

1. The `.env` file is already configured with your LinkedIn credentials:
   ```
   LINKEDIN_CLIENT_ID=7763qv2uyw7eao
   LINKEDIN_CLIENT_SECRET=WPL_AP1.YOUR_LINKEDIN_SECRET_HERE
   LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token_here
   LINKEDIN_REFRESH_TOKEN=your_linkedin_refresh_token_here
   LINKEDIN_REDIRECT_URI=http://localhost
   ```

2. **Important**: You need to obtain a valid LinkedIn access token. Follow the instructions in `LINKEDIN_WATCHER_README.md` to generate your access token.

## Step 5: Set Up Your Obsidian Vault

The AI Employee uses Obsidian as its knowledge base. We've created the basic structure:

```
AI_Employee_Vault/
├── Dashboard.md              # Real-time summary
├── Company_Handbook.md       # Your rules of engagement
├── Business_Goals.md         # Business objectives
├── Needs_Action/             # Items requiring attention
├── Plans/                    # Claude-generated plans
├── Done/                     # Completed items
├── Logs/                     # System logs
├── Pending_Approval/         # Approval requests
├── Approved/                 # Approved items
├── Rejected/                 # Rejected items
├── Accounting/               # Financial records
└── Briefings/                # CEO briefings
```

## Step 6: Configure Claude Code

1. Configure MCP servers in your Claude Code settings (`~/.config/claude-code/mcp.json`):

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["E:/Hackathon-0/src/mcp-servers/email-mcp/index.js"],
      "env": {
        "GMAIL_CLIENT_ID": "YOUR_GMAIL_CLIENT_ID.apps.googleusercontent.com",
        "GMAIL_CLIENT_SECRET": "GOCSPX-YOUR_GMAIL_SECRET_HERE",
        "GMAIL_PROJECT_ID": "mcp-gmail-agent-487020"
      }
    }
  ]
}
```

## Step 7: Start Your AI Employee

1. **Start Claude Code** in your AI_Employee_Vault directory:
   ```bash
   claude --cwd "E:\Hackathon-0\AI_Employee_Vault"
   ```

2. **Start the orchestrator** in a separate terminal:
   ```bash
   python src/orchestrator/orchestrator.py
   ```

3. **Authenticate with Gmail** when prompted (first run only)

## Step 8: Customize Your Company Handbook

Review and customize `AI_Employee_Vault/Company_Handbook.md` to define how your AI employee should handle different situations:

- Email handling rules
- WhatsApp response protocols
- Business task priorities
- Approval requirements
- Working hours and escalation triggers

## What Happens Next?

### Your AI Employee Will:
- **Monitor Gmail** for important messages and create action files in `Needs_Action/`
- **Monitor WhatsApp** for messages with important keywords and create action files
- **Monitor LinkedIn** for important messages, posts, and networking opportunities
- **Process action files** using Claude Code to generate plans
- **Request approvals** for sensitive actions via file-based workflow
- **Generate reports** like the "Monday Morning CEO Briefing"

### You'll See:
- Action files created in `AI_Employee_Vault/Needs_Action/` when important communications arrive
- Plan files in `AI_Employee_Vault/Plans/` as Claude processes requests
- Approval request files in `AI_Employee_Vault/Pending_Approval/` for sensitive actions
- Updates in `AI_Employee_Vault/Dashboard.md` with system status

## First Week: "Monday Morning CEO Briefing"

Every Sunday night, your AI employee will generate a comprehensive report in `AI_Employee_Vault/Briefings/` including:
- Revenue summary
- Completed tasks
- Bottlenecks identified
- Cost optimization suggestions
- Upcoming deadlines

## Security & Privacy

- All data stays local on your machine
- Credentials are stored securely in environment variables
- Human approval required for sensitive actions
- Comprehensive audit logging for all activities

## Troubleshooting

### Common Issues:
- **"Command not found"**: Ensure Claude Code is installed globally
- **Gmail API returns 403**: Check OAuth consent screen verification
- **WhatsApp watcher stops**: Use PM2 for process management

### Performance Tips:
- Use a dedicated machine for 24/7 operation
- Implement proper error handling and retry logic
- Set up process monitoring to restart services if they fail

## Next Steps

1. **Test the system** with a few emails and WhatsApp messages
2. **Refine your Company Handbook** rules based on initial results
3. **Expand functionality** by adding more watchers or MCP servers
4. **Join our Wednesday meetings** for ongoing support and enhancements

---

**🎉 Congratulations! Your Personal AI Employee is now operational. Sit back, relax, and let your AI employee handle your personal and business affairs while you focus on what matters most.**

Need help? Join our research meetings every Wednesday at 10:00 PM (details in the main documentation).
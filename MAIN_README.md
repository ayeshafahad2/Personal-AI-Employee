# Personal AI Employee Hackathon 0: Building Autonomous FTEs (Full-Time Equivalent) in 2026

**Tagline**: Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

This repository contains a complete implementation of a "Digital FTE" (Full-Time Equivalent) - an AI agent powered by Claude Code and Obsidian that proactively manages personal and business affairs 24/7. You can also think of it as a "Smart Consultant" (General Agents). The focus is on high-level reasoning, autonomy, and flexibility. Think of it as hiring a senior employee who figures out how to solve the problems.

## 🚀 Features

### Dashboard Interface
- **Professional & Creative Design**: Stunning Next.js dashboard with real-time monitoring
- **Activity Feed**: Chronological timeline of AI employee activities
- **Task Management**: View and manage pending tasks
- **Communication Hub**: Monitor Gmail and WhatsApp interactions
- **Approval Queue**: Handle sensitive actions requiring human approval
- **Performance Metrics**: Track system performance and efficiency
- **Responsive Design**: Works beautifully on all devices

### Core Functionality
- **Gmail Watcher**: Monitors Gmail for important messages using Gmail API
- **WhatsApp Watcher**: Monitors WhatsApp for messages with specified keywords
- **LinkedIn Watcher**: Monitors LinkedIn for important messages, posts, and networking opportunities
- **File-Based State Management**: All system state represented as files in Obsidian vault
- **Human-in-the-Loop Safety**: Critical actions require explicit human approval through file-based workflows
- **Agentic Autonomy with Guardrails**: AI operates autonomously within well-defined boundaries
- **Local-First Architecture**: All data and processing remains on user's local machine by default

## 🏗️ Architecture

### The Brain
- **Claude Code**: Acts as the reasoning engine with Ralph Wiggum Stop hook for continuous iteration

### The Memory/GUI
- **Obsidian**: Local Markdown vault as the dashboard, keeping data local and accessible

### The Senses (Watchers)
- **Gmail Watcher**: Monitors Gmail using Python and Google APIs
- **WhatsApp Watcher**: Monitors WhatsApp using Playwright automation
- **LinkedIn Watcher**: Monitors LinkedIn using LinkedIn APIs
- **File System Watcher**: Monitors local filesystems

### The Hands (MCP)
- **Model Context Protocol (MCP) servers**: Handle external actions like sending emails or clicking buttons

## 📁 Project Structure

```
E:\Hackathon-0\
├── AI_Employee_Vault/              # Obsidian vault
│   ├── Dashboard.md                # Real-time summary
│   ├── Company_Handbook.md         # Rules of engagement
│   ├── Business_Goals.md           # Business objectives
│   ├── Needs_Action/               # Items requiring attention
│   ├── Plans/                      # Claude-generated plans
│   ├── Done/                       # Completed items
│   ├── Logs/                       # System logs
│   ├── Pending_Approval/           # Approval requests
│   ├── Approved/                   # Approved items
│   ├── Rejected/                   # Rejected items
│   ├── Accounting/                 # Financial records
│   └── Briefings/                  # CEO briefings
├── dashboard/                      # Next.js dashboard application
│   ├── app/                        # Next.js app router
│   ├── components/                 # React components
│   ├── hooks/                      # Custom React hooks
│   ├── styles/                     # Global styles
│   └── public/                     # Static assets
├── src/
│   ├── watchers/                   # Python watcher scripts
│   ├── orchestrator/               # Main orchestrator and watchdog
│   ├── mcp-servers/                # MCP server implementations
│   ├── skills/                     # Claude Code agent skills
│   └── utils/                      # Utility functions
├── .env                           # Environment variables (Gmail credentials)
├── .claude-config.json            # Claude Code MCP configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🛠️ Prerequisites

### Software Requirements
- **Python 3.13+** - For watcher scripts and orchestrator
- **Node.js v24+ LTS** - For MCP servers and dashboard
- **Claude Code** - Pro subscription (reasoning engine)
- **Obsidian** - v1.10.6+ (knowledge base & dashboard)
- **Git** - For version control

### Hardware Requirements
- **Minimum**: 8GB RAM, 4-core CPU, 20GB free disk space
- **Recommended**: 16GB RAM, 8-core CPU, SSD storage
- **Internet**: Stable connection for API calls (10+ Mbps recommended)

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Hackathon-0
```

### 2. Install Dependencies
```bash
npm run setup
```

### 3. Dashboard Setup
The dashboard is built with Next.js and provides a professional interface for monitoring your AI employee:

```bash
# Run the dashboard in development mode
npm run dev

# Build for production
npm run build

# Run in production
npm start
```

The dashboard will be available at [http://localhost:3000](http://localhost:3000)

### 4. AI Employee Setup
1. Ensure your `.env` file contains the required credentials:
   ```
   GMAIL_CLIENT_ID=YOUR_GMAIL_CLIENT_ID.apps.googleusercontent.com
   GMAIL_CLIENT_SECRET=GOCSPX-YOUR_GMAIL_SECRET_HERE
   GMAIL_PROJECT_ID=mcp-gmail-agent-487020
   GMAIL_REDIRECT_URI=http://localhost
   ```

2. Configure Claude Code MCP servers in your Claude Code settings (`~/.config/claude-code/mcp.json`):
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

### 5. Running the System

#### Option 1: Using Dashboard (Recommended)
1. Start the dashboard: `npm run dev`
2. Open [http://localhost:3000](http://localhost:3000) to monitor your AI employee
3. Start Claude Code in your AI_Employee_Vault directory:
   ```bash
   npm run start-claude
   ```
4. Start the orchestrator in a separate terminal:
   ```bash
   npm run start-ai
   ```

#### Option 2: Manual Start
1. **Start Claude Code** in your AI_Employee_Vault directory:
   ```bash
   claude --cwd "E:/Hackathon-0/AI_Employee_Vault"
   ```

2. **Start the orchestrator** in a separate terminal:
   ```bash
   cd src/orchestrator
   python orchestrator.py
   ```

3. **Monitor the dashboard** at [http://localhost:3000](http://localhost:3000)

## 🎛️ Dashboard Features

### Real-Time Monitoring
- **Activity Feed**: See all actions taken by your AI employee in real-time
- **Task Manager**: Track pending tasks and their status
- **Communication Hub**: Monitor all Gmail and WhatsApp interactions
- **Approval Queue**: Handle sensitive actions requiring your approval
- **Performance Metrics**: Track system performance and efficiency

### Professional Design Elements
- **Modern UI/UX**: Clean, intuitive interface with professional aesthetics
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Real-Time Updates**: Live data refresh without page reloads
- **Visual Indicators**: Color-coded priority levels and status indicators
- **Interactive Elements**: Approve/reject actions directly from the dashboard

## 🔐 Security & Privacy

- **Local-First Architecture**: All data remains on your local machine by default
- **Secure Credential Management**: Credentials stored in environment variables
- **Human-in-the-Loop Safety**: Critical actions require explicit human approval
- **Comprehensive Audit Logging**: All actions logged for review and accountability
- **Permission Boundaries**: Granular controls on what actions can be performed automatically

## 📊 Success Metrics

- **Setup Time**: Under 30 minutes for full deployment
- **Automation Rate**: 90% of routine communications handled automatically
- **Task Completion**: 95% of user tasks completed within expected timeframe
- **Security**: Zero unauthorized transactions without human approval
- **Uptime**: 99% availability for monitoring services
- **Productivity**: 80% reduction in routine administrative tasks

## 🤝 Contributing

We welcome contributions to improve the Personal AI Employee system! Feel free to submit issues and pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, join our research meetings every Wednesday at 10:00 PM via Zoom:
- Meeting ID: 871 8870 7642
- Passcode: 744832

Or watch live recordings on YouTube: https://www.youtube.com/@panaversity

---

**Your life and business on autopilot. Welcome to the future of personal productivity.**
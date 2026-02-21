# Quickstart Guide: Personal AI Employee

## Prerequisites

Before getting started with your Personal AI Employee, ensure you have the following prerequisites in place:

### Required Software
- **Claude Code**: Active subscription (Pro or use Free Gemini API with Claude Code Router) - Primary reasoning engine
- **Obsidian**: v1.10.6+ (free) - Knowledge base & dashboard
- **Python**: 3.13 or higher - Sentinel scripts & orchestration
- **Node.js**: v24+ LTS - MCP servers & automation
- **Github Desktop**: Latest stable - Version control for your vault

### Hardware Requirements
- **Minimum**: 8GB RAM, 4-core CPU, 20GB free disk space
- **Recommended**: 16GB RAM, 8-core CPU, SSD storage
- **For always-on operation**: Consider a dedicated mini-PC or cloud VM
- **Internet**: Stable connection for API calls (10+ Mbps recommended)

### Skill Level Expectations
- Comfortable with command-line interfaces (terminal/bash)
- Understanding of file systems and folder structures
- Familiarity with APIs (what they are, how to call them)
- No prior AI/ML experience required
- Able to use and prompt Claude Code

## Setup Process

### Step 1: Environment Setup
1. Install all required software listed above
2. Verify Claude Code works by running: `claude --version`
3. Set up a UV Python project for dependency management

### Step 2: Create Your AI Employee Vault
1. Create a new Obsidian vault named "AI_Employee_Vault"
2. Inside the vault, create the following folder structure:
   ```
   AI_Employee_Vault/
   ├── Inbox/
   ├── Needs_Action/
   ├── Plans/
   ├── Done/
   ├── Logs/
   ├── Pending_Approval/
   ├── Approved/
   ├── Rejected/
   ├── Accounting/
   │   └── Current_Month.md
   └── Briefings/
   ```

### Step 3: Create Essential Files
1. Create `Dashboard.md` with basic structure:
   ```markdown
   # AI Employee Dashboard
   
   ## Recent Activity
   - [Placeholder for recent activities]
   
   ## Pending Actions
   - [Placeholder for pending actions]
   
   ## Current Status
   - [Placeholder for system status]
   ```

2. Create `Company_Handbook.md` with basic rules:
   ```markdown
   # Company Handbook
   
   ## Rules of Engagement
   - Always be polite on WhatsApp
   - Flag any payment over $500 for my approval
   - Escalate emails from VIP contacts
   - Schedule social media posts for optimal engagement times
   ```

### Step 4: Configure Claude Code
1. Configure MCP servers in your Claude Code settings (`~/.config/claude-code/mcp.json`):
   ```json
   {
     "servers": [
       {
         "name": "email",
         "command": "node",
         "args": ["/path/to/email-mcp/index.js"],
         "env": {
           "GMAIL_CREDENTIALS": "/path/to/credentials.json"
         }
       },
       {
         "name": "browser",
         "command": "npx",
         "args": ["@anthropic/browser-mcp"],
         "env": {
           "HEADLESS": "true"
         }
       }
     ]
   }
   ```

### Step 5: Initialize Watcher Scripts
1. Create the base watcher structure in your project:
   ```python
   # base_watcher.py - Template for all watchers
   import time
   import logging
   from pathlib import Path
   from abc import ABC, abstractmethod
   
   
   class BaseWatcher(ABC):
       def __init__(self, vault_path: str, check_interval: int = 60):
           self.vault_path = Path(vault_path)
           self.needs_action = self.vault_path / 'Needs_Action'
           self.check_interval = check_interval
           self.logger = logging.getLogger(self.__class__.__name__)
           
       @abstractmethod
       def check_for_updates(self) -> list:
           '''Return list of new items to process'''
           pass
       
       @abstractmethod
       def create_action_file(self, item) -> Path:
           '''Create .md file in Needs_Action folder'''
           pass
       
       def run(self):
           self.logger.info(f'Starting {self.__class__.__name__}')
           while True:
               try:
                   items = self.check_for_updates()
                   for item in items:
                       self.create_action_file(item)
               except Exception as e:
                   self.logger.error(f'Error: {e}')
               time.sleep(self.check_interval)
   ```

## Running Your AI Employee

### Starting the System
1. Start your Claude Code session pointing to your AI_Employee_Vault
2. Start your watcher scripts in separate terminals:
   ```bash
   python watchers/gmail_watcher.py
   python watchers/whatsapp_watcher.py
   python watchers/filesystem_watcher.py
   ```
3. Start your orchestrator:
   ```bash
   python orchestrator/orchestrator.py
   ```

### Monitoring and Maintenance
- Check the Dashboard.md regularly for system status
- Monitor the Logs/ folder for any errors or issues
- Review Pending_Approval/ folder for actions requiring your attention
- Update Company_Handbook.md as needed to refine AI behavior

## Troubleshooting

### Common Issues
- **Claude Code not responding**: Ensure it's running in the correct directory with access to the vault
- **Watchers not detecting changes**: Check API credentials and permissions
- **MCP servers not connecting**: Verify configuration in mcp.json and server status

### Performance Tips
- Use a dedicated machine or VM for 24/7 operation
- Implement proper error handling and retry logic
- Set up process monitoring to restart services if they fail
# WhatsApp Watcher Setup and Usage Guide

## Overview
The WhatsApp Watcher is a component of the Personal AI Employee that monitors WhatsApp Web for important messages containing specific keywords and creates action files in the `Needs_Action` folder for processing.

## Prerequisites
- Python 3.8+
- Playwright (`pip install playwright`)
- Microsoft Edge browser (recommended) or Chromium browser

## Setup

### 1. Install Dependencies
Make sure you have Playwright installed:
```bash
pip install -r requirements.txt
playwright install msedge
```

### 2. Prepare Your Vault Directory
Ensure your AI Employee Vault directory is set up with the proper structure:
```
AI_Employee_Vault/
├── Needs_Action/
├── Logs/
└── ...
```

## Usage

### Option 1: Run the WhatsApp Watcher Continuously
```bash
python run_whatsapp_watcher.py [VAULT_PATH]
```

### Option 2: Test the Connection
```bash
python test_whatsapp_connection.py
```

### Option 3: Integrate with the Main Orchestrator
The WhatsApp watcher can be integrated with the main orchestrator system to run alongside other watchers like email monitoring.

## Configuration
The WhatsApp watcher monitors for messages containing these keywords by default:
- urgent
- asap
- invoice
- payment
- help
- important
- needed
- require
- assistance
- meeting
- deadline
- tomorrow
- today
- now
- critical

## Important Notes
1. **WhatsApp Terms of Service**: Be aware that automating WhatsApp Web may violate WhatsApp's Terms of Service. Use responsibly and at your own risk.

2. **Login Requirement**: You need to be logged in to WhatsApp Web in the browser that opens when the watcher runs. If you're not already logged in, you'll need to scan the QR code when prompted.

3. **Session Persistence**: The watcher saves session data to maintain login state between runs.

4. **Headless Mode**: For production use, you can change `headless=False` to `headless=True` in the WhatsApp watcher code.

## Troubleshooting
- If the watcher can't detect your login state, ensure you're properly logged in to WhatsApp Web
- If you receive errors about selectors not being found, WhatsApp Web may have updated its interface
- Check the log file at `[VAULT_PATH]/Logs/watcher.log` for detailed error information
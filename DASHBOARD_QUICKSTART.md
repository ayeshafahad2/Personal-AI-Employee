# 🚀 Dashboard Quick Start

## Your Social Media Command Center is Ready!

### Start the Dashboard (3 Easy Ways)

#### Option 1: Double-Click (Easiest)
1. Double-click `start_dashboard.bat`
2. Dashboard opens automatically at http://localhost:8081
3. Done! ✅

#### Option 2: Command Line
```bash
python dashboard_server.py
```
Then open: http://localhost:8081

#### Option 3: PowerShell
```powershell
.\start_dashboard.bat
```

---

## What You Can Do Now

### ✅ Post to Social Media - No CLI Needed!

1. **Type your message** in the text box
2. **Select platforms** (check boxes) or click a specific platform button
3. **Click "Post to All Selected"** or individual platform button
4. **Watch it happen** - see posts appear in real-time!

### Supported Platforms
- 📧 **Gmail** - Send emails
- 💬 **WhatsApp** - Send messages
- 📸 **Instagram** - Post updates (needs images)
- 💼 **LinkedIn** - Professional posts
- 📘 **Facebook** - Page posts
- 🐦 **Twitter/X** - Tweets

---

## Features

| Feature | Description |
|---------|-------------|
| 📊 **Real-Time Stats** | See total posts and today's posts per platform |
| 📜 **Post History** | View recent posts for each platform |
| 📋 **Activity Logs** | Track all posting activity with timestamps |
| 🔄 **Auto-Refresh** | Dashboard updates every 10 seconds |
| 🎯 **Multi-Post** | Post to multiple platforms at once |

---

## Configuration Required

Before posting, make sure your `.env` file has the correct credentials for each platform you want to use.

**Quick Check:**
```bash
# Twitter
TWITTER_BEARER_TOKEN=your_token

# Facebook  
FACEBOOK_PAGE_ACCESS_TOKEN=your_token

# LinkedIn
LINKEDIN_ACCESS_TOKEN=your_token

# Instagram
INSTAGRAM_PAGE_ACCESS_TOKEN=your_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_id

# Gmail
GMAIL_CLIENT_ID=your_id
GMAIL_CLIENT_SECRET=your_secret

# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
```

**Get help:** See `DASHBOARD_README.md` for detailed setup instructions.

---

## Example Usage

### Post to Twitter Only
1. Type: "Hello world from my AI Employee! 🤖"
2. Click: **🐦 Twitter** button
3. Done! ✅

### Post to Multiple Platforms
1. Check: ☑ Twitter, ☑ LinkedIn, ☑ Facebook
2. Type: "Exciting news! Check out my latest project."
3. Click: **🚀 Post to All Selected**
4. Posted to 3 platforms at once! ✅

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Server not running" | Run `python dashboard_server.py` |
| "Credentials not configured" | Add tokens to `.env` file |
| Instagram fails | Instagram needs images - use browser automation |
| WhatsApp fails | Install Twilio: `pip install twilio` |

---

## Files Created

```
✅ dashboard_server.py      - Backend API server
✅ dashboard/dashboard.html - Updated frontend UI  
✅ start_dashboard.bat      - Windows startup script
✅ start_dashboard.sh       - Linux/Mac startup script
✅ requirements_dashboard.txt - Python dependencies
✅ DASHBOARD_README.md      - Full documentation
```

---

## Server Status

The dashboard server is **currently running** on:
- **URL:** http://localhost:8081
- **API:** http://localhost:8081/api

**To stop:** Press `Ctrl+C` in the server terminal

---

## Next Steps

1. **Open Dashboard:** http://localhost:8081
2. **Configure credentials** in `.env` for platforms you want to use
3. **Start posting!** No more CLI commands needed! 🎉

---

**Questions?** See `DASHBOARD_README.md` for complete documentation.

# Social Media Dashboard - Complete Guide

## Overview

The Social Media Dashboard provides a unified web interface to post to all your social media platforms from one place. No more CLI commands needed!

## Features

- ✅ **One-Click Posting**: Post to Twitter, Facebook, LinkedIn, Instagram, Gmail, and WhatsApp
- ✅ **Multi-Platform**: Select multiple platforms and post to all at once
- ✅ **Real-Time Stats**: View total posts and today's posts for each platform
- ✅ **Activity Logs**: Track all posting activity with timestamps
- ✅ **Auto-Refresh**: Dashboard updates every 10 seconds
- ✅ **Post History**: View recent posts for each platform

## Quick Start (Windows)

### Option 1: Double-Click Startup

1. Double-click `start_dashboard.bat`
2. Dashboard will open automatically at http://localhost:8081
3. Keep the command window open while using the dashboard

### Option 2: Manual Start

```bash
# Install dependencies
pip install flask flask-cors requests python-dotenv twilio

# Start server
python dashboard_server.py

# Open browser
http://localhost:8081
```

## Quick Start (Linux/Mac)

```bash
# Make script executable
chmod +x start_dashboard.sh

# Run startup script
./start_dashboard.sh
```

## Configuration

### Required Credentials

Before using the dashboard, configure your social media credentials in `.env`:

```bash
# Copy example
cp .env.example .env
```

Then edit `.env` with your actual credentials:

#### Twitter/X
```bash
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

Get from: https://developer.twitter.com/en/portal/dashboard

#### Facebook
```bash
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_access_token_here
FACEBOOK_API_VERSION=v18.0
```

Get from: https://developers.facebook.com/apps/

#### LinkedIn
```bash
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_REDIRECT_URI=https://localhost
```

Get tokens by running: `python get_linkedin_token.py`

#### Instagram
```bash
INSTAGRAM_PAGE_ACCESS_TOKEN=your_page_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id
```

Note: Instagram requires a Business/Creator account connected to a Facebook Page.

#### Gmail
```bash
GMAIL_CLIENT_ID=your_client_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-your_secret
GMAIL_PROJECT_ID=your_project_id
GMAIL_REDIRECT_URI=http://localhost
GMAIL_TOKEN_PATH=token.json
GMAIL_DEFAULT_RECIPIENT=your_email@example.com
```

First-time setup: Run `python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault`

#### WhatsApp (via Twilio)
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
WHATSAPP_RECIPIENT_NUMBER=whatsapp:+your_number
```

Get from: https://console.twilio.com/

## Usage

### Posting to a Single Platform

1. Type your message in the text area
2. Click the platform button (e.g., "🐦 Twitter")
3. Wait for confirmation
4. Post appears in the platform's post history

### Posting to Multiple Platforms

1. Check the boxes for platforms you want to post to
2. Type your message
3. Click "🚀 Post to All Selected"
4. All selected platforms will receive the post

### Viewing Statistics

- **Total**: All-time posts for that platform
- **Today**: Posts made today
- **Status**: Current connection status

### Activity Logs

View recent activity across all platforms:
- Timestamp
- Platform
- Status (✅ success, ❌ error, ⏳ pending)
- Content preview

## API Reference

The dashboard exposes a REST API at `http://localhost:8081/api`

### Post to Platform

```bash
POST /api/post
Content-Type: application/json

{
    "action": "post_twitter",
    "content": "Your message here"
}
```

**Actions:**
- `post_twitter` - Post to Twitter/X
- `post_facebook` - Post to Facebook Page
- `post_linkedin` - Post to LinkedIn
- `post_instagram` - Post to Instagram (requires image_url)
- `send_gmail` - Send email (optional: subject, to)
- `send_whatsapp` - Send WhatsApp message (optional: to)

### Get Posts

```bash
GET /api/posts/<platform>
# Example: GET /api/posts/twitter
```

### Get Statistics

```bash
GET /api/stats
```

### Get Activity Logs

```bash
GET /api/logs?date=20240224
# Format: YYYYMMDD
```

### Health Check

```bash
GET /api/health
```

## Troubleshooting

### "Server not running" error

**Solution:** Start the dashboard server:
```bash
python dashboard_server.py
```

### Platform credentials error

**Solution:** Check your `.env` file has the correct credentials for that platform.

### Instagram posting fails

**Solution:** Instagram API requires images. Use the Instagram-specific automation scripts for image posts, or ensure you provide an `image_url` in the API request.

### Gmail token expired

**Solution:** Re-run authentication:
```bash
python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault
```

### WhatsApp not sending

**Solution:** Install Twilio library:
```bash
pip install twilio
```

## File Structure

```
Hackathon-0/
├── dashboard/
│   └── dashboard.html      # Frontend UI
├── dashboard_server.py     # Backend API server
├── start_dashboard.bat     # Windows startup script
├── start_dashboard.sh      # Linux/Mac startup script
├── requirements_dashboard.txt  # Python dependencies
└── AI_Employee_Vault/
    └── Social_Media/
        ├── Twitter/
        │   └── posted_twitter.json
        ├── Facebook/
        │   └── posted_facebook.json
        ├── LinkedIn/
        │   └── posted_linkedin.json
        ├── Instagram/
        │   └── posted_instagram.json
        ├── Gmail/
        │   └── posted_gmail.json
        └── WhatsApp/
            └── posted_whatsapp.json
```

## Platform Limitations

| Platform | Character Limit | Media Support | Notes |
|----------|----------------|---------------|-------|
| Twitter | 280 chars | Text only | API v2 |
| Facebook | 63,206 chars | Text, links | Page posts only |
| LinkedIn | 3,000 chars | Text only | Personal profile |
| Instagram | 2,200 chars | Image required | Business account |
| Gmail | 25MB | Full email | OAuth required |
| WhatsApp | 4,096 chars | Text, media | Twilio sandbox |

## Security Notes

- ⚠️ **Never commit `.env`** - Contains sensitive credentials
- ⚠️ **Keep server local** - Dashboard runs on localhost only
- ⚠️ **Token security** - Store OAuth tokens securely
- ⚠️ **CORS enabled** - Only for local development

## Advanced Usage

### Custom Recipient for Email/WhatsApp

```json
{
    "action": "send_gmail",
    "content": "Message body",
    "subject": "Email subject",
    "to": "recipient@example.com"
}
```

### Instagram with Image

```json
{
    "action": "post_instagram",
    "content": "Caption text",
    "image_url": "https://example.com/image.jpg"
}
```

## Support

For issues or questions:
1. Check logs in `AI_Employee_Vault/Logs/`
2. Review platform-specific error messages
3. Verify credentials in `.env`
4. Ensure server is running on port 8081

## License

Part of the Personal AI Employee project.

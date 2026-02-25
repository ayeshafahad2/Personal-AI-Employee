# 🚀 Professional Dashboard Setup Guide

## Current Status

Your dashboard is **fully functional** but needs platform credentials configured.

### Platform Status

| Platform | Status | What's Needed |
|----------|--------|---------------|
| 🐦 **Twitter** | ⚠️ Token Issue | Fresh bearer token |
| 📘 **Facebook** | ❌ Not Configured | Page Access Token |
| 💼 **LinkedIn** | ❌ Not Configured | Access Token |
| 📸 **Instagram** | ❌ Not Configured | Business Token + Account ID |
| 📧 **Gmail** | ❌ Not Configured | OAuth Credentials |
| 💬 **WhatsApp** | ❌ Not Configured | Twilio Credentials |

---

## Quick Setup Commands

### Option 1: Run Setup Wizard (Recommended)

```bash
python setup_all_platforms.py
```

This interactive wizard will guide you through each platform setup.

### Option 2: Individual Platform Setup

#### Twitter - Fix 403 Error

```bash
python refresh_twitter_token.py
```

This will get a fresh bearer token using your existing API credentials.

#### LinkedIn - Get Access Token

```bash
python get_linkedin_token.py
```

This will walk you through LinkedIn OAuth and update `.env` automatically.

#### Gmail - OAuth Setup

```bash
python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault
```

This opens a browser for Google OAuth and creates `token.json`.

---

## Manual Configuration (Advanced)

If you prefer to get credentials manually, here are the direct links:

### Twitter
- **URL:** https://developer.twitter.com/en/portal/dashboard
- **What you need:** Bearer Token
- **Update:** `TWITTER_BEARER_TOKEN` in `.env`

### Facebook
- **URL:** https://developers.facebook.com/apps/
- **What you need:** Page Access Token with `pages_manage_posts` permission
- **Update:** `FACEBOOK_PAGE_ACCESS_TOKEN` in `.env`

### LinkedIn
- **URL:** https://www.linkedin.com/developers/apps
- **What you need:** Access Token with `w_member_social` permission
- **Update:** `LINKEDIN_ACCESS_TOKEN` in `.env`

### Instagram
- **URL:** https://developers.facebook.com/apps/
- **Requirements:** 
  - Instagram Business/Creator account
  - Connected to Facebook Page
- **What you need:**
  - Page Access Token with `instagram_manage_posts` permission
  - Instagram Business Account ID
- **Update:** 
  - `INSTAGRAM_PAGE_ACCESS_TOKEN` in `.env`
  - `INSTAGRAM_BUSINESS_ACCOUNT_ID` in `.env`

### Gmail
- **URL:** https://console.cloud.google.com/apis/credentials
- **Requirements:**
  - Google Cloud Project
  - Gmail API enabled
- **What you need:**
  - OAuth 2.0 Client ID
  - OAuth 2.0 Client Secret
- **Update:** Run OAuth script (above) or add to `.env`

### WhatsApp (Twilio)
- **URL:** https://console.twilio.com/
- **What you need:**
  - Account SID (starts with AC...)
  - Auth Token
  - WhatsApp Sandbox Number
- **Update:**
  - `TWILIO_ACCOUNT_SID` in `.env`
  - `TWILIO_AUTH_TOKEN` in `.env`
  - `TWILIO_WHATSAPP_NUMBER` in `.env`

---

## After Configuration

### 1. Restart Dashboard Server

Stop current server (Ctrl+C) then:

```bash
python dashboard_server.py
```

### 2. Verify Configuration

Open dashboard: http://localhost:8081

Check the **Platform Configuration** section - all configured platforms should show ✅

### 3. Test Posting

1. Type a test message
2. Click a platform button
3. Check the post appears in that platform's section
4. Verify no errors in Activity Logs

---

## Troubleshooting

### Twitter Still Shows 403

Your Twitter API credentials might be invalid or revoked.

**Solution:**
1. Go to https://developer.twitter.com/en/portal/projects
2. Check if your app is approved
3. Regenerate all credentials
4. Update `.env` with new values

### LinkedIn Token Expired

LinkedIn tokens expire after 60 days.

**Solution:**
```bash
python get_linkedin_token.py
```

### Gmail Token Expired

Gmail OAuth tokens expire.

**Solution:**
```bash
python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault
```

### Platform Shows "Not Configured" After Setup

The server might be using old credentials.

**Solution:**
1. Stop dashboard server (Ctrl+C)
2. Restart: `python dashboard_server.py`
3. Refresh dashboard page

---

## Security Best Practices

- ✅ Never commit `.env` to version control
- ✅ Store credentials securely
- ✅ Use environment variables in production
- ✅ Rotate tokens periodically
- ✅ Use app-specific passwords where available

---

## Dashboard Features

Once configured, your dashboard provides:

- ✅ **One-Click Posting** - Post to any platform instantly
- ✅ **Multi-Platform Posts** - Post to multiple platforms at once
- ✅ **Real-Time Stats** - See total and today's posts
- ✅ **Platform Status** - Monitor which platforms are active
- ✅ **Error Detection** - See exactly what went wrong
- ✅ **Activity Logs** - Track all posting activity
- ✅ **Auto-Refresh** - Updates every 10 seconds
- ✅ **Post History** - View recent posts per platform

---

## Quick Reference

### Start Dashboard
```bash
start_dashboard.bat
# or
python dashboard_server.py
```

### Open Dashboard
```
http://localhost:8081
```

### Check Status API
```bash
curl http://localhost:8081/api/status
```

### Post via API
```bash
curl -X POST http://localhost:8081/api/post \
  -H "Content-Type: application/json" \
  -d "{\"action\": \"post_twitter\", \"content\": \"Hello!\"}"
```

---

## Need Help?

1. **Setup Issues:** Run `python setup_all_platforms.py`
2. **Twitter Errors:** Run `python refresh_twitter_token.py`
3. **LinkedIn Errors:** Run `python get_linkedin_token.py`
4. **Gmail Errors:** Run `python watchers/gmail_watcher.py --auth`

---

## Files Reference

| File | Purpose |
|------|---------|
| `dashboard_server.py` | Backend API server |
| `dashboard/dashboard.html` | Web UI |
| `setup_all_platforms.py` | Interactive setup wizard |
| `refresh_twitter_token.py` | Twitter token refresh |
| `get_linkedin_token.py` | LinkedIn OAuth |
| `.env` | Your credentials (DO NOT COMMIT) |
| `DASHBOARD_README.md` | Full documentation |

---

**Your dashboard is production-ready!** 🎉

Just configure your platform credentials and start posting like a pro!

# 📧 Gmail Setup Guide

## Current Status: ❌ NOT CONFIGURED

Your `.env` file shows:
```env
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
```

**You need Gmail OAuth credentials to send emails.**

---

## 🚀 Quick Setup (2 Options)

### Option 1: Use Dashboard (Recommended for Testing)

The dashboard can send emails once you configure credentials.

**Steps:**

1. **Get Gmail API Credentials:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Create a new project (or select existing)
   - Enable Gmail API
   - Create OAuth 2.0 Client ID
   - Download credentials JSON

2. **Add to `.env`:**
   ```env
   GMAIL_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
   GMAIL_CLIENT_SECRET=your_secret_here
   GMAIL_PROJECT_ID=your_project_id
   GMAIL_REDIRECT_URI=http://localhost
   ```

3. **Run OAuth Setup:**
   ```bash
   python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault
   ```

4. **Authenticate:**
   - Browser will open
   - Login to Gmail
   - Grant permissions
   - `token.json` will be created

5. **Send from Dashboard:**
   - Open http://localhost:8081
   - Type message
   - Check "Gmail" checkbox
   - Click "📧 Gmail"

---

### Option 2: Manual Test Script

Create a simple test script:

```bash
python test_gmail_send.py
```

**Requirements:**
- Gmail account
- App Password (if 2FA enabled)
- Or OAuth credentials

---

## 🔐 Get Gmail App Password (Easier than OAuth)

If you have 2FA enabled on Gmail:

1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and your device
3. Generate app password
4. Use in script

---

## 📝 What You Need

| Credential | Where to Get | Status |
|------------|--------------|--------|
| `GMAIL_CLIENT_ID` | Google Cloud Console | ❌ Missing |
| `GMAIL_CLIENT_SECRET` | Google Cloud Console | ❌ Missing |
| `GMAIL_PROJECT_ID` | Google Cloud Console | ❌ Missing |
| `token.json` | OAuth flow | ❌ Not created |

---

## 🎯 Alternative: Use Dashboard API

Once configured, send emails via dashboard:

**Web Interface:**
1. Open http://localhost:8081
2. Type message
3. Click "📧 Gmail"

**API:**
```bash
curl -X POST http://localhost:8081/api/post \
  -H "Content-Type: application/json" \
  -d '{
    "action": "send_gmail",
    "content": "Email body",
    "subject": "Test Subject",
    "to": "recipient@example.com"
  }'
```

---

## ❓ Need Help?

**Common Issues:**

| Issue | Solution |
|-------|----------|
| "Credentials not configured" | Add to `.env` file |
| "Token expired" | Re-run OAuth setup |
| "Gmail API error" | Check Gmail API is enabled |

---

## 📖 Resources

- **Gmail API Docs:** https://developers.google.com/gmail/api
- **Google Cloud Console:** https://console.cloud.google.com/
- **OAuth Setup Guide:** https://developers.google.com/identity/protocols/oauth2

---

**Status:** Gmail credentials required before sending emails.

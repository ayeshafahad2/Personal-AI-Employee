# Twitter 403 Error Fix

## Problem
Your Twitter API token is returning a `403 Forbidden` error. This means the token is either:
1. Expired
2. Revoked
3. Doesn't have proper permissions

## Solution

### Option 1: Refresh Twitter Token (Recommended)

Run this command to get a new Twitter token:

```bash
python get_twitter_token.py
```

This will:
1. Open a browser window
2. Ask you to authorize the app
3. Get new credentials
4. Update your `.env` file automatically

### Option 2: Manual Token Refresh

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Select your app
3. Click "Keys and tokens"
4. Regenerate the "Bearer Token"
5. Copy the new token
6. Update your `.env` file:
   ```
   TWITTER_BEARER_TOKEN=new_token_here
   ```

### Option 3: Check App Permissions

1. Go to https://developer.twitter.com/en/portal/projects
2. Select your project
3. Check if your app has "Read and Write" permissions
4. If not, request elevated access

## After Fixing

1. Restart the dashboard server:
   ```bash
   # Stop current server (Ctrl+C)
   python dashboard_server.py
   ```

2. Refresh the dashboard in your browser

3. Try posting again!

---

## Other Platform Setup

### Facebook
```bash
# Get Page Access Token from:
https://developers.facebook.com/apps/

# Add to .env:
FACEBOOK_PAGE_ACCESS_TOKEN=your_token
```

### LinkedIn
```bash
# Run this to get tokens:
python get_linkedin_token.py

# Or add manually:
LINKEDIN_ACCESS_TOKEN=your_token
```

### Instagram
```bash
# Need Business/Creator account
# Get from Facebook Developer:
INSTAGRAM_PAGE_ACCESS_TOKEN=your_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_id
```

### Gmail
```bash
# Run OAuth setup:
python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault

# Or add credentials:
GMAIL_CLIENT_ID=your_id
GMAIL_CLIENT_SECRET=your_secret
```

### WhatsApp
```bash
# Get from Twilio:
https://console.twilio.com/

TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
```

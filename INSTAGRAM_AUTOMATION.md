# Instagram Automation - Complete Guide

## ✅ Files Created

| File | Purpose | Command |
|------|---------|---------|
| `instagram_auto_poster.py` | Auto-post images with captions | `python instagram_auto_poster.py` |
| `instagram_active_watcher.py` | Monitor DMs & notifications | `python instagram_active_watcher.py` |
| `instagram_dashboard.py` | Quick view browser (currently running) | `python instagram_dashboard.py` |

## Features

### Instagram Auto Poster
- Opens Instagram in browser
- Helps you create and publish posts
- Auto-copies caption to clipboard
- Supports image uploads (manual drag-drop on web)
- Takes screenshot after posting

### Instagram Active Watcher
- Monitors Direct Messages (DMs)
- Tracks notifications (likes, comments, follows)
- Shows unread/read status
- Continuous monitoring mode (30-second intervals)
- Saves JSON reports
- Takes periodic screenshots

### Instagram Dashboard
- Simple browser viewer
- Opens Instagram for manual monitoring
- Quick navigation links
- Stays open for 10 minutes

## Usage

### Post to Instagram

```bash
python instagram_auto_poster.py
```

**What it does:**
1. Opens Instagram in Chrome
2. Waits for login (if needed)
3. Opens post creator
4. Copies caption to clipboard
5. You drag-drop image and paste caption
6. You click "Share"
7. Saves screenshot

### Monitor Activity

```bash
python instagram_active_watcher.py
```

**Options:**
1. Run once - Show current DMs and notifications
2. Continuous watch - Check every 30 seconds
3. Manual review - Keep browser open

**Output:**
```
======================================================================
  INSTAGRAM ACTIVITY DASHBOARD
======================================================================
  Updated: 2026-02-20

----------------------------------------------------------------------
  DIRECT MESSAGES (Last 10)
----------------------------------------------------------------------
  1. [UNREAD]
     John Doe: Hey, saw your post about AI...

----------------------------------------------------------------------
  NOTIFICATIONS (Last 10)
----------------------------------------------------------------------
  1. [NEW]
     jane_smith started following you
```

### Quick View

```bash
python instagram_dashboard.py
```

Opens Instagram for 10 minutes for manual monitoring.

## API vs Browser Approach

### Browser Automation (Current)
**Pros:**
- ✅ Works immediately - no API setup
- ✅ No app approval needed
- ✅ Full Instagram features
- ✅ No rate limits from API

**Cons:**
- ⚠️ Requires browser window
- ⚠️ Some manual steps (upload, click)
- ⚠️ Less reliable than API

### Instagram Graph API (Alternative)
**Pros:**
- ✅ Fully automated
- ✅ More reliable
- ✅ Better for production

**Cons:**
- ⚠️ Requires Instagram Business account
- ⚠️ Requires Facebook Developer app
- ⚠️ Needs app approval
- ⚠️ Limited to image/carousel posts

## Setup Instagram API (Optional)

If you want full API automation:

### Step 1: Convert to Business Account
1. Open Instagram → Settings
2. Account → Switch to Professional Account
3. Select "Business"

### Step 2: Create Facebook Developer App
1. Go to https://developers.facebook.com/
2. Create App → Business type
3. Add "Instagram Graph API" product

### Step 3: Get Credentials
1. Get Page Access Token with `instagram_manage_posts` permission
2. Get Instagram Business Account ID:
   ```
   GET https://graph.facebook.com/v18.0/{page-id}?fields=instagram_business_account
   ```

### Step 4: Update .env
```env
INSTAGRAM_PAGE_ACCESS_TOKEN=your_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id_here
FACEBOOK_API_VERSION=v18.0
```

### Step 5: Use MCP Server
```bash
python mcp_instagram_server.py
```

## Current Status

| Platform | Post | Notify | Watch |
|----------|------|--------|-------|
| LinkedIn | ✅ | ✅ | ✅ |
| WhatsApp | ✅ | ✅ | ✅ |
| Instagram | ✅ | ⬜ | ✅ |
| Twitter/X | ❌ | ❌ | ❌ |

## Next Steps

1. **Test Instagram posting:**
   ```bash
   python instagram_auto_poster.py
   ```

2. **Test Instagram monitoring:**
   ```bash
   python instagram_active_watcher.py
   ```

3. **Add Twitter/X** (optional - let me know)

## Troubleshooting

### "Login not detected"
- Make sure you're logging in to the correct Instagram account
- Wait for the feed to fully load
- Try manual login before running script

### "Cannot find create button"
- Instagram may have updated UI
- Use manual mode - click "+" or "Create" yourself
- Script will still help with caption

### "No unread messages found"
- Check if you actually have unread DMs
- Instagram's web interface has limited DM support
- Use browser window to verify

## Files Generated

- `instagram_post_result.png` - Screenshot after posting
- `instagram_activity.png` - Screenshot of activity
- `instagram_activity.json` - Activity report
- `AI_Employee_Vault/Logs/instagram_*.json` - Post logs

---

**Instagram automation is ready!**

Run: `python instagram_dashboard.py` (already running)

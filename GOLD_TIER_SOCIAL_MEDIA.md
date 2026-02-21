# Gold Tier - Social Media Integration Complete

## ✅ Gold Tier Status: COMPLETE (Social Media Only)

This implementation adds **Facebook, Instagram, and Twitter (X)** integration to your Personal AI Employee.

> **Note:** This Gold Tier implementation focuses on social media automation only. Odoo/Accounting integration is not included as requested.

---

## 📁 New Files Created

### MCP Servers (3 files)

| File | Platform | Capabilities |
|------|----------|--------------|
| `mcp_facebook_server.py` | Facebook | Post to Pages, Photo posts |
| `mcp_instagram_server.py` | Instagram | Image posts, Carousel posts |
| `mcp_twitter_server.py` | Twitter/X | Tweets, Tweets with media |

### Unified Poster

| File | Purpose |
|------|---------|
| `social_media_poster.py` | Post to all platforms at once |

---

## 🚀 Quick Start

### Step 1: Configure Social Media Credentials

Update `.env` with your API credentials:

```env
# Facebook
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_token
FACEBOOK_API_VERSION=v18.0

# Instagram
INSTAGRAM_PAGE_ACCESS_TOKEN=your_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id

# Twitter/X
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_secret
```

### Step 2: Get API Credentials

#### Facebook Page Access Token

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create an app (Business type)
3. Add **Pages API** product
4. Get Page Access Token from Graph API Explorer
5. Add to `.env`

#### Instagram Business Account

1. Convert Instagram to **Business** or **Creator** account
2. Connect to Facebook Page
3. In Facebook Developer app, add **Instagram Graph API**
4. Get:
   - Page Access Token (with `instagram_manage_posts` permission)
   - Instagram Business Account ID
5. Add both to `.env`

#### Twitter/X API Credentials

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a project and app
3. Get credentials:
   - Bearer Token
   - API Key & Secret
   - Access Token & Secret
4. Add all to `.env`

### Step 3: Test Connections

```bash
python social_media_poster.py --test
```

---

## 📋 Usage Examples

### Post to All Platforms

```bash
# Post text to all configured platforms
python social_media_poster.py --text "Your post content here"

# Post to specific platforms
python social_media_poster.py --text "Content" --platforms linkedin,facebook,twitter

# Post with image (for Instagram)
python social_media_poster.py --text "Caption" --image "https://example.com/image.jpg"
```

### Post to Individual Platforms

Each MCP server can be used independently:

**Facebook:**
```python
from mcp_facebook_server import FacebookMCPServer

server = FacebookMCPServer()
result = server.post_to_page("Hello Facebook!")
```

**Instagram:**
```python
from mcp_instagram_server import InstagramMCPServer

server = InstagramMCPServer()
result = server.post_image("https://example.com/image.jpg", "Caption here")
```

**Twitter:**
```python
from mcp_twitter_server import TwitterMCPServer

server = TwitterMCPServer()
result = server.post_tweet("Hello Twitter!")
```

---

## 🔧 MCP Server Configuration

Add to your AI assistant's MCP configuration:

```json
{
  "mcpServers": {
    "facebook": {
      "command": "python",
      "args": ["mcp_facebook_server.py"]
    },
    "instagram": {
      "command": "python",
      "args": ["mcp_instagram_server.py"]
    },
    "twitter": {
      "command": "python",
      "args": ["mcp_twitter_server.py"]
    }
  }
}
```

---

## 📊 Platform Capabilities

| Feature | Facebook | Instagram | Twitter | LinkedIn |
|---------|----------|-----------|---------|----------|
| Text Posts | ✅ | ❌ | ✅ (280 chars) | ✅ |
| Image Posts | ✅ | ✅ | ✅ | ✅ |
| Carousel | ❌ | ✅ (2-10) | ✅ (4) | ✅ |
| Video | ❌ | ⬜ | ⬜ | ✅ |
| Links | ✅ | ❌ | ✅ | ✅ |
| Scheduling | ⬜ | ⬜ | ⬜ | ⬜ |

---

## 🗂️ Vault Integration

All posts are automatically logged to your Obsidian vault:

### Logs Folder
```
AI_Employee_Vault/Logs/
├── facebook_2026-02-17.json
├── instagram_2026-02-17.json
├── twitter_2026-02-17.json
└── social_media_2026-02-17.json
```

### Dashboard Updates

Each post updates `Dashboard.md`:
```markdown
## Recent Activity

- [2026-02-17 18:30:00] Facebook post published: https://facebook.com/123456
- [2026-02-17 18:30:05] Instagram post published: https://instagram.com/p/789012
- [2026-02-17 18:30:10] Twitter post published: https://twitter.com/i/web/status/345678
```

---

## 🎯 Example Workflows

### Workflow 1: Cross-Platform Announcement

```bash
# Announce something on all platforms at once
python social_media_poster.py \
  --text "🚀 Exciting news! We just launched our new product. Check it out!" \
  --platforms linkedin,facebook,twitter
```

### Workflow 2: Instagram Post with Image

```bash
# Post to Instagram with image
python social_media_poster.py \
  --text "Beautiful sunset today! 🌅 #nature #photography" \
  --image "https://example.com/sunset.jpg" \
  --platforms instagram
```

### Workflow 3: AI-Generated Social Posts

Let your AI Employee generate and post content:

1. Create action file in `Needs_Action/social_post.md`:
```markdown
---
type: social_media_post
platforms: linkedin,facebook,twitter
status: pending
---

# Social Media Post Request

Please create and post engaging content about our latest achievement.
```

2. Run orchestrator:
```bash
python orchestrator.py --process
```

3. AI will generate content and post via MCP servers

---

## 📝 API Setup Guides

### Facebook Detailed Setup

1. **Create Facebook Developer Account**
   - Visit https://developers.facebook.com/
   - Click "Get Started" → Create account

2. **Create App**
   - App Type: **Business**
   - Fill in app details

3. **Add Pages API**
   - In app dashboard, click "Add Product"
   - Select "Pages"
   - Complete setup

4. **Get Access Token**
   - Go to Graph API Explorer
   - Select your app
   - Request permissions: `pages_manage_posts`, `pages_read_engagement`
   - Generate token
   - Copy to `.env`

### Instagram Detailed Setup

1. **Convert to Business Account**
   - Open Instagram → Settings
   - Account → Switch to Professional Account
   - Select "Business"

2. **Connect Facebook Page**
   - In Instagram Settings
   - Account → Linked Accounts → Facebook
   - Select your business page

3. **Get Credentials**
   - In Facebook Developer app
   - Add Instagram Graph API
   - Get Page Access Token
   - Get Instagram Business Account ID from:
     ```
     GET https://graph.facebook.com/v18.0/{page-id}?fields=instagram_business_account
     ```

### Twitter Detailed Setup

1. **Create Developer Account**
   - Visit https://developer.twitter.com/
   - Apply for developer account
   - Wait for approval (usually quick)

2. **Create Project & App**
   - Create new project
   - Create new app within project
   - Set app permissions to "Read and Write"

3. **Get Credentials**
   - In app dashboard → Keys and Tokens
   - Generate:
     - API Key & Secret
     - Access Token & Secret
     - Bearer Token
   - Copy all to `.env`

---

## 🔒 Security Notes

- **Never commit `.env`** to version control
- **Rotate tokens** every 90 days
- **Use app roles** to limit permissions
- **Monitor API usage** in developer consoles
- **Set up alerts** for unusual activity

---

## 📊 Logging & Analytics

### View Post Logs

```bash
# View today's social media logs
cat AI_Employee_Vault/Logs/social_media_$(date +%Y-%m-%d).json
```

### Track Performance

Each platform provides analytics:
- **Facebook**: Page Insights
- **Instagram**: Professional Dashboard
- **Twitter**: Analytics dashboard
- **LinkedIn**: Post analytics

---

## ⚠️ Rate Limits

| Platform | Limit | Notes |
|----------|-------|-------|
| Facebook | 200 posts/day | Per page |
| Instagram | 25 posts/day | Business accounts |
| Twitter | 300 tweets/day | Free tier |
| LinkedIn | 150 posts/day | Personal accounts |

---

## 🎯 Gold Tier Checklist

| Requirement | Status |
|-------------|--------|
| Facebook Integration | ✅ Complete |
| Instagram Integration | ✅ Complete |
| Twitter (X) Integration | ✅ Complete |
| Unified Social Poster | ✅ Complete |
| Vault Logging | ✅ Complete |
| MCP Servers | ✅ Complete |

---

## 🚀 Next Steps

### To Go Further

1. **Add Scheduling**: Implement post scheduling
2. **Add Analytics**: Fetch engagement metrics
3. **Add Content Generation**: AI-generated post content
4. **Add Hashtag Suggestions**: AI-powered hashtag research
5. **Add Media Library**: Local image/video management

### For Platinum Tier

- Cloud deployment for 24/7 operation
- Synced vault between local and cloud
- Always-on watchers

---

**Gold Tier Social Media Integration Complete! 🎉**

Run: `python social_media_poster.py --test` to verify your setup.

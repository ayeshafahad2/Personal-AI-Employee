# Social Media Dashboard

Last updated: 2026-02-24 15:50:14

---

## Quick Actions

- [[../Dashboard|← Back to Main Dashboard]]
- [Post to All Platforms](#post-to-all-platforms)
- [View Facebook Posts](./Facebook/)
- [View Twitter Posts](./Twitter/)

---

## Overview

| Platform | Total Posts | Today | Last Activity |
|----------|-------------|-------|---------------|
| Facebook | 0 | 0 | N/A |
| Twitter | 0 | 0 | N/A |

---

## Recent Facebook Posts

*No recent posts*

---

## Recent Twitter Posts

*No recent posts*

---

## Post to All Platforms

To post to all platforms at once, run:

```bash
python social_media_unified_post.py --text "Your message here"
```

Or post individually:

```bash
# Facebook
python watchers/facebook_watcher.py --post "Your message"

# Twitter
python watchers/twitter_watcher.py --tweet "Your message"
```

---

## Activity Log

See detailed logs in: `Logs/social_media_activity.json`

---

*Dashboard auto-updates every 5 minutes when watchers are running*

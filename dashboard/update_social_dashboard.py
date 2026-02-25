#!/usr/bin/env python3
"""
Social Media Dashboard for Obsidian
Updates the Obsidian dashboard with social media activity
"""

import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class SocialMediaDashboard:
    """Obsidian Social Media Dashboard"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        self.social_dir = self.vault_path / 'Social_Media'
        self.dashboard_file = self.social_dir / 'Dashboard.md'
        self.logs_dir = self.vault_path / 'Logs'
        
        # Ensure directories exist
        self.social_dir.mkdir(parents=True, exist_ok=True)
        (self.social_dir / 'Facebook').mkdir(parents=True, exist_ok=True)
        (self.social_dir / 'Twitter').mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def get_platform_stats(self, platform: str) -> dict:
        """Get stats for a platform"""
        platform_dir = self.social_dir / platform.capitalize()
        
        stats = {
            'total_posts': 0,
            'today_posts': 0,
            'last_post': None,
            'last_post_time': None
        }
        
        # Read state file
        state_file = platform_dir / '.state.json'
        if state_file.exists():
            with open(state_file, 'r') as f:
                state = json.load(f)
                stats['total_posts'] = state.get('posts_count', 0)
                stats['last_post_time'] = state.get('last_check')
        
        # Count today's posts
        today = datetime.now().strftime('%Y-%m-%d')
        today_file = platform_dir / f'posts_{today}.md'
        if today_file.exists():
            with open(today_file, 'r') as f:
                content = f.read()
                stats['today_posts'] = content.count('## Post -')
        
        # Get last post
        posts_file = platform_dir / f'posted_{"tweets" if platform == "twitter" else "posts"}.json'
        if posts_file.exists():
            with open(posts_file, 'r') as f:
                posts = json.load(f)
                if posts:
                    stats['last_post'] = posts[-1].get('content', '')[:100]
        
        return stats
    
    def get_recent_posts(self, platform: str, limit: int = 5) -> list:
        """Get recent posts from a platform"""
        platform_dir = self.social_dir / platform.capitalize()
        posts_file = platform_dir / f'posted_{"tweets" if platform == "twitter" else "posts"}.json'
        
        if posts_file.exists():
            with open(posts_file, 'r') as f:
                posts = json.load(f)
                return posts[-limit:]
        
        return []
    
    def update_dashboard(self):
        """Update the social media dashboard"""
        # Get stats
        fb_stats = self.get_platform_stats('facebook')
        tw_stats = self.get_platform_stats('twitter')
        
        # Get recent posts
        fb_posts = self.get_recent_posts('facebook')
        tw_posts = self.get_recent_posts('twitter')
        
        # Generate dashboard content
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        dashboard = f"""# Social Media Dashboard

Last updated: {now}

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
| Facebook | {fb_stats['total_posts']} | {fb_stats['today_posts']} | {fb_stats['last_post_time'] or 'N/A'} |
| Twitter | {tw_stats['total_posts']} | {tw_stats['today_posts']} | {tw_stats['last_post_time'] or 'N/A'} |

---

## Recent Facebook Posts

"""
        
        if fb_posts:
            for post in reversed(fb_posts[-5:]):
                content = post.get('content', '')[:200]
                timestamp = post.get('timestamp', '')[:16]
                dashboard += f"""### {timestamp}

{content}...

"""
        else:
            dashboard += "*No recent posts*\n\n"
        
        dashboard += """---

## Recent Twitter Posts

"""
        
        if tw_posts:
            for post in reversed(tw_posts[-5:]):
                content = post.get('content', '')[:200]
                timestamp = post.get('timestamp', '')[:16]
                dashboard += f"""### {timestamp}

{content}...

"""
        else:
            dashboard += "*No recent posts*\n\n"
        
        dashboard += """---

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
"""
        
        # Write dashboard
        with open(self.dashboard_file, 'w', encoding='utf-8') as f:
            f.write(dashboard)
        
        print(f"Dashboard updated: {self.dashboard_file}")
        
        # Also update main Dashboard.md
        self.update_main_dashboard(fb_stats, tw_stats)
    
    def update_main_dashboard(self, fb_stats: dict, tw_stats: dict):
        """Update the main vault Dashboard.md with social media section"""
        main_dashboard = self.vault_path / 'Dashboard.md'
        
        if main_dashboard.exists():
            with open(main_dashboard, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add social media section if not exists
            if '## Social Media' not in content:
                social_section = f"""
## Social Media

| Platform | Posts | Today |
|----------|-------|-------|
| Facebook | {fb_stats['total_posts']} | {fb_stats['today_posts']} |
| Twitter | {tw_stats['total_posts']} | {tw_stats['today_posts']} |

See full details: [[Social_Media/Dashboard|Social Media Dashboard]]

"""
                content += social_section
                
                with open(main_dashboard, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Main dashboard updated: {main_dashboard}")
    
    def log_activity(self, activity: dict):
        """Log social media activity"""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs_dir / f'social_media_{today}.json'
        
        activities = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                activities = json.load(f)
        
        activities.append({
            'timestamp': datetime.now().isoformat(),
            **activity
        })
        
        with open(log_file, 'w') as f:
            json.dump(activities, f, indent=2)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Social Media Dashboard')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault',
                       help='Path to Obsidian vault')
    parser.add_argument('--update', action='store_true', help='Update dashboard')
    
    args = parser.parse_args()
    
    dashboard = SocialMediaDashboard(vault_path=args.vault)
    
    if args.update:
        print("Updating social media dashboard...")
        dashboard.update_dashboard()
    else:
        # Just show status
        print("Social Media Dashboard Status")
        print("=" * 50)
        fb_stats = dashboard.get_platform_stats('facebook')
        tw_stats = dashboard.get_platform_stats('twitter')
        
        print(f"\nFacebook: {fb_stats['total_posts']} total, {fb_stats['today_posts']} today")
        print(f"Twitter: {tw_stats['total_posts']} total, {tw_stats['today_posts']} today")
        print(f"\nDashboard: {dashboard.dashboard_file}")


if __name__ == '__main__':
    main()

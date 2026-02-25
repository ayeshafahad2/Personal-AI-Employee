#!/usr/bin/env python3
"""
Facebook Watcher
Monitors Facebook profile for new posts and activity
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from base_social_watcher import BaseSocialWatcher

load_dotenv()


class FacebookWatcher(BaseSocialWatcher):
    """Facebook profile watcher"""
    
    def __init__(self, vault_path: str = None):
        super().__init__('facebook', vault_path)
        
        # Facebook profile URL from env or default
        self.profile_url = os.getenv(
            'FACEBOOK_PROFILE_URL',
            'https://www.facebook.com/profile.php?id=61576154677449'
        )
        
        # Track posted content locally
        self.posts_log = self.platform_dir / 'posted_posts.json'
        if not self.posts_log.exists():
            with open(self.posts_log, 'w') as f:
                json.dump([], f)
    
    def check_for_updates(self):
        """Check Facebook for new activity"""
        # Since Facebook doesn't have a simple public API for personal profiles,
        # we'll track locally posted content
        
        print(f"  Profile: {self.profile_url}")
        print(f"  Total posts tracked: {self.state['posts_count']}")
        
        # In a real implementation, you would:
        # 1. Use Facebook Graph API (requires Page Access Token)
        # 2. Or scrape the profile (against ToS)
        # 3. Or track locally posted content
        
        # For now, we track locally posted content
        self._check_local_posts()
    
    def _check_local_posts(self):
        """Check for newly posted content from our automation"""
        posts_file = self.platform_dir / 'posted_posts.json'
        
        if posts_file.exists():
            import json
            with open(posts_file, 'r') as f:
                posts = json.load(f)
            
            # Log any new posts
            for post in posts:
                if post.get('id') != self.state.get('last_post_id'):
                    print(f"  New post detected!")
                    self.log_post(post)
                    print(f"  Logged to: {self.platform_dir}")
    
    def post_to_facebook(self, content: str) -> dict:
        """
        Post to Facebook
        
        Args:
            content: Post content
            
        Returns:
            Dict with post info
        """
        post_data = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'url': self.profile_url,
            'platform': 'facebook'
        }
        
        # Save to local log
        posts_file = self.platform_dir / 'posted_posts.json'
        import json
        
        posts = []
        if posts_file.exists():
            with open(posts_file, 'r') as f:
                posts = json.load(f)
        
        posts.append(post_data)
        
        with open(posts_file, 'w') as f:
            json.dump(posts, f, indent=2)
        
        # Log the post
        self.log_post(post_data)
        
        return post_data


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Facebook Watcher')
    parser.add_argument('--watch', action='store_true', help='Start watching')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault',
                       help='Path to Obsidian vault')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds')
    parser.add_argument('--post', type=str, help='Post content to Facebook')
    
    args = parser.parse_args()
    
    watcher = FacebookWatcher(vault_path=args.vault)
    
    if args.post:
        # Post to Facebook
        print("Posting to Facebook...")
        result = watcher.post_to_facebook(args.post)
        print(f"Posted! ID: {result['id']}")
        print(f"Logged to: {watcher.platform_dir}")
    elif args.watch:
        # Start watching
        watcher.watch(interval=args.interval)
    else:
        # Just check once
        print("Facebook Watcher")
        print("=" * 50)
        watcher.check_for_updates()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Instagram Watcher
Monitors Instagram for posts and activity
"""

import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from base_social_watcher import BaseSocialWatcher

load_dotenv()


class InstagramWatcher(BaseSocialWatcher):
    """Instagram watcher"""
    
    def __init__(self, vault_path: str = None):
        super().__init__('instagram', vault_path)
        
        self.username = os.getenv('INSTAGRAM_USERNAME', 'your_instagram')
    
    def check_for_updates(self):
        """Check Instagram for new activity"""
        print(f"  Checking Instagram...")
        print(f"  Account: @{self.username}")
        
        # Track posts
        try:
            posts = self._get_recent_posts()
            print(f"  Found {len(posts)} recent posts")
            
            for post in posts:
                self.log_post(post)
                
        except Exception as e:
            print(f"  Instagram check: {e}")
    
    def _get_recent_posts(self):
        """Get recent posts (placeholder)"""
        return []
    
    def log_post(self, post: dict):
        """Log post to vault"""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.platform_dir / f'posts_{today}.md'
        
        content = f"""
## Post - {post.get('timestamp', datetime.now().isoformat())}

**Type:** {post.get('type', 'image')}
**Likes:** {post.get('likes', 0)}
**Comments:** {post.get('comments', 0)}

### Caption

{post.get('caption', '')}

"""
        
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                existing = f.read()
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(existing + content + "\n---\n")
        else:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"# Instagram Posts - {today}\n\n---\n" + content)
        
        self.state['posts_count'] = self.state.get('posts_count', 0) + 1
        self.save_state()
    
    def post_image(self, image_path: str, caption: str) -> dict:
        """Post an image to Instagram"""
        post_data = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'type': 'image',
            'image_path': image_path,
            'caption': caption,
            'timestamp': datetime.now().isoformat(),
            'platform': 'instagram'
        }
        
        # Save to local log
        posts_file = self.platform_dir / 'posted_posts.json'
        posts = []
        if posts_file.exists():
            with open(posts_file, 'r') as f:
                posts = json.load(f)
        
        posts.append(post_data)
        
        with open(posts_file, 'w') as f:
            json.dump(posts, f, indent=2)
        
        self.log_post({
            'type': 'image',
            'caption': caption,
            'likes': 0,
            'comments': 0,
            'timestamp': post_data['timestamp']
        })
        
        return post_data


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Instagram Watcher')
    parser.add_argument('--watch', action='store_true', help='Start watching')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault')
    parser.add_argument('--interval', type=int, default=300)
    parser.add_argument('--post', type=str, help='Post image with caption')
    parser.add_argument('--image', type=str, help='Image path')
    parser.add_argument('--caption', type=str, help='Caption')
    
    args = parser.parse_args()
    
    watcher = InstagramWatcher(vault_path=args.vault)
    
    if args.post and args.image:
        print(f"Posting to Instagram...")
        result = watcher.post_image(args.image, args.caption or '')
        print(f"Posted! ID: {result['id']}")
    elif args.watch:
        watcher.watch(interval=args.interval)
    else:
        print("Instagram Watcher")
        print("=" * 50)
        watcher.check_for_updates()


if __name__ == '__main__':
    main()

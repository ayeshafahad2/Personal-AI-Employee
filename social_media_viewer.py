#!/usr/bin/env python3
"""
Social Media Unified Viewer
Terminal-based viewer for all social media activity
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class SocialMediaViewer:
    """Unified viewer for all social media"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        self.social_dir = self.vault_path / 'Social_Media'
    
    def clear_screen(self):
        """Clear terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_header(self):
        """Get viewer header"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"""
╔══════════════════════════════════════════════════════════╗
║           SOCIAL MEDIA DASHBOARD                         ║
║           Updated: {now}                          ║
╚══════════════════════════════════════════════════════════╝
"""
    
    def get_platform_stats(self, platform: str) -> dict:
        """Get stats for a platform"""
        platform_dir = self.social_dir / platform.capitalize()
        
        stats = {'total': 0, 'today': 0}
        
        state_file = platform_dir / '.state.json'
        if state_file.exists():
            with open(state_file, 'r') as f:
                state = json.load(f)
                stats['total'] = state.get('posts_count', 0)
        
        today = datetime.now().strftime('%Y-%m-%d')
        today_file = platform_dir / f'posts_{today}.md'
        if today_file.exists():
            with open(today_file, 'r') as f:
                stats['today'] = f.read().count('## Post -')
        
        return stats
    
    def get_recent_posts(self, platform: str, limit: int = 5) -> list:
        """Get recent posts"""
        platform_dir = self.social_dir / platform.capitalize()
        posts_file = platform_dir / f'posted_{"tweets" if platform == "twitter" else "posts"}.json'
        
        if posts_file.exists():
            with open(posts_file, 'r') as f:
                posts = json.load(f)
                return posts[-limit:]
        return []
    
    def display(self):
        """Display the viewer"""
        self.clear_screen()
        print(self.get_header())
        
        # Facebook section
        fb_stats = self.get_platform_stats('facebook')
        fb_posts = self.get_recent_posts('facebook')
        
        print(f"\n📘 FACEBOOK")
        print(f"   Total: {fb_stats['total']} | Today: {fb_stats['today']}")
        print("   " + "─" * 50)
        
        if fb_posts:
            for post in reversed(fb_posts[-3:]):
                content = post.get('content', '')[:80]
                timestamp = post.get('timestamp', '')[:16]
                print(f"   • [{timestamp}] {content}...")
        else:
            print("   No recent posts")
        
        # Twitter section
        tw_stats = self.get_platform_stats('twitter')
        tw_posts = self.get_recent_posts('twitter')
        
        print(f"\n🐦 TWITTER")
        print(f"   Total: {tw_stats['total']} | Today: {tw_stats['today']}")
        print("   " + "─" * 50)
        
        if tw_posts:
            for post in reversed(tw_posts[-3:]):
                content = post.get('content', '')[:80]
                timestamp = post.get('timestamp', '')[:16]
                print(f"   • [{timestamp}] {content}...")
        else:
            print("   No recent posts")
        
        # Quick actions
        print("\n" + "═" * 50)
        print("   QUICK ACTIONS:")
        print("   [1] Post to Facebook")
        print("   [2] Post to Twitter")
        print("   [3] Post to Both")
        print("   [R] Refresh")
        print("   [Q] Quit")
        print("═" * 50)
    
    def run(self):
        """Run the viewer"""
        print("Starting Social Media Viewer...")
        print("Press Ctrl+C to exit")
        
        try:
            while True:
                self.display()
                
                # Wait for input with timeout
                start = time.time()
                while time.time() - start < 10:
                    time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\nViewer exited.")


def main():
    viewer = SocialMediaViewer()
    viewer.run()


if __name__ == '__main__':
    main()

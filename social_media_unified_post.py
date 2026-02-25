#!/usr/bin/env python3
"""
Social Media Unified Poster
Post to all platforms at once
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import subprocess
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class SocialMediaPoster:
    """Post to all social media platforms"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        self.social_dir = self.vault_path / 'Social_Media'
        self.logs_dir = self.vault_path / 'Logs'
        
        # Ensure directories exist
        for platform in ['Facebook', 'Twitter']:
            (self.social_dir / platform).mkdir(parents=True, exist_ok=True)
    
    def post_to_all(self, content: str):
        """
        Post to all platforms
        
        Args:
            content: Content to post
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'content': content,
            'platforms': {}
        }
        
        print("=" * 60)
        print("  POSTING TO ALL PLATFORMS")
        print("=" * 60)
        print(f"\n  Content:\n  {content}\n")
        
        # Post to Facebook
        print("[1/2] Posting to Facebook...")
        fb_result = self._post_facebook(content)
        results['platforms']['facebook'] = fb_result
        print(f"      {'✓ Posted!' if fb_result['success'] else '✗ Failed'}")
        
        # Post to Twitter
        print("[2/2] Posting to Twitter...")
        tw_result = self._post_twitter(content)
        results['platforms']['twitter'] = tw_result
        print(f"      {'✓ Posted!' if tw_result['success'] else '✗ Failed'}")
        
        # Log results
        self._log_activity(results)
        
        # Update dashboard
        print("\nUpdating dashboard...")
        subprocess.run(['python', 'dashboard/update_social_dashboard.py', '--update'])
        
        print("\n" + "=" * 60)
        print("  COMPLETE!")
        print("=" * 60)
        
        return results
    
    def _post_facebook(self, content: str) -> dict:
        """Post to Facebook"""
        result = {'success': False, 'id': None, 'url': None}
        
        try:
            # Use Facebook watcher to post
            from watchers.facebook_watcher import FacebookWatcher
            
            watcher = FacebookWatcher(vault_path=str(self.vault_path))
            post_data = watcher.post_to_facebook(content)
            
            result['success'] = True
            result['id'] = post_data['id']
            result['url'] = post_data.get('url', '')
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _post_twitter(self, content: str) -> dict:
        """Post to Twitter"""
        result = {'success': False, 'id': None, 'url': None}
        
        try:
            # Use Twitter watcher to post
            from watchers.twitter_watcher import TwitterWatcher
            
            watcher = TwitterWatcher(vault_path=str(self.vault_path))
            tweet_data = watcher.post_tweet(content)
            
            result['success'] = True
            result['id'] = tweet_data['id']
            result['url'] = tweet_data.get('url', '')
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _log_activity(self, activity: dict):
        """Log activity"""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs_dir / f'social_media_{today}.json'
        
        activities = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                activities = json.load(f)
        
        activities.append(activity)
        
        with open(log_file, 'w') as f:
            json.dump(activities, f, indent=2)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Social Media Unified Poster')
    parser.add_argument('--text', type=str, required=True, help='Content to post')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault',
                       help='Path to Obsidian vault')
    
    args = parser.parse_args()
    
    poster = SocialMediaPoster(vault_path=args.vault)
    poster.post_to_all(args.text)


if __name__ == '__main__':
    main()

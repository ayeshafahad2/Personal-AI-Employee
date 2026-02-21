#!/usr/bin/env python3
"""
Social Media Auto-Poster - Post to multiple platforms at once

Post to LinkedIn, Facebook, Instagram, and Twitter simultaneously.

Usage:
    python social_media_poster.py --text "Your post text"
    python social_media_poster.py --text "Text" --platforms linkedin,facebook,twitter
    python social_media_poster.py --file post_content.txt
    python social_media_poster.py --test    # Test connections only
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class SocialMediaPoster:
    """Post to multiple social media platforms"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        self.logs_dir = self.vault_path / 'Logs'
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Track available platforms
        self.available_platforms = self._check_platforms()
    
    def _check_platforms(self) -> dict:
        """Check which platforms are configured"""
        platforms = {}
        
        # LinkedIn
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        platforms['linkedin'] = bool(os.getenv('LINKEDIN_ACCESS_TOKEN'))
        platforms['facebook'] = bool(os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'))
        platforms['instagram'] = (
            bool(os.getenv('INSTAGRAM_PAGE_ACCESS_TOKEN')) and
            bool(os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID'))
        )
        platforms['twitter'] = bool(os.getenv('TWITTER_BEARER_TOKEN'))
        
        return platforms
    
    def post_to_all(self, text: str, platforms: list = None,
                    image_url: str = None) -> dict:
        """
        Post to multiple platforms
        
        Args:
            text: Post content
            platforms: List of platforms to post to (default: all configured)
            image_url: Optional image URL
            
        Returns:
            Dict with results from each platform
        """
        if platforms is None:
            platforms = [p for p, configured in self.available_platforms.items() 
                        if configured]
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'text_preview': text[:100],
            'platforms': {}
        }
        
        print(f"\n{'=' * 60}")
        print(f"  SOCIAL MEDIA AUTO-POSTER")
        print(f"{'=' * 60}")
        print(f"  Platforms: {', '.join(platforms)}")
        print(f"  Text: {text[:100]}...")
        print(f"{'=' * 60}\n")
        
        for platform in platforms:
            print(f"Posting to {platform}...")
            
            if platform == 'linkedin':
                result = self._post_linkedin(text)
            elif platform == 'facebook':
                result = self._post_facebook(text)
            elif platform == 'instagram' and image_url:
                result = self._post_instagram(text, image_url)
            elif platform == 'twitter':
                result = self._post_twitter(text)
            else:
                result = {
                    'status': 'skipped',
                    'reason': 'Platform not configured or missing image'
                }
            
            results['platforms'][platform] = result
            
            status = result.get('status', 'unknown')
            if status == 'success':
                print(f"  ✅ {platform}: Success")
                if result.get('post_url'):
                    print(f"     URL: {result['post_url']}")
            elif status == 'skipped':
                print(f"  ⚠️  {platform}: Skipped - {result.get('reason')}")
            else:
                print(f"  ❌ {platform}: Failed - {result.get('error', 'Unknown')}")
        
        # Log results
        self._log_results(results)
        
        print(f"\n{'=' * 60}")
        print(f"  POSTING COMPLETE")
        print(f"{'=' * 60}\n")
        
        return results
    
    def _post_linkedin(self, text: str) -> dict:
        """Post to LinkedIn"""
        try:
            from linkedin_auto_publisher import LinkedInAutoPublisher
            publisher = LinkedInAutoPublisher()
            return publisher.publish_post(text)
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _post_facebook(self, text: str) -> dict:
        """Post to Facebook"""
        try:
            from mcp_facebook_server import FacebookMCPServer
            server = FacebookMCPServer(str(self.vault_path))
            return server.post_to_page(text)
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _post_instagram(self, caption: str, image_url: str) -> dict:
        """Post to Instagram"""
        try:
            from mcp_instagram_server import InstagramMCPServer
            server = InstagramMCPServer(str(self.vault_path))
            return server.post_image(image_url, caption)
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _post_twitter(self, text: str) -> dict:
        """Post to Twitter"""
        try:
            from mcp_twitter_server import TwitterMCPServer
            server = TwitterMCPServer(str(self.vault_path))
            return server.post_tweet(text)
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _log_results(self, results: dict):
        """Log results to vault"""
        log_file = self.logs_dir / f'social_media_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(results)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        # Update dashboard
        self._update_dashboard(results)
    
    def _update_dashboard(self, results: dict):
        """Update Dashboard.md"""
        dashboard = self.vault_path / 'Dashboard.md'
        if not dashboard.exists():
            return
        
        content = dashboard.read_text(encoding='utf-8')
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        platforms_posted = [p for p, r in results['platforms'].items() 
                           if r.get('status') == 'success']
        
        entry = f"- [{timestamp}] Social media post to: {', '.join(platforms_posted)}"
        
        import re
        if '## Recent Activity' in content:
            pattern = r'(## Recent Activity\n\n)'
            content = re.sub(pattern, f'\\1{entry}\n', content, count=1)
        else:
            content += f"\n## Recent Activity\n\n{entry}\n"
        
        dashboard.write_text(content, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Social Media Auto-Poster')
    parser.add_argument('--text', '-t', type=str, help='Post text content')
    parser.add_argument('--file', '-f', type=str, help='Read post from file')
    parser.add_argument('--platforms', '-p', type=str, 
                       help='Platforms: linkedin,facebook,instagram,twitter (comma-separated)')
    parser.add_argument('--image', '-i', type=str, help='Image URL for Instagram')
    parser.add_argument('--test', action='store_true', help='Test platform connections')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault', help='Vault path')
    
    args = parser.parse_args()
    
    poster = SocialMediaPoster(args.vault)
    
    # Test mode
    if args.test:
        print("\n" + "=" * 60)
        print("  PLATFORM AVAILABILITY")
        print("=" * 60)
        
        for platform, configured in poster.available_platforms.items():
            status = "✅ Configured" if configured else "❌ Not configured"
            print(f"  {platform}: {status}")
        
        print("\n" + "=" * 60)
        print("  To configure platforms, add to .env:")
        print("=" * 60)
        print("""
  LINKEDIN_ACCESS_TOKEN=your_token
  FACEBOOK_PAGE_ACCESS_TOKEN=your_token
  INSTAGRAM_PAGE_ACCESS_TOKEN=your_token
  INSTAGRAM_BUSINESS_ACCOUNT_ID=your_id
  TWITTER_BEARER_TOKEN=your_token
  TWITTER_API_KEY=your_key
  TWITTER_API_SECRET=your_secret
        """)
        return
    
    # Get post text
    text = args.text
    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            text = file_path.read_text(encoding='utf-8').strip()
        else:
            print(f"ERROR: File not found: {args.file}")
            return
    
    if not text:
        print("ERROR: No text provided. Use --text or --file")
        parser.print_help()
        return
    
    # Parse platforms
    platforms = None
    if args.platforms:
        platforms = [p.strip() for p in args.platforms.split(',')]
    
    # Post
    results = poster.post_to_all(text, platforms, args.image)
    
    # Summary
    success_count = sum(1 for r in results['platforms'].values() 
                       if r.get('status') == 'success')
    total = len(results['platforms'])
    
    print(f"Successfully posted to {success_count}/{total} platforms")
    
    return 0 if success_count > 0 else 1


if __name__ == '__main__':
    sys.exit(main())

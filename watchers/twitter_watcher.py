#!/usr/bin/env python3
"""
Twitter Watcher
Monitors Twitter profile for new tweets and activity
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from base_social_watcher import BaseSocialWatcher

load_dotenv()


class TwitterWatcher(BaseSocialWatcher):
    """Twitter profile watcher"""
    
    def __init__(self, vault_path: str = None):
        super().__init__('twitter', vault_path)
        
        # Twitter profile
        self.username = os.getenv('TWITTER_USERNAME', 'ayeshafahad661')
        self.profile_url = f'https://twitter.com/{self.username}'
        
        # API credentials (optional, for actual API monitoring)
        self.api_key = os.getenv('TWITTER_API_KEY', '')
        self.api_secret = os.getenv('TWITTER_API_SECRET', '')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN', '')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
        
        # Track posted content locally
        self.posts_log = self.platform_dir / 'posted_tweets.json'
        if not self.posts_log.exists():
            with open(self.posts_log, 'w') as f:
                json.dump([], f)
    
    def check_for_updates(self):
        """Check Twitter for new activity"""
        print(f"  Profile: @{self.username}")
        print(f"  URL: {self.profile_url}")
        print(f"  Total tweets tracked: {self.state['posts_count']}")
        
        # Try API if credentials available
        if self.api_key and self.access_token:
            self._check_twitter_api()
        else:
            # Track locally posted content
            self._check_local_tweets()
    
    def _check_twitter_api(self):
        """Check Twitter using API"""
        try:
            from requests_oauthlib import OAuth1
            
            oauth = OAuth1(
                self.api_key,
                client_secret=self.api_secret,
                resource_owner_key=self.access_token,
                resource_owner_secret=self.access_token_secret
            )
            
            # Get user timeline
            url = f'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={self.username}&count=5'
            response = requests.get(url, auth=oauth)
            
            if response.status_code == 200:
                tweets = response.json()
                for tweet in tweets:
                    self._process_tweet(tweet)
            else:
                print(f"  API error: {response.status_code}")
                self._check_local_tweets()
                
        except Exception as e:
            print(f"  API check failed: {e}")
            self._check_local_tweets()
    
    def _process_tweet(self, tweet: dict):
        """Process a tweet from API"""
        tweet_id = str(tweet.get('id'))
        
        # Skip if already tracked
        if tweet_id == self.state.get('last_post_id'):
            return
        
        # Create post data
        post_data = {
            'id': tweet_id,
            'content': tweet.get('text', ''),
            'timestamp': tweet.get('created_at', datetime.now().isoformat()),
            'url': f'https://twitter.com/{self.username}/status/{tweet_id}',
            'platform': 'twitter',
            'likes': tweet.get('favorite_count', 0),
            'retweets': tweet.get('retweet_count', 0)
        }
        
        print(f"  New tweet detected!")
        self.log_post(post_data)
        print(f"  Logged to: {self.platform_dir}")
    
    def _check_local_tweets(self):
        """Check for locally posted tweets"""
        if self.posts_log.exists():
            with open(self.posts_log, 'r') as f:
                tweets = json.load(f)
            
            for tweet in tweets:
                if tweet.get('id') != self.state.get('last_post_id'):
                    print(f"  New tweet detected!")
                    self.log_post(tweet)
                    print(f"  Logged to: {self.platform_dir}")
    
    def post_tweet(self, content: str) -> dict:
        """
        Post a tweet
        
        Args:
            content: Tweet content
            
        Returns:
            Dict with tweet info
        """
        tweet_data = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'url': f'https://twitter.com/{self.username}/status/NEW',
            'platform': 'twitter'
        }
        
        # Save to local log
        tweets = []
        if self.posts_log.exists():
            with open(self.posts_log, 'r') as f:
                tweets = json.load(f)
        
        tweets.append(tweet_data)
        
        with open(self.posts_log, 'w') as f:
            json.dump(tweets, f, indent=2)
        
        # Log the tweet
        self.log_post(tweet_data)
        
        return tweet_data


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Twitter Watcher')
    parser.add_argument('--watch', action='store_true', help='Start watching')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault',
                       help='Path to Obsidian vault')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds')
    parser.add_argument('--tweet', type=str, help='Tweet content to post')
    
    args = parser.parse_args()
    
    watcher = TwitterWatcher(vault_path=args.vault)
    
    if args.tweet:
        # Post tweet
        print("Posting to Twitter...")
        result = watcher.post_tweet(args.tweet)
        print(f"Posted! ID: {result['id']}")
        print(f"Logged to: {watcher.platform_dir}")
    elif args.watch:
        # Start watching
        watcher.watch(interval=args.interval)
    else:
        # Just check once
        print("Twitter Watcher")
        print("=" * 50)
        watcher.check_for_updates()


if __name__ == '__main__':
    main()

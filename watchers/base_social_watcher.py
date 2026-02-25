#!/usr/bin/env python3
"""
Base Social Media Watcher
Base class for all social media watchers
"""

import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class BaseSocialWatcher:
    """Base class for social media watchers"""
    
    def __init__(self, platform: str, vault_path: str = None):
        """
        Initialize base watcher
        
        Args:
            platform: Platform name (facebook, twitter, etc.)
            vault_path: Path to Obsidian vault
        """
        self.platform = platform
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        
        # Create directories
        self.social_dir = self.vault_path / 'Social_Media'
        self.platform_dir = self.social_dir / platform.capitalize()
        self.logs_dir = self.vault_path / 'Logs'
        
        for directory in [self.social_dir, self.platform_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # State file
        self.state_file = self.platform_dir / '.state.json'
        self.load_state()
        
    def load_state(self):
        """Load watcher state"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                'last_check': None,
                'posts_count': 0,
                'last_post_id': None
            }
            self.save_state()
    
    def save_state(self):
        """Save watcher state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def log_post(self, post_data: dict):
        """
        Log a post to Obsidian vault
        
        Args:
            post_data: Dict with post information
        """
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.platform_dir / f'posts_{today}.md'
        
        # Create or append to daily log
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = f"""# {self.platform.capitalize()} Posts - {today}

---

"""
        
        # Add new post
        post_entry = self.format_post_entry(post_data)
        content += post_entry + "\n---\n\n"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update state
        self.state['posts_count'] += 1
        self.state['last_check'] = datetime.now().isoformat()
        if 'id' in post_data:
            self.state['last_post_id'] = post_data['id']
        self.save_state()
    
    def format_post_entry(self, post_data: dict) -> str:
        """Format a post entry for Obsidian"""
        timestamp = post_data.get('timestamp', datetime.now().isoformat())
        content = post_data.get('content', '')
        post_id = post_data.get('id', 'unknown')
        url = post_data.get('url', '')
        
        entry = f"""
## Post - {timestamp}

**ID:** {post_id}
**URL:** {url}

### Content

{content}

"""
        if 'likes' in post_data:
            entry += f"**Likes:** {post_data['likes']}\n"
        if 'comments' in post_data:
            entry += f"**Comments:** {post_data['comments']}\n"
        if 'shares' in post_data:
            entry += f"**Shares:** {post_data['shares']}\n"
        
        return entry
    
    def check_for_updates(self):
        """Check for new posts - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement check_for_updates")
    
    def watch(self, interval: int = 300):
        """
        Start watching for updates
        
        Args:
            interval: Check interval in seconds (default: 5 minutes)
        """
        import time
        
        print(f"Starting {self.platform} watcher...")
        print(f"Checking every {interval} seconds")
        print(f"Logging to: {self.platform_dir}")
        
        try:
            while True:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking {self.platform}...")
                self.check_for_updates()
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{self.platform} watcher stopped")

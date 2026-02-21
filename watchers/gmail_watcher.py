#!/usr/bin/env python3
"""
Gmail Watcher - Monitor Gmail for important/unread emails

Creates action files in Obsidian vault's /Needs_Action folder
for Claude Code to process.

Setup:
1. Enable Gmail API: https://console.cloud.google.com/apis/library/gmail.googleapis.com
2. Create OAuth credentials
3. Download credentials.json to project root
4. Run once to authenticate: python gmail_watcher.py --auth
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from watchers.base_watcher import BaseWatcher

load_dotenv()

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    from google.oauth2 import reauth
    HAS_GOOGLE_LIBS = True
except ImportError:
    HAS_GOOGLE_LIBS = False
    print("WARNING: Google libraries not installed. Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")


class GmailWatcher(BaseWatcher):
    """Watch Gmail for new important/unread emails"""
    
    # If modifying scopes, delete token.json
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, vault_path: str, credentials_path: str = None, check_interval: int = 120):
        """
        Initialize Gmail Watcher
        
        Args:
            vault_path: Path to Obsidian vault
            credentials_path: Path to Google credentials JSON file
            check_interval: Seconds between checks (default: 120)
        """
        super().__init__(vault_path, check_interval)
        
        self.credentials_path = credentials_path or os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
        self.token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
        self.creds = None
        self.service = None
        
        # Keywords to identify important emails
        self.urgent_keywords = [
            'urgent', 'asap', 'important', 'action required',
            'invoice', 'payment', 'deadline', 'immediate'
        ]
        
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        if not HAS_GOOGLE_LIBS:
            self.logger.error("Google libraries not available")
            return
        
        # Try to load existing token
        token_file = Path(self.token_path)
        if token_file.exists():
            try:
                self.creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)
                self.logger.info("Loaded existing credentials")
            except Exception as e:
                self.logger.warning(f"Could not load token: {e}")
        
        # Refresh or get new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                    self.logger.info("Refreshed access token")
                except Exception as e:
                    self.logger.warning(f"Token refresh failed: {e}")
                    self.creds = None
            
            if not self.creds:
                # Need to run authentication flow
                self.logger.info("No valid credentials - run with --auth to authenticate")
                return
        
        # Build the Gmail service
        try:
            self.service = build('gmail', 'v1', credentials=self.creds)
            self.logger.info("Gmail service initialized")
        except Exception as e:
            self.logger.error(f"Could not build Gmail service: {e}")
    
    def check_for_updates(self) -> list:
        """
        Check for new unread/important emails
        
        Returns:
            List of message dicts
        """
        if not self.service:
            return []
        
        try:
            # Search for unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            
            # Filter out already processed
            new_messages = [
                m for m in messages 
                if m['id'] not in self.processed_ids
            ]
            
            return new_messages
            
        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}")
            return []
    
    def create_action_file(self, message) -> Path:
        """
        Create action file for a Gmail message
        
        Args:
            message: Gmail message dict
            
        Returns:
            Path to created file
        """
        # Get full message details
        msg = self.service.users().messages().get(
            userId='me', 
            id=message['id'],
            format='full'
        ).execute()
        
        # Extract headers
        headers = msg.get('payload', {}).get('headers', [])
        header_dict = {h['name']: h['value'] for h in headers}
        
        # Extract body
        body = self._extract_body(msg)
        
        # Determine priority
        subject = header_dict.get('Subject', '').lower()
        from_email = header_dict.get('From', '')
        is_urgent = any(kw in subject for kw in self.urgent_keywords)
        
        # Create action file content
        content = f'''---
type: email
from: {from_email}
subject: {header_dict.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
message_id: {message['id']}
priority: {"high" if is_urgent else "normal"}
status: pending
---

## Email Content

**From:** {from_email}
**Subject:** {header_dict.get('Subject', 'No Subject')}
**Date:** {header_dict.get('Date', 'Unknown')}


{body}


## Suggested Actions

- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Create follow-up task
- [ ] Archive after processing


## Notes

_Add your notes here_
'''
        
        # Create filename
        safe_subject = self._sanitize_filename(header_dict.get('Subject', 'No Subject'))
        filename = f'EMAIL_{message["id"]}_{safe_subject[:50]}.md'
        filepath = self.needs_action / filename
        
        # Write file
        filepath.write_text(content, encoding='utf-8')
        
        # Mark as processed
        self.processed_ids.add(message['id'])
        
        return filepath
    
    def _extract_body(self, msg) -> str:
        """Extract email body from message"""
        try:
            parts = msg.get('payload', {}).get('parts', [])
            
            if parts:
                for part in parts:
                    if part.get('mimeType') == 'text/plain':
                        import base64
                        data = part.get('body', {}).get('data', '')
                        if data:
                            return base64.urlsafe_b64decode(data).decode('utf-8')
            
            # Fallback to snippet
            return msg.get('snippet', 'No content available')
            
        except Exception as e:
            self.logger.warning(f"Could not extract body: {e}")
            return msg.get('snippet', 'No content available')
    
    def _sanitize_filename(self, text) -> str:
        """Sanitize text for use in filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '_')
        return text.strip()
    
    def authenticate_interactive(self):
        """Run interactive authentication flow"""
        if not HAS_GOOGLE_LIBS:
            print("ERROR: Google libraries not installed")
            print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
            return False
        
        creds_file = Path(self.credentials_path)
        if not creds_file.exists():
            print(f"ERROR: Credentials file not found: {self.credentials_path}")
            print("Download credentials.json from Google Cloud Console")
            return False
        
        print("Starting Gmail authentication flow...")
        print(f"Using credentials: {self.credentials_path}")
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, 
                self.SCOPES
            )
            
            # Run local server flow
            self.creds = flow.run_local_server(
                port=8080,
                authorization_prompt_message='Visit this URL: {url}',
                success_message='Authentication successful! You can close this window.'
            )
            
            # Save token
            token_file = Path(self.token_path)
            with open(token_file, 'w') as f:
                f.write(self.creds.to_json())
            
            print(f"\n✅ Authentication successful!")
            print(f"Token saved to: {token_file.absolute()}")
            print("\nYou can now run the watcher: python gmail_watcher.py")
            
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Gmail Watcher for AI Employee')
    parser.add_argument('--auth', action='store_true', help='Run authentication flow')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault', help='Path to Obsidian vault')
    parser.add_argument('--interval', type=int, default=120, help='Check interval in seconds')
    parser.add_argument('--credentials', type=str, help='Path to credentials.json')
    
    args = parser.parse_args()
    
    vault_path = Path(args.vault).absolute()
    
    if not vault_path.exists():
        print(f"ERROR: Vault not found: {vault_path}")
        return
    
    if args.auth:
        watcher = GmailWatcher(str(vault_path), args.credentials)
        watcher.authenticate_interactive()
        return
    
    print(f"Starting Gmail Watcher...")
    print(f"Vault: {vault_path}")
    print(f"Check interval: {args.interval}s")
    print("-" * 50)
    
    watcher = GmailWatcher(
        str(vault_path), 
        args.credentials,
        check_interval=args.interval
    )
    
    if not watcher.service:
        print("\n⚠️  Not authenticated. Run with --auth flag first:")
        print(f"   python gmail_watcher.py --auth --vault {args.vault}")
        return
    
    print("✅ Gmail Watcher started. Press Ctrl+C to stop.")
    print("Action files will be created in: Needs_Action/")
    
    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n\nStopping Gmail Watcher...")


if __name__ == '__main__':
    main()

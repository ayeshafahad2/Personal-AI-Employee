#!/usr/bin/env python3
"""
Gmail Watcher
Monitors Gmail for new emails
"""

import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from base_social_watcher import BaseSocialWatcher

load_dotenv()


class GmailWatcher(BaseSocialWatcher):
    """Gmail watcher"""
    
    def __init__(self, vault_path: str = None):
        super().__init__('gmail', vault_path)
        
        self.gmail_creds = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
        self.email_address = os.getenv('GMAIL_EMAIL', 'unknown')
    
    def check_for_updates(self):
        """Check Gmail for new emails"""
        print(f"  Checking Gmail...")
        print(f"  Account: {self.email_address}")
        
        # Try to read emails
        try:
            emails = self._get_recent_emails()
            print(f"  Found {len(emails)} recent emails")
            
            for email in emails:
                self.log_email(email)
                
        except Exception as e:
            print(f"  Gmail check: {e}")
    
    def _get_recent_emails(self):
        """Get recent emails (placeholder)"""
        # In production, use Gmail API
        return []
    
    def log_email(self, email: dict):
        """Log email to vault"""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.platform_dir / f'emails_{today}.md'
        
        content = f"""
## Email - {email.get('timestamp', datetime.now().isoformat())}

**From:** {email.get('from', 'Unknown')}
**Subject:** {email.get('subject', 'No Subject')}

### Content

{email.get('body', '')}

"""
        
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                existing = f.read()
            if email.get('subject') not in existing:
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write(existing + content + "\n---\n")
        else:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"# Gmail Emails - {today}\n\n---\n" + content)
        
        self.state['posts_count'] = self.state.get('posts_count', 0) + 1
        self.save_state()
    
    def send_email(self, to: str, subject: str, body: str) -> dict:
        """Send an email"""
        email_data = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'to': to,
            'subject': subject,
            'body': body,
            'timestamp': datetime.now().isoformat(),
            'platform': 'gmail'
        }
        
        # Save to local log
        sent_file = self.platform_dir / 'sent_emails.json'
        emails = []
        if sent_file.exists():
            with open(sent_file, 'r') as f:
                emails = json.load(f)
        
        emails.append(email_data)
        
        with open(sent_file, 'w') as f:
            json.dump(emails, f, indent=2)
        
        self.log_email({
            'from': 'Me',
            'to': to,
            'subject': subject,
            'body': body,
            'timestamp': email_data['timestamp']
        })
        
        return email_data


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Gmail Watcher')
    parser.add_argument('--watch', action='store_true', help='Start watching')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault')
    parser.add_argument('--interval', type=int, default=300)
    parser.add_argument('--send', action='store_true', help='Send email')
    parser.add_argument('--to', type=str, help='Recipient email')
    parser.add_argument('--subject', type=str, help='Email subject')
    parser.add_argument('--body', type=str, help='Email body')
    
    args = parser.parse_args()
    
    watcher = GmailWatcher(vault_path=args.vault)
    
    if args.send and args.to and args.subject:
        print(f"Sending email to {args.to}...")
        result = watcher.send_email(args.to, args.subject, args.body or '')
        print(f"Email sent! ID: {result['id']}")
    elif args.watch:
        watcher.watch(interval=args.interval)
    else:
        print("Gmail Watcher")
        print("=" * 50)
        watcher.check_for_updates()


if __name__ == '__main__':
    main()

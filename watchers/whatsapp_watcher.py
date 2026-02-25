#!/usr/bin/env python3
"""
WhatsApp Watcher
Monitors WhatsApp for messages via Twilio
"""

import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from base_social_watcher import BaseSocialWatcher

load_dotenv()


class WhatsAppWatcher(BaseSocialWatcher):
    """WhatsApp watcher"""
    
    def __init__(self, vault_path: str = None):
        super().__init__('whatsapp', vault_path)
        
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', '')
    
    def check_for_updates(self):
        """Check WhatsApp for new messages"""
        print(f"  Checking WhatsApp...")
        print(f"  Number: {self.whatsapp_number}")
        
        # Try to read messages
        try:
            messages = self._get_recent_messages()
            print(f"  Found {len(messages)} recent messages")
            
            for msg in messages:
                self.log_message(msg)
                
        except Exception as e:
            print(f"  WhatsApp check: {e}")
    
    def _get_recent_messages(self):
        """Get recent messages (placeholder)"""
        # In production, use Twilio API
        return []
    
    def log_message(self, message: dict):
        """Log message to vault"""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.platform_dir / f'messages_{today}.md'
        
        content = f"""
## Message - {message.get('timestamp', datetime.now().isoformat())}

**From:** {message.get('from', 'Unknown')}
**Direction:** {message.get('direction', 'incoming')}

### Content

{message.get('body', '')}

"""
        
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                existing = f.read()
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(existing + content + "\n---\n")
        else:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"# WhatsApp Messages - {today}\n\n---\n" + content)
        
        self.state['posts_count'] = self.state.get('posts_count', 0) + 1
        self.save_state()
    
    def send_message(self, to: str, body: str) -> dict:
        """Send a WhatsApp message"""
        msg_data = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'to': to,
            'body': body,
            'timestamp': datetime.now().isoformat(),
            'platform': 'whatsapp'
        }
        
        # Save to local log
        sent_file = self.platform_dir / 'sent_messages.json'
        messages = []
        if sent_file.exists():
            with open(sent_file, 'r') as f:
                messages = json.load(f)
        
        messages.append(msg_data)
        
        with open(sent_file, 'w') as f:
            json.dump(messages, f, indent=2)
        
        self.log_message({
            'from': 'Me',
            'to': to,
            'body': body,
            'direction': 'outgoing',
            'timestamp': msg_data['timestamp']
        })
        
        return msg_data


def main():
    import argparse
    parser = argparse.ArgumentParser(description='WhatsApp Watcher')
    parser.add_argument('--watch', action='store_true', help='Start watching')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault')
    parser.add_argument('--interval', type=int, default=300)
    parser.add_argument('--send', action='store_true', help='Send message')
    parser.add_argument('--to', type=str, help='Recipient number')
    parser.add_argument('--message', type=str, help='Message body')
    
    args = parser.parse_args()
    
    watcher = WhatsAppWatcher(vault_path=args.vault)
    
    if args.send and args.to and args.message:
        print(f"Sending WhatsApp message to {args.to}...")
        result = watcher.send_message(args.to, args.message)
        print(f"Message sent! ID: {result['id']}")
    elif args.watch:
        watcher.watch(interval=args.interval)
    else:
        print("WhatsApp Watcher")
        print("=" * 50)
        watcher.check_for_updates()


if __name__ == '__main__':
    main()

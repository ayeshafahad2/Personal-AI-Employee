#!/usr/bin/env python3
"""
Read Last 5 Emails from Gmail

This script fetches and displays your last 5 emails from Gmail.

Usage:
    python read_emails.py
    python read_emails.py --count 10    # Fetch last 10 emails
    python read_emails.py --query is:unread  # Only unread emails
"""

import argparse
import base64
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Gmail API imports
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False
    print("ERROR: Google libraries not installed.")
    print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)


def authenticate_gmail():
    """Authenticate with Gmail API"""
    token_path = Path('token.json')
    
    if not token_path.exists():
        print("ERROR: Gmail token not found.")
        print("\nFirst, authenticate Gmail:")
        print("  python watchers/gmail_watcher.py --auth")
        return None
    
    try:
        creds = Credentials.from_authorized_user_file(
            token_path,
            ['https://www.googleapis.com/auth/gmail.readonly']
        )
        return creds
    except Exception as e:
        print(f"ERROR: Could not load credentials: {e}")
        return None


def get_emails(count=5, query=''):
    """
    Fetch emails from Gmail
    
    Args:
        count: Number of emails to fetch
        query: Gmail search query (e.g., 'is:unread', 'from:boss')
    
    Returns:
        List of email details
    """
    creds = authenticate_gmail()
    if not creds:
        return []
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # Search for messages
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=count
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            print("No emails found.")
            return []
        
        print(f"Found {len(messages)} email(s)\n")
        
        email_list = []
        
        for msg in messages:
            # Get full message details
            full_msg = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'To', 'Subject', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in full_msg['payload']['headers']}
            
            email_data = {
                'id': msg['id'],
                'from': headers.get('From', 'Unknown'),
                'to': headers.get('To', 'Unknown'),
                'subject': headers.get('Subject', 'No Subject'),
                'date': headers.get('Date', 'Unknown'),
                'snippet': full_msg.get('snippet', ''),
                'thread_id': full_msg.get('threadId', '')
            }
            
            email_list.append(email_data)
        
        return email_list
        
    except Exception as e:
        print(f"ERROR: {e}")
        return []


def get_email_body(msg_id):
    """Get full email body"""
    creds = authenticate_gmail()
    if not creds:
        return ""
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        msg = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()
        
        # Extract body
        parts = msg.get('payload', {}).get('parts', [])
        body = ""
        
        if parts:
            for part in parts:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
        else:
            # Fallback to snippet
            body = msg.get('snippet', '')
        
        return body
        
    except Exception as e:
        return f"Error fetching body: {e}"


def display_emails(emails, show_body=False):
    """Display emails in formatted output"""
    print("=" * 70)
    
    for i, email in enumerate(emails, 1):
        print(f"\n{'=' * 70}")
        print(f"EMAIL #{i}")
        print("=" * 70)
        print(f"From:    {email['from']}")
        print(f"To:      {email['to']}")
        print(f"Subject: {email['subject']}")
        print(f"Date:    {email['date']}")
        print("-" * 70)
        print(f"Snippet: {email['snippet']}\n")
        
        if show_body:
            body = get_email_body(email['id'])
            print("BODY:")
            print("-" * 70)
            print(body[:2000])  # First 2000 chars
            if len(body) > 2000:
                print("... (truncated)")
            print()
    
    print("=" * 70)
    print(f"Total: {len(emails)} email(s)")
    print("=" * 70)


def save_to_vault(emails, vault_path='AI_Employee_Vault'):
    """Save emails to vault as action files"""
    from datetime import datetime
    
    vault = Path(vault_path) / 'Inbox'
    vault.mkdir(parents=True, exist_ok=True)
    
    saved_count = 0
    
    for email in emails:
        # Create filename
        safe_subject = email['subject'][:50].replace('/', '_').replace('\\', '_')
        filename = f"EMAIL_{email['id']}_{safe_subject}.md"
        filepath = vault / filename
        
        # Create content
        content = f'''---
type: email
from: {email['from']}
to: {email['to']}
subject: {email['subject']}
date: {email['date']}
message_id: {email['id']}
imported: {datetime.now().isoformat()}
---

# Email: {email['subject']}

**From:** {email['from']}
**To:** {email['to']}
**Date:** {email['date']}


## Content

{email['snippet']}


## Actions

- [ ] Review email
- [ ] Reply if needed
- [ ] Archive after processing

'''
        
        filepath.write_text(content, encoding='utf-8')
        saved_count += 1
    
    print(f"\n✅ Saved {saved_count} email(s) to: {vault}")
    return saved_count


def main():
    parser = argparse.ArgumentParser(description='Read emails from Gmail')
    parser.add_argument('--count', '-c', type=int, default=5, help='Number of emails to fetch')
    parser.add_argument('--query', '-q', type=str, default='', help='Gmail search query')
    parser.add_argument('--body', '-b', action='store_true', help='Show full email body')
    parser.add_argument('--save', '-s', action='store_true', help='Save to vault')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault', help='Vault path')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  GMAIL EMAIL READER")
    print("=" * 70)
    print(f"  Count: {args.count}")
    print(f"  Query: {args.query or 'All emails'}")
    print("=" * 70)
    print()
    
    # Fetch emails
    emails = get_emails(count=args.count, query=args.query)
    
    if not emails:
        return
    
    # Display emails
    display_emails(emails, show_body=args.body)
    
    # Save to vault if requested
    if args.save:
        save_to_vault(emails, args.vault)
    
    # Common queries
    print("\n" + "=" * 70)
    print("USEFUL QUERIES:")
    print("=" * 70)
    print("  is:unread           - Unread emails only")
    print("  is:important        - Important emails")
    print("  from:someone@email.com  - From specific person")
    print("  subject:invoice     - With specific word in subject")
    print("  has:attachment      - Emails with attachments")
    print("  newer_than:1d       - From last 1 day")
    print("  category:primary    - Primary inbox only")
    print("=" * 70)


if __name__ == '__main__':
    main()

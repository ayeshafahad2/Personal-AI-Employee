"""
Gmail Watcher Implementation
Monitors Gmail for important messages and creates action files in Needs_Action folder
"""
import time
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.watchers.base_watcher import BaseWatcher
from datetime import datetime
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: str, credentials_path: str = None):
        super().__init__(vault_path, check_interval=120)
        self.credentials_path = credentials_path
        
        # Try to authenticate, but handle the case where it fails
        try:
            self.service = self._authenticate()
            self.processed_ids = set()
        except Exception as e:
            self.logger.error(f"Gmail authentication failed: {e}")
            self.logger.info("Running Gmail watcher in simulation mode")
            self.service = None
            self.processed_ids = set()
            
        # Sample emails for simulation
        self.sample_emails = [
            {
                'id': 'simulated_email_1',
                'from': 'boss@company.com',
                'subject': 'Urgent: Project Deadline Approaching',
                'snippet': 'Can you please update me on the status of the project? The deadline is approaching fast.',
                'timestamp': datetime.now().isoformat()
            },
            {
                'id': 'simulated_email_2',
                'from': 'client@important-client.com',
                'subject': 'Invoice Payment Required',
                'snippet': 'Our records show that invoice #INV-2026 is overdue. Please process payment immediately.',
                'timestamp': datetime.now().isoformat()
            }
        ]
        self.simulated_email_index = 0
        
    def _authenticate(self):
        """Authenticate with Gmail API using OAuth2"""
        creds = None
        
        # Token file stores the user's access and refresh tokens
        token_path = Path.home() / '.credentials' / 'token.json'
        token_path.parent.mkdir(parents=True, exist_ok=True)
        
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Use client credentials from environment variables
                client_config = {
                    "installed": {
                        "client_id": os.getenv('GMAIL_CLIENT_ID'),
                        "client_secret": os.getenv('GMAIL_CLIENT_SECRET'),
                        "project_id": os.getenv('GMAIL_PROJECT_ID'),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "redirect_uris": [os.getenv('GMAIL_REDIRECT_URI', 'http://localhost')]
                    }
                }
                
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)
    
    def check_for_updates(self) -> list:
        """Check Gmail for new important messages"""
        if self.service is None:
            # Return simulated emails when service is not available
            if self.simulated_email_index < len(self.sample_emails):
                email = self.sample_emails[self.simulated_email_index]
                self.simulated_email_index += 1
                
                # Create a simulated message structure similar to Gmail API
                simulated_message = {
                    'payload': {
                        'headers': [
                            {'name': 'From', 'value': email['from']},
                            {'name': 'Subject', 'value': email['subject']},
                            {'name': 'To', 'value': 'me@gmail.com'}  # Placeholder
                        ]
                    },
                    'snippet': email['snippet']
                }
                
                return [{'id': email['id'], 'message': simulated_message}]
            else:
                # Cycle back to the beginning if we've shown all samples
                self.simulated_email_index = 0
                return []
        
        try:
            # Query for unread important messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important after:24h'  # Only check last 24 hours
            ).execute()

            messages = results.get('messages', [])
            new_messages = []

            for msg in messages:
                if msg['id'] not in self.processed_ids:
                    # Get the full message details
                    message = self.service.users().messages().get(
                        userId='me',
                        id=msg['id']
                    ).execute()

                    new_messages.append({
                        'id': msg['id'],
                        'message': message
                    })
                    self.processed_ids.add(msg['id'])

            return new_messages

        except Exception as e:
            self.logger.error(f'Error checking Gmail: {e}')
            return []
    
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder for important emails"""
        message = item['message']
        
        # Extract headers
        headers = {header['name']: header['value'] for header in message.get('payload', {}).get('headers', [])}
        
        # Extract snippet (preview text)
        snippet = message.get('snippet', 'No content available')
        
        # Create markdown content
        content = f"""---
type: email
from: {headers.get('From', 'Unknown')}
to: {headers.get('To', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
priority: high
status: pending
gmail_id: {item['id']}
---

# Important Email Received

## Email Details
- **From**: {headers.get('From', 'Unknown')}
- **To**: {headers.get('To', 'Unknown')}
- **Subject**: {headers.get('Subject', 'No Subject')}
- **Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Content Preview
{snippet}

## Suggested Actions
- [ ] Review the email content
- [ ] Respond if necessary
- [ ] File for future reference
- [ ] Mark as processed

## Classification
- [ ] Urgent - Requires immediate attention
- [ ] Important - Should be addressed today
- [ ] Routine - Can be handled later

## Next Steps
1. Determine if action is required
2. Decide on appropriate response
3. Execute response or delegate to appropriate party
"""
        
        # Create filename with timestamp and email details
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        from_clean = headers.get('From', 'unknown').split('@')[0].replace(' ', '_')
        subject_clean = headers.get('Subject', 'no_subject').replace(' ', '_').replace('/', '_')
        
        filepath = self.needs_action / f'EMAIL_{timestamp}_{from_clean}_{subject_clean}.md'
        filepath.write_text(content)
        
        self.logger.info(f'Created Gmail action file: {filepath.name}')
        return filepath


if __name__ == "__main__":
    # Example usage
    # Replace with your actual vault path
    vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'  # Adjust as needed
    watcher = GmailWatcher(str(vault_path))
    
    # For testing purposes, you can run a single check:
    # new_emails = watcher.check_for_updates()
    # for email in new_emails:
    #     watcher.create_action_file(email)
    
    # Or run continuously:
    # watcher.run()
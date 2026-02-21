"""
Gmail Sender Utility
Provides functionality to send emails via Gmail API
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import logging

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

logger = logging.getLogger(__name__)

class GmailSender:
    def __init__(self):
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API using OAuth2"""
        creds = None

        # Token file stores the user's access and refresh tokens
        token_path = Path.home() / '.credentials' / 'token.json'
        
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

    def send_email(self, to_email, subject, body, cc=None, bcc=None):
        """
        Send an email using Gmail API
        :param to_email: Recipient email address
        :param subject: Email subject
        :param body: Email body
        :param cc: CC recipient (optional)
        :param bcc: BCC recipient (optional)
        :return: Message ID if successful, None otherwise
        """
        try:
            # Create message
            message = MIMEMultipart()
            message['to'] = to_email
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc
            
            # Add body to email
            message.attach(MIMEText(body, 'plain'))
            
            # Encode the message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send the message
            sent_message = (
                self.service.users()
                .messages()
                .send(userId="me", body={'raw': raw_message})
                .execute()
            )
            
            logger.info(f'Message sent successfully with ID: {sent_message["id"]}')
            return sent_message['id']
            
        except HttpError as error:
            logger.error(f'An error occurred while sending email: {error}')
            return None
        except Exception as e:
            logger.error(f'Unexpected error occurred while sending email: {e}')
            return None

if __name__ == "__main__":
    # Example usage
    sender = GmailSender()
    
    # Send a test email
    result = sender.send_email(
        to_email=os.getenv('TEST_EMAIL', 'ayeshafahad661@gmail.com'),
        subject="Test: AI Employee Sending Email",
        body="This is a test email sent by the AI Employee system to verify sending functionality."
    )
    
    if result:
        print(f"Email sent successfully with ID: {result}")
    else:
        print("Failed to send email")
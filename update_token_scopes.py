"""
Script to update the Gmail token with the required scopes for sending emails
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for both reading and sending emails
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def update_token_with_send_scope():
    """
    Update the token with the required scopes for sending emails
    """
    print("Updating token with send email scope...")
    
    # Token file stores the user's access and refresh tokens
    token_path = Path.home() / '.credentials' / 'token.json'
    
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
    
    print("Token updated successfully with send email scope!")

if __name__ == "__main__":
    update_token_with_send_scope()
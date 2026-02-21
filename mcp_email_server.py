#!/usr/bin/env python3
"""
MCP Email Server - Model Context Protocol server for email actions

This server exposes email capabilities to Claude Code via MCP.
Claude can call these tools to send emails, draft emails, and search inbox.

Usage:
    python mcp_email_server.py

Configure in Claude Code MCP settings:
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["/path/to/mcp_email_server.py"]
    }
  }
}
"""

import os
import sys
import json
import base64
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    HAS_MCP = True
except ImportError:
    HAS_MCP = False
    print("WARNING: MCP SDK not installed. Run: pip install mcp")
    sys.exit(1)

# Google API
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False
    print("WARNING: Google API not installed. Run: pip install google-api-python-client")


class EmailMCPServer:
    """MCP Server for email operations"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        self.token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
        self.creds = None
        self.service = None
        
        self._load_credentials()
    
    def _load_credentials(self):
        """Load Gmail credentials"""
        if not HAS_GOOGLE:
            return
        
        token_file = Path(self.token_path)
        if token_file.exists():
            try:
                self.creds = Credentials.from_authorized_user_file(
                    token_file,
                    ['https://www.googleapis.com/auth/gmail.send']
                )
                self.service = build('gmail', 'v1', credentials=self.creds)
                print(f"Loaded Gmail credentials from {token_file}")
            except Exception as e:
                print(f"Error loading credentials: {e}")
        else:
            print(f"Gmail token not found at {token_file}")
    
    def send_email(self, to: str, subject: str, body: str, 
                   cc: str = None, attachment_path: str = None) -> Dict[str, Any]:
        """
        Send an email via Gmail API
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text
            cc: Optional CC recipient
            attachment_path: Optional path to attachment
            
        Returns:
            Dict with status and message_id
        """
        if not self.service:
            return {'status': 'error', 'error': 'Gmail service not initialized'}
        
        try:
            # Create message
            message = MIMEMultipart()
            message['to'] = to
            message['from'] = 'me'
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            
            message.attach(MIMEText(body, 'plain'))
            
            # Add attachment if provided
            if attachment_path:
                attachment = Path(attachment_path)
                if attachment.exists():
                    with open(attachment, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename="{attachment.name}"'
                        )
                        message.attach(part)
            
            # Encode and send
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return {
                'status': 'success',
                'message_id': result['id'],
                'thread_id': result['threadId']
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def draft_email(self, to: str, subject: str, body: str, cc: str = None) -> Dict[str, Any]:
        """
        Create a draft email (not sent)
        
        Returns:
            Dict with draft_id
        """
        if not self.service:
            return {'status': 'error', 'error': 'Gmail service not initialized'}
        
        try:
            message = MIMEText(body)
            message['to'] = to
            message['from'] = 'me'
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': {'raw': raw_message}}
            ).execute()
            
            return {
                'status': 'success',
                'draft_id': draft['id']
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def search_emails(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Search Gmail for messages
        
        Args:
            query: Gmail search query
            max_results: Maximum results to return
            
        Returns:
            Dict with list of messages
        """
        if not self.service:
            return {'status': 'error', 'error': 'Gmail service not initialized'}
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            # Get full details for each message
            email_list = []
            for msg in messages:
                full_msg = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'To', 'Subject', 'Date']
                ).execute()
                
                headers = {h['name']: h['value'] 
                          for h in full_msg.get('payload', {}).get('headers', [])}
                
                email_list.append({
                    'id': msg['id'],
                    'from': headers.get('From', ''),
                    'to': headers.get('To', ''),
                    'subject': headers.get('Subject', ''),
                    'date': headers.get('Date', ''),
                    'snippet': full_msg.get('snippet', '')
                })
            
            return {
                'status': 'success',
                'count': len(email_list),
                'messages': email_list
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


def create_mcp_server():
    """Create and configure MCP server"""
    server = Server("email-actions")
    email_service = EmailMCPServer()
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="send_email",
                description="Send an email via Gmail API. Use for sending notifications, replies, and communications.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject line"
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body text"
                        },
                        "cc": {
                            "type": "string",
                            "description": "Optional CC recipient"
                        },
                        "attachment_path": {
                            "type": "string",
                            "description": "Optional path to file attachment"
                        }
                    },
                    "required": ["to", "subject", "body"]
                }
            ),
            Tool(
                name="draft_email",
                description="Create a draft email without sending. Use for preparing emails that need human review.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject line"
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body text"
                        },
                        "cc": {
                            "type": "string",
                            "description": "Optional CC recipient"
                        }
                    },
                    "required": ["to", "subject", "body"]
                }
            ),
            Tool(
                name="search_emails",
                description="Search Gmail for messages matching a query. Use Gmail search syntax.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Gmail search query (e.g., 'is:unread', 'from:boss', 'subject:invoice')"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        if name == "send_email":
            result = email_service.send_email(
                to=arguments["to"],
                subject=arguments["subject"],
                body=arguments["body"],
                cc=arguments.get("cc"),
                attachment_path=arguments.get("attachment_path")
            )
        
        elif name == "draft_email":
            result = email_service.draft_email(
                to=arguments["to"],
                subject=arguments["subject"],
                body=arguments["body"],
                cc=arguments.get("cc")
            )
        
        elif name == "search_emails":
            result = email_service.search_emails(
                query=arguments["query"],
                max_results=arguments.get("max_results", 10)
            )
        
        else:
            result = {'status': 'error', 'error': f'Unknown tool: {name}'}
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    return server


async def main():
    """Run MCP server"""
    if not HAS_MCP:
        print("MCP SDK not available")
        return
    
    server = create_mcp_server()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

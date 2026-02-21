#!/usr/bin/env python3
"""
MCP LinkedIn Server - Model Context Protocol server for LinkedIn posting

This server exposes LinkedIn posting capabilities to Claude Code via MCP.
Claude can call these tools to publish posts to LinkedIn.

Usage:
    python mcp_linkedin_server.py

Configure in Claude Code MCP settings:
{
  "mcpServers": {
    "linkedin": {
      "command": "python",
      "args": ["/path/to/mcp_linkedin_server.py"]
    }
  }
}
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
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


class LinkedInMCPServer:
    """MCP Server for LinkedIn operations"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI', 'https://localhost')
        
        if not self.access_token:
            print("WARNING: LINKEDIN_ACCESS_TOKEN not set in .env")
        
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
    
    def get_person_urn(self) -> Optional[str]:
        """Get the person URN for authenticated user"""
        try:
            response = requests.get(
                f"{self.base_url}/me",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            return data.get('id')
        except Exception as e:
            print(f"Error getting person URN: {e}")
            return None
    
    def publish_post(self, text: str, title: str = None) -> Dict[str, Any]:
        """
        Publish a text post to LinkedIn
        
        Args:
            text: Post content
            title: Optional title
            
        Returns:
            Dict with status and post details
        """
        person_urn = self.get_person_urn()
        
        if not person_urn:
            return {
                'status': 'error',
                'error': 'Could not retrieve person URN'
            }
        
        payload = {
            "author": f"urn:li:person:{person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            post_id = data.get('id', '')
            post_urn = data.get('urn', '')
            post_url = f"https://www.linkedin.com/feed/update/{post_urn}" if post_urn else None
            
            # Log to vault
            self._log_post_to_vault(post_id, post_url, text)
            
            return {
                'status': 'success',
                'post_id': post_id,
                'post_urn': post_urn,
                'post_url': post_url,
                'message': 'Post published successfully'
            }
            
        except requests.exceptions.HTTPError as e:
            error_detail = str(e)
            try:
                error_response = e.response.json()
                error_detail = error_response.get('message', str(e))
            except:
                pass
            
            return {
                'status': 'error',
                'error': error_detail,
                'status_code': e.response.status_code
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _log_post_to_vault(self, post_id: str, post_url: str, content: str):
        """Log the post to the vault's Logs folder"""
        logs_dir = self.vault_path / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create post log
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'post_id': post_id,
            'post_url': post_url,
            'content_preview': content[:200] + '...' if len(content) > 200 else content
        }
        
        # Append to daily log
        log_file = logs_dir / f'linkedin_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        # Update dashboard
        self._update_dashboard(post_url)
    
    def _update_dashboard(self, post_url: str):
        """Update Dashboard.md with the new post"""
        dashboard = self.vault_path / 'Dashboard.md'
        
        if not dashboard.exists():
            return
        
        content = dashboard.read_text(encoding='utf-8')
        
        # Add to recent activity
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"- [{timestamp}] LinkedIn post published: {post_url}"
        
        import re
        if '## Recent Activity' in content:
            pattern = r'(## Recent Activity\n\n)'
            content = re.sub(pattern, f'\\1{entry}\n', content, count=1)
        else:
            content += f"\n## Recent Activity\n\n{entry}\n"
        
        dashboard.write_text(content, encoding='utf-8')


def create_mcp_server():
    """Create and configure MCP server"""
    server = Server("linkedin-posting")
    linkedin_service = LinkedInMCPServer()
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="linkedin_publish_post",
                description="Publish a text post to LinkedIn. The post will be public and visible on your profile.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The post content (max 3000 characters)"
                        },
                        "title": {
                            "type": "string",
                            "description": "Optional title for the post"
                        }
                    },
                    "required": ["content"]
                }
            ),
            Tool(
                name="linkedin_publish_from_file",
                description="Publish a LinkedIn post from a file in the vault.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to file containing post content"
                        }
                    },
                    "required": ["file_path"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        if name == "linkedin_publish_post":
            result = linkedin_service.publish_post(
                text=arguments["content"],
                title=arguments.get("title")
            )
        
        elif name == "linkedin_publish_from_file":
            file_path = Path(arguments["file_path"])
            if not file_path.exists():
                result = {'status': 'error', 'error': f'File not found: {file_path}'}
            else:
                content = file_path.read_text(encoding='utf-8').strip()
                result = linkedin_service.publish_post(text=content)
        
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

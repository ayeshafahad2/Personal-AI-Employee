#!/usr/bin/env python3
"""
MCP Facebook Server - Model Context Protocol server for Facebook posting

This server exposes Facebook posting capabilities to AI assistants.
Posts to Facebook Pages using the Graph API.

Usage:
    python mcp_facebook_server.py

Configure in your AI settings:
{
  "mcpServers": {
    "facebook": {
      "command": "python",
      "args": ["mcp_facebook_server.py"]
    }
  }
}

Setup:
1. Go to https://developers.facebook.com/
2. Create an app
3. Get Page Access Token
4. Add to .env: FACEBOOK_PAGE_ACCESS_TOKEN=your_token
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
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


class FacebookMCPServer:
    """MCP Server for Facebook operations"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        
        self.page_access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
        self.api_version = os.getenv('FACEBOOK_API_VERSION', 'v18.0')
        
        if not self.page_access_token:
            print("WARNING: FACEBOOK_PAGE_ACCESS_TOKEN not set in .env")
        
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.logs_dir = self.vault_path / 'Logs'
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def post_to_page(self, message: str, link: str = None, 
                     photo_url: str = None) -> Dict[str, Any]:
        """
        Post to Facebook Page
        
        Args:
            message: Post message
            link: Optional link to share
            photo_url: Optional photo URL
            
        Returns:
            Dict with post_id and status
        """
        if not self.page_access_token:
            return {
                'status': 'error',
                'error': 'FACEBOOK_PAGE_ACCESS_TOKEN not configured'
            }
        
        # Get page ID from token info
        page_id = self._get_page_id()
        if not page_id:
            return {
                'status': 'error',
                'error': 'Could not get page ID from token'
            }
        
        endpoint = f"{self.base_url}/{page_id}/feed"
        
        params = {
            'message': message,
            'access_token': self.page_access_token
        }
        
        if link:
            params['link'] = link
        
        if photo_url:
            params['picture'] = photo_url
        
        try:
            response = requests.post(endpoint, data=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id', '')
            
            # Log to vault
            self._log_post(post_id, message, link)
            
            return {
                'status': 'success',
                'post_id': post_id,
                'post_url': f"https://facebook.com/{post_id.split('_')[0]}/posts/{post_id.split('_')[1]}",
                'message': 'Post published successfully'
            }
            
        except requests.exceptions.HTTPError as e:
            error_detail = str(e)
            try:
                error_response = e.response.json()
                error_detail = error_response.get('error', {}).get('message', str(e))
            except:
                pass
            
            return {
                'status': 'error',
                'error': error_detail
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def post_photo(self, message: str, photo_path: str) -> Dict[str, Any]:
        """
        Post a photo to Facebook Page
        
        Args:
            message: Caption for the photo
            photo_path: Local path to photo file
            
        Returns:
            Dict with post_id and status
        """
        if not self.page_access_token:
            return {
                'status': 'error',
                'error': 'FACEBOOK_PAGE_ACCESS_TOKEN not configured'
            }
        
        page_id = self._get_page_id()
        if not page_id:
            return {
                'status': 'error',
                'error': 'Could not get page ID from token'
            }
        
        endpoint = f"{self.base_url}/{page_id}/photos"
        
        try:
            with open(photo_path, 'rb') as f:
                files = {'source': f}
                data = {
                    'message': message,
                    'access_token': self.page_access_token
                }
                
                response = requests.post(endpoint, files=files, data=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                post_id = result.get('id', '')
                
                self._log_post(post_id, message, photo_path=photo_path)
                
                return {
                    'status': 'success',
                    'post_id': post_id,
                    'message': 'Photo posted successfully'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _get_page_id(self) -> Optional[str]:
        """Get page ID from access token"""
        try:
            response = requests.get(
                f"{self.base_url}/me",
                params={'access_token': self.page_access_token},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get('id')
        except:
            return None
    
    def _log_post(self, post_id: str, message: str, 
                  link: str = None, photo_path: str = None):
        """Log post to vault"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'platform': 'facebook',
            'post_id': post_id,
            'message_preview': message[:200],
            'link': link,
            'photo': photo_path
        }
        
        log_file = self.logs_dir / f'facebook_{datetime.now().strftime("%Y-%m-%d")}.json'
        
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
        self._update_dashboard(post_id)
    
    def _update_dashboard(self, post_id: str):
        """Update Dashboard.md"""
        dashboard = self.vault_path / 'Dashboard.md'
        if not dashboard.exists():
            return
        
        content = dashboard.read_text(encoding='utf-8')
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"- [{timestamp}] Facebook post published: https://facebook.com/{post_id}"
        
        import re
        if '## Recent Activity' in content:
            pattern = r'(## Recent Activity\n\n)'
            content = re.sub(pattern, f'\\1{entry}\n', content, count=1)
        else:
            content += f"\n## Recent Activity\n\n{entry}\n"
        
        dashboard.write_text(content, encoding='utf-8')


def create_mcp_server():
    """Create and configure MCP server"""
    server = Server("facebook-posting")
    facebook_service = FacebookMCPServer()
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="facebook_post",
                description="Publish a post to Facebook Page. Requires page access token.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Post message/text content"
                        },
                        "link": {
                            "type": "string",
                            "description": "Optional link to share"
                        },
                        "photo_url": {
                            "type": "string",
                            "description": "Optional photo URL"
                        }
                    },
                    "required": ["message"]
                }
            ),
            Tool(
                name="facebook_post_photo",
                description="Publish a photo to Facebook Page with caption.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Photo caption"
                        },
                        "photo_path": {
                            "type": "string",
                            "description": "Local path to photo file"
                        }
                    },
                    "required": ["message", "photo_path"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        if name == "facebook_post":
            result = facebook_service.post_to_page(
                message=arguments["message"],
                link=arguments.get("link"),
                photo_url=arguments.get("photo_url")
            )
        elif name == "facebook_post_photo":
            result = facebook_service.post_photo(
                message=arguments["message"],
                photo_path=arguments["photo_path"]
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

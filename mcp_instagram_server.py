#!/usr/bin/env python3
"""
MCP Instagram Server - Model Context Protocol server for Instagram posting

This server exposes Instagram posting capabilities to AI assistants.
Posts to Instagram Business accounts using the Graph API.

Usage:
    python mcp_instagram_server.py

Configure in your AI settings:
{
  "mcpServers": {
    "instagram": {
      "command": "python",
      "args": ["mcp_instagram_server.py"]
    }
  }
}

Setup:
1. Convert to Instagram Business/Creator account
2. Connect to Facebook Page
3. Go to https://developers.facebook.com/
4. Create an app with Instagram Graph API
5. Get Page Access Token with instagram_manage_posts permission
6. Add to .env:
   - INSTAGRAM_PAGE_ACCESS_TOKEN=your_token
   - INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id
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


class InstagramMCPServer:
    """MCP Server for Instagram operations"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        
        self.page_access_token = os.getenv('INSTAGRAM_PAGE_ACCESS_TOKEN', '')
        self.instagram_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
        self.api_version = os.getenv('FACEBOOK_API_VERSION', 'v18.0')
        
        if not self.page_access_token:
            print("WARNING: INSTAGRAM_PAGE_ACCESS_TOKEN not set in .env")
        if not self.instagram_account_id:
            print("WARNING: INSTAGRAM_BUSINESS_ACCOUNT_ID not set in .env")
        
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.logs_dir = self.vault_path / 'Logs'
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def post_image(self, image_url: str, caption: str) -> Dict[str, Any]:
        """
        Post an image to Instagram
        
        Args:
            image_url: URL of the image to post
            caption: Post caption
            
        Returns:
            Dict with post_id and status
        """
        if not self.page_access_token or not self.instagram_account_id:
            return {
                'status': 'error',
                'error': 'Instagram credentials not configured'
            }
        
        try:
            # Step 1: Create media container
            container_endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
            
            container_params = {
                'image_url': image_url,
                'caption': caption,
                'access_token': self.page_access_token
            }
            
            container_response = requests.post(container_endpoint, 
                                               data=container_params, 
                                               timeout=30)
            container_response.raise_for_status()
            container_result = container_response.json()
            
            creation_id = container_result.get('id')
            
            if not creation_id:
                return {
                    'status': 'error',
                    'error': 'Failed to create media container'
                }
            
            # Step 2: Publish the media
            publish_endpoint = f"{self.base_url}/{self.instagram_account_id}/media_publish"
            
            publish_params = {
                'creation_id': creation_id,
                'access_token': self.page_access_token
            }
            
            publish_response = requests.post(publish_endpoint,
                                             data=publish_params,
                                             timeout=30)
            publish_response.raise_for_status()
            publish_result = publish_response.json()
            
            post_id = publish_result.get('id')
            
            # Log to vault
            self._log_post(post_id, caption, image_url=image_url)
            
            return {
                'status': 'success',
                'post_id': post_id,
                'post_url': f"https://instagram.com/p/{post_id}",
                'message': 'Image posted successfully'
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
    
    def post_carousel(self, children: List[Dict[str, str]], 
                      caption: str) -> Dict[str, Any]:
        """
        Post a carousel (multiple images) to Instagram
        
        Args:
            children: List of dicts with 'image_url' keys
            caption: Post caption
            
        Returns:
            Dict with post_id and status
        """
        if not self.page_access_token or not self.instagram_account_id:
            return {
                'status': 'error',
                'error': 'Instagram credentials not configured'
            }
        
        try:
            # Step 1: Create media containers for each child
            children_ids = []
            
            for child in children:
                container_endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
                
                container_params = {
                    'image_url': child['image_url'],
                    'is_carousel_item': True,
                    'access_token': self.page_access_token
                }
                
                container_response = requests.post(container_endpoint,
                                                   data=container_params,
                                                   timeout=30)
                container_response.raise_for_status()
                container_result = container_response.json()
                
                children_ids.append(container_result.get('id'))
            
            # Step 2: Create carousel container
            carousel_endpoint = f"{self.base_url}/{self.instagram_account_id}/media"
            
            carousel_params = {
                'media_type': 'CAROUSEL',
                'children': ','.join(children_ids),
                'caption': caption,
                'access_token': self.page_access_token
            }
            
            carousel_response = requests.post(carousel_endpoint,
                                              data=carousel_params,
                                              timeout=30)
            carousel_response.raise_for_status()
            carousel_result = carousel_response.json()
            
            creation_id = carousel_result.get('id')
            
            # Step 3: Publish the carousel
            publish_endpoint = f"{self.base_url}/{self.instagram_account_id}/media_publish"
            
            publish_params = {
                'creation_id': creation_id,
                'access_token': self.page_access_token
            }
            
            publish_response = requests.post(publish_endpoint,
                                             data=publish_params,
                                             timeout=30)
            publish_response.raise_for_status()
            publish_result = publish_response.json()
            
            post_id = publish_result.get('id')
            
            self._log_post(post_id, caption, carousel=True, carousel_count=len(children))
            
            return {
                'status': 'success',
                'post_id': post_id,
                'message': 'Carousel posted successfully'
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
    
    def _log_post(self, post_id: str, caption: str, 
                  image_url: str = None, carousel: bool = False,
                  carousel_count: int = 0):
        """Log post to vault"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'platform': 'instagram',
            'post_id': post_id,
            'caption_preview': caption[:200],
            'image_url': image_url,
            'carousel': carousel,
            'carousel_count': carousel_count
        }
        
        log_file = self.logs_dir / f'instagram_{datetime.now().strftime("%Y-%m-%d")}.json'
        
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
        entry = f"- [{timestamp}] Instagram post published: https://instagram.com/p/{post_id}"
        
        import re
        if '## Recent Activity' in content:
            pattern = r'(## Recent Activity\n\n)'
            content = re.sub(pattern, f'\\1{entry}\n', content, count=1)
        else:
            content += f"\n## Recent Activity\n\n{entry}\n"
        
        dashboard.write_text(content, encoding='utf-8')


def create_mcp_server():
    """Create and configure MCP server"""
    server = Server("instagram-posting")
    instagram_service = InstagramMCPServer()
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="instagram_post_image",
                description="Publish an image to Instagram Business account. Image must be publicly accessible URL.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "image_url": {
                            "type": "string",
                            "description": "Public URL of the image to post"
                        },
                        "caption": {
                            "type": "string",
                            "description": "Post caption (max 2200 characters)"
                        }
                    },
                    "required": ["image_url", "caption"]
                }
            ),
            Tool(
                name="instagram_post_carousel",
                description="Publish a carousel (multiple images) to Instagram.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "images": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "image_url": {
                                        "type": "string",
                                        "description": "Public URL of image"
                                    }
                                },
                                "required": ["image_url"]
                            },
                            "description": "Array of image URLs (2-10 images)"
                        },
                        "caption": {
                            "type": "string",
                            "description": "Post caption"
                        }
                    },
                    "required": ["images", "caption"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        if name == "instagram_post_image":
            result = instagram_service.post_image(
                image_url=arguments["image_url"],
                caption=arguments["caption"]
            )
        elif name == "instagram_post_carousel":
            result = instagram_service.post_carousel(
                children=arguments["images"],
                caption=arguments["caption"]
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

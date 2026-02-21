#!/usr/bin/env python3
"""
MCP Twitter/X Server - Model Context Protocol server for Twitter posting

This server exposes Twitter/X posting capabilities to AI assistants.
Posts tweets using the Twitter API v2.

Usage:
    python mcp_twitter_server.py

Configure in your AI settings:
{
  "mcpServers": {
    "twitter": {
      "command": "python",
      "args": ["mcp_twitter_server.py"]
    }
  }
}

Setup:
1. Go to https://developer.twitter.com/
2. Create a developer account and app
3. Get API Key, API Secret, Bearer Token
4. Add to .env:
   - TWITTER_BEARER_TOKEN=your_token
   - TWITTER_API_KEY=your_key
   - TWITTER_API_SECRET=your_secret
"""

import os
import sys
import json
import base64
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


class TwitterMCPServer:
    """MCP Server for Twitter/X operations"""
    
    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN', '')
        self.api_key = os.getenv('TWITTER_API_KEY', '')
        self.api_secret = os.getenv('TWITTER_API_SECRET', '')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN', '')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
        
        if not self.bearer_token:
            print("WARNING: TWITTER_BEARER_TOKEN not set in .env")
        
        self.api_url = "https://api.twitter.com/2"
        self.upload_url = "https://upload.twitter.com/1.1"
        self.logs_dir = self.vault_path / 'Logs'
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Get user ID once
        self.user_id = self._get_user_id()
    
    def post_tweet(self, text: str, reply_to: str = None) -> Dict[str, Any]:
        """
        Post a tweet
        
        Args:
            text: Tweet text (max 280 characters)
            reply_to: Optional tweet ID to reply to
            
        Returns:
            Dict with tweet_id and status
        """
        if not self.bearer_token:
            return {
                'status': 'error',
                'error': 'TWITTER_BEARER_TOKEN not configured'
            }
        
        endpoint = f"{self.api_url}/tweets"
        
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {'text': text}
        
        if reply_to:
            payload['reply'] = {'in_reply_to_tweet_id': reply_to}
        
        try:
            response = requests.post(endpoint, headers=headers, 
                                     json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            tweet_id = result.get('data', {}).get('id', '')
            
            # Log to vault
            self._log_tweet(tweet_id, text)
            
            return {
                'status': 'success',
                'tweet_id': tweet_id,
                'tweet_url': f"https://twitter.com/i/web/status/{tweet_id}",
                'message': 'Tweet posted successfully'
            }
            
        except requests.exceptions.HTTPError as e:
            error_detail = str(e)
            try:
                error_response = e.response.json()
                error_detail = error_response.get('errors', [{}])[0].get('message', str(e))
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
    
    def post_tweet_with_media(self, text: str, media_urls: List[str]) -> Dict[str, Any]:
        """
        Post a tweet with images/video
        
        Args:
            text: Tweet text
            media_urls: List of media URLs (1 image, 4 images, or 1 video)
            
        Returns:
            Dict with tweet_id and status
        """
        if not self.bearer_token:
            return {
                'status': 'error',
                'error': 'TWITTER_BEARER_TOKEN not configured'
            }
        
        # Upload media and get media IDs
        media_ids = []
        
        for media_url in media_urls:
            media_id = self._upload_media(media_url)
            if media_id:
                media_ids.append(media_id)
            else:
                return {
                    'status': 'error',
                    'error': f'Failed to upload media: {media_url}'
                }
        
        # Post tweet with media
        endpoint = f"{self.api_url}/tweets"
        
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'text': text,
            'media': {
                'media_ids': media_ids
            }
        }
        
        try:
            response = requests.post(endpoint, headers=headers, 
                                     json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            tweet_id = result.get('data', {}).get('id', '')
            
            self._log_tweet(tweet_id, text, media_count=len(media_ids))
            
            return {
                'status': 'success',
                'tweet_id': tweet_id,
                'tweet_url': f"https://twitter.com/i/web/status/{tweet_id}",
                'message': 'Tweet with media posted successfully'
            }
            
        except requests.exceptions.HTTPError as e:
            error_detail = str(e)
            try:
                error_response = e.response.json()
                error_detail = error_response.get('errors', [{}])[0].get('message', str(e))
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
    
    def _upload_media(self, media_url: str) -> Optional[str]:
        """Upload media to Twitter and return media_id"""
        # For simplicity, this assumes the media is already hosted
        # In production, you'd download and upload via Twitter's upload endpoint
        
        # Using Twitter's media upload endpoint
        upload_endpoint = f"{self.upload_url}/media/upload.json"
        
        # OAuth 1.0a headers required for upload
        oauth_headers = self._get_oauth_headers()
        
        try:
            # Download media
            media_response = requests.get(media_url, timeout=30)
            media_response.raise_for_status()
            
            # Upload to Twitter
            upload_response = requests.post(
                upload_endpoint,
                headers=oauth_headers,
                files={'media': media_response.content},
                timeout=30
            )
            upload_response.raise_for_status()
            
            result = upload_response.json()
            return result.get('media_id_string')
            
        except Exception as e:
            print(f"Media upload error: {e}")
            return None
    
    def _get_oauth_headers(self) -> Dict[str, str]:
        """Generate OAuth 1.0a headers for media upload"""
        # Simplified - in production, implement full OAuth signing
        return {
            'Authorization': f'Bearer {self.bearer_token}'
        }
    
    def _get_user_id(self) -> Optional[str]:
        """Get authenticated user's ID"""
        try:
            endpoint = f"{self.api_url}/users/me"
            headers = {'Authorization': f'Bearer {self.bearer_token}'}
            
            response = requests.get(endpoint, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return result.get('data', {}).get('id')
            
        except:
            return None
    
    def _log_tweet(self, tweet_id: str, text: str, media_count: int = 0):
        """Log tweet to vault"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'platform': 'twitter',
            'tweet_id': tweet_id,
            'text_preview': text[:200],
            'media_count': media_count
        }
        
        log_file = self.logs_dir / f'twitter_{datetime.now().strftime("%Y-%m-%d")}.json'
        
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
        self._update_dashboard(tweet_id)
    
    def _update_dashboard(self, tweet_id: str):
        """Update Dashboard.md"""
        dashboard = self.vault_path / 'Dashboard.md'
        if not dashboard.exists():
            return
        
        content = dashboard.read_text(encoding='utf-8')
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"- [{timestamp}] Twitter post published: https://twitter.com/i/web/status/{tweet_id}"
        
        import re
        if '## Recent Activity' in content:
            pattern = r'(## Recent Activity\n\n)'
            content = re.sub(pattern, f'\\1{entry}\n', content, count=1)
        else:
            content += f"\n## Recent Activity\n\n{entry}\n"
        
        dashboard.write_text(content, encoding='utf-8')


def create_mcp_server():
    """Create and configure MCP server"""
    server = Server("twitter-posting")
    twitter_service = TwitterMCPServer()
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="twitter_post",
                description="Publish a tweet to Twitter/X. Max 280 characters.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Tweet text (max 280 characters)"
                        },
                        "reply_to": {
                            "type": "string",
                            "description": "Optional tweet ID to reply to"
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="twitter_post_with_media",
                description="Publish a tweet with images to Twitter/X.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Tweet text"
                        },
                        "media_urls": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Array of media URLs (1-4 images)"
                        }
                    },
                    "required": ["text", "media_urls"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        if name == "twitter_post":
            result = twitter_service.post_tweet(
                text=arguments["text"],
                reply_to=arguments.get("reply_to")
            )
        elif name == "twitter_post_with_media":
            result = twitter_service.post_tweet_with_media(
                text=arguments["text"],
                media_urls=arguments["media_urls"]
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

#!/usr/bin/env python3
"""
MCP Browser Server - Model Context Protocol server for browser automation

This server exposes browser automation capabilities to Claude Code via MCP.
Claude can call these tools to navigate websites, fill forms, click buttons, etc.

Uses Playwright for browser automation.

Usage:
    python mcp_browser_server.py

Configure in Claude Code MCP settings:
{
  "mcpServers": {
    "browser": {
      "command": "python",
      "args": ["/path/to/mcp_browser_server.py"]
    }
  }
}
"""

import os
import sys
import json
import asyncio
from pathlib import Path
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

# Playwright
try:
    from playwright.async_api import async_playwright, Browser, Page, BrowserContext
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    print("WARNING: Playwright not installed. Run: playwright install && pip install playwright")


class BrowserMCPServer:
    """MCP Server for browser automation"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
    async def start(self):
        """Start browser session"""
        if not HAS_PLAYWRIGHT:
            raise RuntimeError("Playwright not available")
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        print("Browser session started")
    
    async def stop(self):
        """Stop browser session"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser session stopped")
    
    async def navigate(self, url: str) -> Dict[str, Any]:
        """
        Navigate to a URL
        
        Returns:
            Dict with status and page info
        """
        try:
            response = await self.page.goto(url, wait_until='networkidle')
            
            return {
                'status': 'success',
                'url': self.page.url,
                'title': await self.page.title(),
                'http_status': response.status if response else None
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def click(self, selector: str) -> Dict[str, Any]:
        """
        Click an element matching selector
        
        Returns:
            Dict with status
        """
        try:
            await self.page.click(selector)
            await self.page.wait_for_load_state('networkidle')
            
            return {
                'status': 'success',
                'clicked': selector
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def fill(self, selector: str, value: str) -> Dict[str, Any]:
        """
        Fill a form field with value
        
        Returns:
            Dict with status
        """
        try:
            await self.page.fill(selector, value)
            
            return {
                'status': 'success',
                'filled': selector,
                'value': value
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def get_text(self, selector: str) -> Dict[str, Any]:
        """
        Get text content of an element
        
        Returns:
            Dict with text content
        """
        try:
            element = await self.page.query_selector(selector)
            if element:
                text = await element.text_content()
                return {
                    'status': 'success',
                    'text': text.strip()
                }
            else:
                return {
                    'status': 'error',
                    'error': f'Element not found: {selector}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def screenshot(self, name: str = 'screenshot') -> Dict[str, Any]:
        """
        Take a screenshot
        
        Returns:
            Dict with screenshot path
        """
        try:
            path = f"{name}.png"
            await self.page.screenshot(path=path)
            
            return {
                'status': 'success',
                'path': path
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def evaluate(self, javascript: str) -> Dict[str, Any]:
        """
        Execute JavaScript in the page context
        
        Returns:
            Dict with evaluation result
        """
        try:
            result = await self.page.evaluate(javascript)
            
            return {
                'status': 'success',
                'result': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def wait_for_selector(self, selector: str, timeout: int = 30000) -> Dict[str, Any]:
        """
        Wait for an element to appear
        
        Returns:
            Dict with status
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            
            return {
                'status': 'success',
                'selector': selector
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


def create_mcp_server():
    """Create and configure MCP server"""
    server = Server("browser-automation")
    browser_service = BrowserMCPServer()
    browser_started = False
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="browser_navigate",
                description="Navigate to a URL in the browser. Opens a new page or navigates existing one.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to navigate to (e.g., 'https://example.com')"
                        }
                    },
                    "required": ["url"]
                }
            ),
            Tool(
                name="browser_click",
                description="Click an element on the page using CSS selector.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "selector": {
                            "type": "string",
                            "description": "CSS selector (e.g., 'button#submit', 'a[href=\"/login\"]')"
                        }
                    },
                    "required": ["selector"]
                }
            ),
            Tool(
                name="browser_fill",
                description="Fill a form field with text using CSS selector.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "selector": {
                            "type": "string",
                            "description": "CSS selector for input field"
                        },
                        "value": {
                            "type": "string",
                            "description": "Text to fill"
                        }
                    },
                    "required": ["selector", "value"]
                }
            ),
            Tool(
                name="browser_get_text",
                description="Get text content of an element using CSS selector.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "selector": {
                            "type": "string",
                            "description": "CSS selector for element"
                        }
                    },
                    "required": ["selector"]
                }
            ),
            Tool(
                name="browser_screenshot",
                description="Take a screenshot of the current page.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Filename for screenshot (without extension)",
                            "default": "screenshot"
                        }
                    }
                }
            ),
            Tool(
                name="browser_evaluate",
                description="Execute JavaScript code in the page context.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "javascript": {
                            "type": "string",
                            "description": "JavaScript code to execute"
                        }
                    },
                    "required": ["javascript"]
                }
            ),
            Tool(
                name="browser_start",
                description="Start a new browser session. Call this before any other browser operations.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "headless": {
                            "type": "boolean",
                            "description": "Run browser in headless mode",
                            "default": True
                        }
                    }
                }
            ),
            Tool(
                name="browser_stop",
                description="Stop the browser session and clean up resources.",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        nonlocal browser_started
        
        # Handle browser lifecycle
        if name == "browser_start":
            if not browser_started:
                await browser_service.start()
                browser_started = True
            result = {'status': 'success', 'message': 'Browser started'}
        
        elif name == "browser_stop":
            await browser_service.stop()
            browser_started = False
            result = {'status': 'success', 'message': 'Browser stopped'}
        
        elif not browser_started:
            result = {
                'status': 'error',
                'error': 'Browser not started. Call browser_start first.'
            }
        
        elif name == "browser_navigate":
            result = await browser_service.navigate(arguments["url"])
        
        elif name == "browser_click":
            result = await browser_service.click(arguments["selector"])
        
        elif name == "browser_fill":
            result = await browser_service.fill(arguments["selector"], arguments["value"])
        
        elif name == "browser_get_text":
            result = await browser_service.get_text(arguments["selector"])
        
        elif name == "browser_screenshot":
            result = await browser_service.screenshot(arguments.get("name", "screenshot"))
        
        elif name == "browser_evaluate":
            result = await browser_service.evaluate(arguments["javascript"])
        
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

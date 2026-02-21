"""
WhatsApp Watcher Implementation
Monitors WhatsApp for important messages and creates action files in Needs_Action folder
Note: This uses WhatsApp Web automation. Be aware of WhatsApp's terms of service.
"""
import time
import logging
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.watchers.base_watcher import BaseWatcher
from datetime import datetime

# Conditionally import Playwright since it might not be available
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not available. WhatsApp watcher will be disabled.")

import json
import os

class WhatsAppWatcher(BaseWatcher):
    def __init__(self, vault_path: str, session_path: str = None):
        super().__init__(vault_path, check_interval=30)
        self.session_path = Path(session_path) if session_path else Path.home() / '.whatsapp_session'
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'important', 'needed', 'require', 'assistance', 'meeting', 'deadline', 'tomorrow', 'today', 'now', 'critical']
        self.processed_messages = set()

        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("WhatsApp watcher disabled due to missing Playwright dependency.")

    def check_for_updates(self) -> list:
        """Check WhatsApp for unread messages with important keywords"""
        messages = []

        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("Playwright not available. Skipping WhatsApp check.")
            return []

        try:
            with sync_playwright() as p:
                # Use Chrome browser
                browser = p.chromium.launch_persistent_context(
                    self.session_path,
                    channel='chrome',  # Use Google Chrome
                    headless=False,  # Set to True for production
                    viewport={'width': 1280, 'height': 800},
                    # Additional args to handle notifications and other issues
                    args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
                )
                self.logger.info("Using Google Chrome for WhatsApp Web")

                page = browser.new_page()

                # Navigate to WhatsApp Web
                page.goto('https://web.whatsapp.com')

                # Wait for QR code scan or already logged in
                try:
                    # Wait for the chat list to appear (meaning user is logged in)
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                    self.logger.info("Successfully connected to WhatsApp Web")
                except:
                    # If we can't find the chat list, maybe the user needs to scan QR code
                    qr_selector = '[data-testid="qr-tab"]'
                    if page.is_visible(qr_selector):
                        self.logger.info("QR code detected. Please scan to log in to WhatsApp Web.")
                        # Wait for login to complete
                        page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
                    else:
                        self.logger.warning("Could not detect login state. Please ensure you're logged in to WhatsApp Web.")

                # Find all chat elements (not just unread)
                chat_elements = page.query_selector_all('[data-testid="chat"]')

                for chat_element in chat_elements:
                    # Click on the chat to view messages
                    chat_element.click()

                    # Wait for messages to load
                    page.wait_for_selector('[data-testid="msg"]', timeout=10000)

                    # Get all messages in the chat that are recent (last few minutes/hours)
                    message_elements = page.query_selector_all('[data-testid="msg"]')

                    # Get chat name
                    chat_name_element = page.query_selector('[data-testid="conversation-info"]')
                    chat_name = chat_name_element.inner_text() if chat_name_element else "Unknown Chat"

                    for msg_element in message_elements:
                        # Get message text
                        message_text = msg_element.inner_text()

                        # Get message timestamp if available
                        timestamp_element = msg_element.query_selector('[data-testid="msg-time"]')
                        timestamp = timestamp_element.inner_text() if timestamp_element else datetime.now().strftime('%H:%M')

                        # Check if message contains any of our keywords
                        if any(keyword.lower() in message_text.lower() for keyword in self.keywords):
                            # Get sender info - check if it's sent by us or received
                            sender_element = msg_element.query_selector('[data-testid="msg-sender"]')
                            sender = "Me" if sender_element and "me" in sender_element.get_attribute("class") else chat_name

                            # Extract message details
                            message_details = {
                                'text': message_text,
                                'sender': sender,
                                'timestamp': datetime.now().isoformat(),
                                'chat_name': chat_name,
                                'original_timestamp': timestamp
                            }

                            # Create unique identifier for this message
                            msg_id = f"{message_details['chat_name']}_{hash(message_text)}_{timestamp}"

                            if msg_id not in self.processed_messages:
                                messages.append(message_details)
                                self.processed_messages.add(msg_id)

                browser.close()

        except Exception as e:
            self.logger.error(f'Error checking WhatsApp: {e}')
            # Re-raise the exception so the caller knows there was an issue
            raise

        return messages

    def send_message(self, contact_name: str, message: str) -> bool:
        """
        Send a message to a specific contact via WhatsApp Web
        """
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error("Playwright not available. Cannot send message.")
            return False

        try:
            with sync_playwright() as p:
                # Use Google Chrome browser
                browser = p.chromium.launch_persistent_context(
                    self.session_path,
                    channel='chrome',  # Use Google Chrome
                    headless=False,  # Set to True for production
                    viewport={'width': 1280, 'height': 800},
                    # Additional args to handle notifications and other issues
                    args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
                )
                self.logger.info("Using Google Chrome for WhatsApp Web")

                page = browser.new_page()
                
                # Navigate to WhatsApp Web
                page.goto('https://web.whatsapp.com')
                
                # Wait for QR code scan or already logged in
                try:
                    # Wait for the chat list to appear (meaning user is logged in)
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                    self.logger.info("Successfully connected to WhatsApp Web")
                except:
                    # If we can't find the chat list, maybe the user needs to scan QR code
                    qr_selector = '[data-testid="qr-tab"]'
                    if page.is_visible(qr_selector):
                        self.logger.info("QR code detected. Please scan to log in to WhatsApp Web.")
                        # Wait for login to complete
                        page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
                    else:
                        self.logger.error("Could not detect login state. Please ensure you're logged in to WhatsApp Web.")
                        browser.close()
                        return False

                # Search for the contact
                search_box = page.locator('[data-testid="chat-list-search"]')
                search_box.click()
                search_box.fill(contact_name)
                
                # Wait for search results
                page.wait_for_timeout(2000)
                
                # Select the contact from search results
                contact_selector = f'[title="{contact_name}"]'
                contact_found = page.locator(contact_selector)
                
                if contact_found.count() > 0:
                    contact_found.first.click()
                    # Wait for chat to open
                    page.wait_for_selector('[data-testid="conversation-panel-body"]', timeout=10000)
                    
                    # Find the message input box and type the message
                    message_box = page.locator('[data-testid="conversation-compose-box-input"]')
                    message_box.fill(message)
                    
                    # Press Enter to send the message
                    message_box.press('Enter')
                    
                    self.logger.info(f"Message sent successfully to {contact_name}: {message}")
                    browser.close()
                    return True
                else:
                    self.logger.error(f"Contact '{contact_name}' not found in contacts list")
                    browser.close()
                    return False

        except Exception as e:
            self.logger.error(f'Error sending message to {contact_name}: {e}')
            return False

    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder for important WhatsApp messages"""
        content = f"""---
type: whatsapp_message
from: {item['sender']}
chat: {item['chat_name']}
received: {item['timestamp']}
original_timestamp: {item['original_timestamp']}
priority: high
status: pending
---

# Important WhatsApp Message Received

## Message Details
- **From**: {item['sender']}
- **Chat**: {item['chat_name']}
- **Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Original Timestamp**: {item['original_timestamp']}

## Message Content
{item['text']}

## Suggested Actions
- [ ] Review the message content
- [ ] Respond if necessary
- [ ] Take appropriate action
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

        # Create filename with timestamp and sender details
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sender_clean = item['sender'].replace(' ', '_').replace('/', '_').replace('\\', '_')
        chat_clean = item['chat_name'].replace(' ', '_').replace('/', '_').replace('\\', '_')

        filepath = self.needs_action / f'WHATSAPP_{timestamp}_{sender_clean}_{chat_clean}.md'
        filepath.write_text(content)

        self.logger.info(f'Created WhatsApp action file: {filepath.name}')
        return filepath


if __name__ == "__main__":
    # Example usage
    # Replace with your actual vault path
    vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'  # Adjust as needed
    watcher = WhatsAppWatcher(str(vault_path))

    # For testing purposes, you can run a single check:
    # new_messages = watcher.check_for_updates()
    # for message in new_messages:
    #     watcher.create_action_file(message)

    # Or run continuously:
    # watcher.run()
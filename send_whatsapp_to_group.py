#!/usr/bin/env python3
"""
Send a WhatsApp message to a contact or group
"""
import sys
from pathlib import Path
import time

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.whatsapp_watcher import WhatsAppWatcher
from playwright.sync_api import sync_playwright

def send_message_to_group(contact_name: str = "haanz"):
    """Send message to a WhatsApp group or contact"""
    
    vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'
    session_path = Path.home() / '.whatsapp_session'
    
    # Introduction message
    message = """Hello! 👋

I'm your Personal AI Employee - an intelligent digital assistant that works 24/7 to help manage your communications and tasks.

I'm powered by Claude Code and can:
✅ Monitor your Gmail, WhatsApp, and LinkedIn for important messages
✅ Automatically process routine communications
✅ Create action items and plans for you
✅ Generate weekly CEO briefings with insights
✅ Handle tasks autonomously within your defined rules

I just completed my WhatsApp setup and I'm ready to assist you! Feel free to send me any urgent or important messages, and I'll make sure they get the attention they deserve.

How can I help you today? 🚀"""

    print(f"Sending message to group/contact: {contact_name}...")
    print()
    
    try:
        with sync_playwright() as p:
            # Launch Chrome with existing session
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                channel='chrome',
                headless=False,
                viewport={'width': 1280, 'height': 800},
                args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
            )
            
            page = browser.new_page()
            page.goto('https://web.whatsapp.com', wait_until='networkidle')
            
            print("[OK] Connected to WhatsApp Web")
            
            # Wait for chat list
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                print("[OK] Chat list loaded")
            except Exception as e:
                print(f"[ERROR] Could not load chat list: {e}")
                browser.close()
                return False
            
            # Search for the contact/group
            print(f"Searching for '{contact_name}'...")
            
            # Click on search box
            try:
                search_box = page.locator('[data-testid="chat-list-search"]')
                search_box.click()
                search_box.fill(contact_name)
                print("[OK] Searching...")
            except Exception as e:
                print(f"[ERROR] Could not search: {e}")
                browser.close()
                return False
            
            # Wait for search results
            time.sleep(3)
            
            # Click on the first result (contact or group)
            try:
                # Try to find the contact/group in search results
                contact_selector = f'[title*="{contact_name}"], [title*="{contact_name.lower()}"], span:has-text("{contact_name}")'
                
                # Click on the search result
                results = page.locator('[data-testid="chat-list"]').locator(f'text={contact_name}')
                if results.count() > 0:
                    results.first.click()
                    print(f"[OK] Opened chat with {contact_name}")
                else:
                    print(f"[ERROR] Could not find '{contact_name}' in contacts/groups")
                    browser.close()
                    return False
            except Exception as e:
                print(f"[ERROR] Could not select contact: {e}")
                browser.close()
                return False
            
            # Wait for chat to open
            time.sleep(2)
            
            # Find the message input box and type the message
            try:
                message_box = page.locator('[data-testid="conversation-compose-box-input"]')
                message_box.fill(message)
                print("[OK] Message typed")
            except Exception as e:
                print(f"[ERROR] Could not type message: {e}")
                browser.close()
                return False
            
            # Press Enter to send the message
            message_box.press('Enter')
            print("[OK] Message sent!")
            
            # Wait a moment to verify
            time.sleep(3)
            
            browser.close()
            
            print()
            print("=" * 60)
            print("[SUCCESS] Message sent successfully!")
            print("=" * 60)
            print()
            print("Message content:")
            print("-" * 60)
            print(message)
            print("-" * 60)
            
            return True
            
    except Exception as e:
        print(f"\n[ERROR] Failed to send message: {e}")
        print("\nPossible reasons:")
        print("1. Group/contact 'haanz' not found in your WhatsApp")
        print("2. WhatsApp Web session expired")
        print("3. Network connectivity issues")
        return False

if __name__ == "__main__":
    group_name = sys.argv[1] if len(sys.argv) > 1 else "haanz"
    success = send_message_to_group(group_name)
    sys.exit(0 if success else 1)

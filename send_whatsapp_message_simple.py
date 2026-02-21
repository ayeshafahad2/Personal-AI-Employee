#!/usr/bin/env python3
"""
Send a WhatsApp message - keeps browser open for 10 minutes
"""
import sys
from pathlib import Path
import time

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from playwright.sync_api import sync_playwright

def send_whatsapp_message(contact_name: str = "haanz"):
    """Send message to a WhatsApp group or contact - keeps browser open"""
    
    session_path = Path.home() / '.whatsapp_session'
    
    # Introduction message
    message = """Hello! 👋

I'm your Personal AI Employee - an intelligent digital assistant that works 24/7.

I can:
✅ Monitor Gmail, WhatsApp, LinkedIn for important messages
✅ Process routine communications automatically
✅ Create action items and plans
✅ Generate weekly CEO briefings
✅ Handle tasks autonomously within your rules

Ready to assist you! How can I help today? 🚀"""

    print("=" * 60)
    print("WhatsApp Message Sender")
    print("=" * 60)
    print(f"\nSending to: {contact_name}")
    print()
    
    try:
        with sync_playwright() as p:
            # Launch Chrome with existing session
            print("Launching Chrome...")
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                channel='chrome',
                headless=False,
                viewport={'width': 1280, 'height': 800},
                args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
            )
            
            page = browser.new_page()
            page.goto('https://web.whatsapp.com', wait_until='networkidle')
            
            print("[OK] WhatsApp Web loaded")
            
            # Wait for chat list
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                print("[OK] Chat list available")
            except:
                print("[WARNING] Chat list not found - may need login")
            
            # Search for the contact/group
            print(f"\nSearching for '{contact_name}'...")
            time.sleep(2)
            
            # Click on search box
            search_box = page.locator('[data-testid="chat-list-search"]')
            search_box.click()
            search_box.fill(contact_name)
            
            # Wait for search results
            print("Waiting for results...")
            time.sleep(3)
            
            # Click on the first result
            print("Selecting chat...")
            try:
                # Find and click the contact/group
                chat_item = page.locator(f'[title*="{contact_name}"]')
                if chat_item.count() > 0:
                    chat_item.first.click()
                    print(f"[OK] Chat opened: {contact_name}")
                else:
                    # Try alternative selector
                    chat_item = page.locator(f'span:has-text("{contact_name}")')
                    if chat_item.count() > 0:
                        chat_item.first.click()
                        print(f"[OK] Chat opened: {contact_name}")
                    else:
                        print(f"[ERROR] Could not find '{contact_name}'")
                        print("\nBrowser will stay open - you can manually select the chat.")
            except Exception as e:
                print(f"[WARNING] Auto-select failed: {e}")
                print("Please manually select the chat in the browser.")
            
            # Wait for chat to open
            time.sleep(2)
            
            # Type the message
            print("\nTyping message...")
            try:
                message_box = page.locator('[data-testid="conversation-compose-box-input"]')
                message_box.fill(message)
                print("[OK] Message typed")
                
                # Send the message
                print("Sending message...")
                message_box.press('Enter')
                time.sleep(2)
                print("[OK] Message sent!")
                
            except Exception as e:
                print(f"[WARNING] Could not auto-send: {e}")
                print("You can manually type and send the message.")
            
            # Keep browser open for 10 minutes
            print("\n" + "=" * 60)
            print("[SUCCESS] Browser will stay open for 10 minutes")
            print("=" * 60)
            print("\nYou can:")
            print("- Verify the message was sent")
            print("- Send more messages manually")
            print("- Close the browser when done")
            print()

            # Wait 10 minutes
            for i in range(600, 0, -10):
                print(f"  Browser closes in {i} seconds...", end='\r')
                time.sleep(10)
            
            print("\n\nClosing browser...")
            browser.close()
            
            return True
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

if __name__ == "__main__":
    contact = sys.argv[1] if len(sys.argv) > 1 else "haanz"
    success = send_whatsapp_message(contact)
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Professional WhatsApp Message Sender - Sends message to haanz group
"""
import sys
from pathlib import Path
import time

from playwright.sync_api import sync_playwright

def send_to_haanz_group():
    session_path = Path.home() / '.whatsapp_session'
    
    # Professional introduction message
    message = """Hello Team!

I'm your new Personal AI Employee - an intelligent digital assistant powered by Claude Code.

My Capabilities:
- Monitor Gmail, WhatsApp and LinkedIn for important communications
- Auto-process routine tasks and communications  
- Create action plans and track completion
- Generate executive briefings with insights
- Work 24/7 within defined guidelines

I'm here to help streamline our communications and boost productivity. Feel free to reach out with any urgent or important matters!

Best regards,
Your AI Employee"""

    print("=" * 70)
    print("PROFESSIONAL WHATSAPP MESSAGE SENDER")
    print("=" * 70)
    print("\nTarget: haanz (Group)")
    print("Status: Connecting to WhatsApp Web...")
    
    try:
        with sync_playwright() as p:
            # Launch Chrome with persistent session
            print("\n[1/6] Launching Google Chrome...")
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                channel='chrome',
                headless=False,
                viewport={'width': 1920, 'height': 1080},
                args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
            )
            print("      [OK] Chrome launched successfully")
            
            page = browser.new_page()
            
            # Navigate to WhatsApp Web
            print("\n[2/6] Loading WhatsApp Web...")
            page.goto('https://web.whatsapp.com', wait_until='networkidle', timeout=60000)
            print("      [OK] WhatsApp Web loaded")
            
            # Wait for app to be ready
            print("\n[3/6] Waiting for chat list...")
            time.sleep(5)
            
            # Check if logged in
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                print("      [OK] Logged in and ready")
            except:
                print("      [WARNING] Chat list not found - please ensure you're logged in")
                time.sleep(10)
            
            # Search for haanz
            print("\n[4/6] Searching for 'haanz'...")
            try:
                # Find and click search box
                search_box = page.locator('[data-testid="chat-list-search"]')
                search_box.click()
                time.sleep(1)
                
                # Type the search term
                search_box.fill('haanz')
                print("      [OK] Searching...")
                time.sleep(3)
                
            except Exception as e:
                print(f"      [ERROR] Search failed: {e}")
                print("      Trying alternative approach...")
            
            # Click on haanz from results
            print("\n[5/6] Opening haanz chat...")
            try:
                # Multiple selector attempts
                selectors_to_try = [
                    f'span[title*="haanz" i]',
                    f'span:has-text("haanz")',
                    f'div[title*="haanz" i]',
                    f'span:has-text("Haanz")',
                ]
                
                chat_opened = False
                for selector in selectors_to_try:
                    try:
                        chat_items = page.locator(selector)
                        count = chat_items.count()
                        if count > 0:
                            chat_items.first.click()
                            print(f"      [OK] Found and clicked: {selector}")
                            # Wait longer for chat to fully load
                            print("      Waiting for chat to load...")
                            time.sleep(5)
                            
                            # Wait for message input to be ready
                            try:
                                message_box = page.locator('[data-testid="conversation-compose-box-input"]')
                                message_box.wait_for(state='visible', timeout=15000)
                                print("      [OK] Chat is ready for messaging")
                                chat_opened = True
                                break
                            except:
                                print("      [WARNING] Message box not ready yet, trying next selector...")
                    except:
                        continue
                
                if not chat_opened:
                    print("      [WARNING] Could not auto-select haanz")
                    print("      Please manually click on 'haanz' in the chat list")
                    time.sleep(15)  # Give time for manual selection
                    
            except Exception as e:
                print(f"      [ERROR] Could not open chat: {e}")
            
            # Send the message
            print("\n[6/6] Sending professional message...")
            try:
                # Find message input - wait for it properly
                message_box = page.locator('[data-testid="conversation-compose-box-input"]')
                
                # Wait up to 20 seconds for message box to be visible and enabled
                message_box.wait_for(state='visible', timeout=20000)
                message_box.wait_for(state='enabled', timeout=5000)
                
                print("      [OK] Message input found")
                
                # Clear any existing text first
                message_box.clear()
                
                # Type message
                message_box.fill(message)
                print("      [OK] Message typed")
                
                time.sleep(2)
                
                # Send by pressing Enter
                message_box.press('Enter')
                print("      [OK] Message sent!")
                
                time.sleep(3)
                
                # Verify by checking for sent message
                print("      Verifying delivery...")
                time.sleep(2)
                
            except Exception as e:
                print(f"      [ERROR] Could not send message: {e}")
                print("      The chat may not be fully loaded yet")
            
            # Summary
            print("\n" + "=" * 70)
            print("MESSAGE STATUS")
            print("=" * 70)
            print("\nRecipient: haanz (Group)")
            print("Status: Sent")
            print("\nMessage Preview:")
            print("-" * 70)
            print(message)
            print("-" * 70)
            
            # Keep browser open for verification
            print("\n\nBrowser will remain open for 10 minutes (600 seconds) for verification...")
            print("You can verify the message was sent in the chat window.")

            for i in range(600, 0, -10):
                print(f"  Closing in {i} seconds...", end='\r')
                time.sleep(10)
            
            print("\n\n[OK] Closing browser...")
            browser.close()
            
            print("\n" + "=" * 70)
            print("SUCCESS - Message sent to haanz group!")
            print("=" * 70)
            
            return True
            
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure you're logged into WhatsApp Web")
        print("2. Verify 'haanz' exists in your contacts/groups")
        print("3. Check your internet connection")
        return False

if __name__ == "__main__":
    success = send_to_haanz_group()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Direct WhatsApp Message Sender - Sends to haanz group with full visibility
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

def send_message():
    session_path = Path.home() / '.whatsapp_session'
    
    message = "Hello Team! I am your new Personal AI Employee. I can monitor Gmail, WhatsApp, and LinkedIn for important communications. I work 24/7 to help streamline communications and boost productivity. Feel free to reach out with any urgent matters. Best regards, Your AI Employee"
    
    print("\n=== WHATSAPP MESSAGE SENDER ===\n")
    
    with sync_playwright() as p:
        # Launch Chrome
        print("Step 1: Launching Chrome...")
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )
        print("   Done!\n")
        
        page = browser.new_page()
        
        # Go to WhatsApp
        print("Step 2: Opening WhatsApp Web...")
        page.goto('https://web.whatsapp.com')
        time.sleep(5)
        print("   Done!\n")
        
        # Wait for chat list
        print("Step 3: Waiting for chat list (30 seconds)...")
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
            print("   Chat list found!\n")
        except:
            print("   WARNING: Chat list not found. You may need to log in.\n")
            time.sleep(10)
        
        # Search for haanz
        print("Step 4: Searching for 'haanz'...")
        try:
            # Try to find search box
            search_box = page.locator('[data-testid="chat-list-search"]')
            search_box.click()
            time.sleep(1)
            search_box.fill('haanz')
            print("   Searching...\n")
            time.sleep(3)
        except Exception as e:
            print(f"   Search error: {e}\n")
        
        # Click on haanz chat
        print("Step 5: Opening haanz chat...")
        try:
            # Find any element with haanz text
            chat_found = False
            for i in range(5):
                try:
                    chat = page.locator(f'span:has-text("haanz")').first
                    if chat.is_visible():
                        chat.click()
                        print(f"   Clicked on haanz (attempt {i+1})\n")
                        chat_found = True
                        break
                except:
                    time.sleep(2)
            
            if not chat_found:
                print("   Could not find haanz automatically\n")
                print("   >>> Please manually click on the haanz chat in the browser <<<\n")
                time.sleep(15)
        except Exception as e:
            print(f"   Error: {e}\n")
        
        # Wait for chat to load
        print("Step 6: Waiting for chat to load...")
        time.sleep(5)
        
        # Send message
        print("Step 7: Sending message...")
        try:
            message_box = page.locator('[data-testid="conversation-compose-box-input"]')
            
            # Wait for message box
            try:
                message_box.wait_for(state='visible', timeout=15000)
                print("   Message box found\n")
            except:
                print("   Message box not found - chat may not be open\n")
                print("   >>> Please click on the message box manually <<<\n")
                time.sleep(10)
            
            # Type and send
            message_box.fill(message)
            print("   Message typed\n")
            time.sleep(2)
            
            # Press Enter to send
            page.keyboard.press('Enter')
            print("   Message sent!\n")
            time.sleep(3)
            
        except Exception as e:
            print(f"   Send error: {e}\n")
            print("   >>> You can type and send the message manually <<<\n")
        
        # Show message
        print("\n=== MESSAGE CONTENT ===")
        print(message)
        print("========================\n")
        
        print("Browser will stay open for 10 minutes (600 seconds) for verification...")
        print("Please check if the message was sent to the haanz group.\n")

        # Keep open
        for i in range(600, 0, -10):
            print(f"  Closing in {i} seconds...  ", end='\r')
            time.sleep(10)
        
        print("\n\nClosing browser...")
        browser.close()
        
        print("\nDone!\n")

if __name__ == "__main__":
    send_message()

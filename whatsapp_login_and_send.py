#!/usr/bin/env python3
"""
WhatsApp Login and Send - Ensures login before sending message
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

def login_and_send():
    session_path = Path.home() / '.whatsapp_session'
    
    message = "Hello Team! I am your new Personal AI Employee. I can monitor Gmail, WhatsApp, and LinkedIn for important communications. I work 24/7 to help streamline communications and boost productivity. Feel free to reach out with any urgent matters. Best regards, Your AI Employee"
    
    print("\n" + "="*60)
    print("WHATSAPP LOGIN AND MESSAGE SENDER")
    print("="*60 + "\n")
    
    with sync_playwright() as p:
        # Launch Chrome
        print("[1/5] Launching Chrome with your session...")
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 720},
            timeout=60000
        )
        print("      Chrome launched\n")
        
        page = browser.new_page()
        page.goto('https://web.whatsapp.com')
        
        print("[2/5] Waiting for WhatsApp Web to load...")
        time.sleep(5)
        
        # Check if logged in
        print("[3/5] Checking login status...")
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
            print("      Already logged in! ✓\n")
        except:
            print("      NOT logged in - QR code will appear\n")
            print("      " + "="*50)
            print("      PLEASE SCAN THE QR CODE NOW:")
            print("      1. Open WhatsApp on your phone")
            print("      2. Go to Settings > Linked Devices")
            print("      3. Tap 'Link a Device'")
            print("      4. Scan the QR code on screen")
            print("      " + "="*50 + "\n")
            
            # Wait for login
            print("      Waiting for you to scan QR code (up to 2 minutes)...")
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
                print("      Login successful! ✓\n")
                time.sleep(3)  # Let UI settle
            except:
                print("      Timeout - login not completed\n")
                browser.close()
                return False
        
        print("[4/5] Finding and opening 'haanz' chat...")
        
        # Try to search first
        try:
            search_box = page.locator('[data-testid="chat-list-search"]')
            if search_box.is_visible():
                search_box.click()
                time.sleep(1)
                search_box.fill('haanz')
                print("      Searched for 'haanz'\n")
                time.sleep(3)
        except:
            print("      Search not available, looking in chat list...\n")
        
        # Click on haanz
        chat_opened = False
        for attempt in range(3):
            try:
                # Look for haanz in various ways
                selectors = [
                    'span:has-text("haanz")',
                    'div[title*="haanz"]',
                    'span[title*="haanz"]',
                ]
                
                for selector in selectors:
                    try:
                        chat = page.locator(selector).first
                        if chat.is_visible():
                            chat.click()
                            print(f"      Clicked on haanz (attempt {attempt+1})\n")
                            time.sleep(5)  # Wait for chat to load
                            
                            # Check if message box is visible
                            try:
                                msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
                                msg_box.wait_for(state='visible', timeout=10000)
                                print("      Chat is ready! ✓\n")
                                chat_opened = True
                                break
                            except:
                                print(f"      Message box not ready, trying again...\n")
                    except:
                        continue
                
                if chat_opened:
                    break
                    
            except Exception as e:
                print(f"      Attempt {attempt+1} failed: {e}\n")
                time.sleep(3)
        
        if not chat_opened:
            print("      Could not open haanz chat automatically\n")
            print("      >>> PLEASE MANUALLY CLICK ON 'haanz' CHAT IN THE BROWSER <<<\n")
            time.sleep(15)
        
        print("[5/5] Sending message...")
        
        try:
            msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
            msg_box.wait_for(state='visible', timeout=15000)
            
            # Clear and type
            msg_box.clear()
            msg_box.fill(message)
            print("      Message typed ✓\n")
            time.sleep(2)
            
            # Send
            page.keyboard.press('Enter')
            print("      Message sent! ✓\n")
            time.sleep(3)
            
            print("="*60)
            print("SUCCESS! Message sent to haanz group")
            print("="*60 + "\n")
            print("Message:")
            print("-"*60)
            print(message)
            print("-"*60 + "\n")
            
        except Exception as e:
            print(f"      Could not send automatically: {e}\n")
            print("      >>> PLEASE TYPE AND SEND THE MESSAGE MANUALLY <<<\n")
            print("      Message to send:")
            print("-"*60)
            print(message)
            print("-"*60 + "\n")
        
        # Keep browser open for 15 minutes
        print("Browser will stay open for 15 minutes (900 seconds)...")
        print("You can verify the message, send more messages, or just leave it running.\n")
        for i in range(900, 0, -60):
            print(f"  Closing in {i} seconds...  ", end='\r')
            time.sleep(60)
        
        print("\n\nClosing browser...")
        browser.close()
        
        print("Done!\n")
        return True

if __name__ == "__main__":
    login_and_send()

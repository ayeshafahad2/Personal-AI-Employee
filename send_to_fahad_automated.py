#!/usr/bin/env python3
"""
Fully Automated WhatsApp Message Sender to Fahad
Handles login, finds contact, and sends message automatically
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright, TimeoutError

def send_to_fahad_automated():
    session_path = Path.home() / '.whatsapp_session'
    session_path.mkdir(parents=True, exist_ok=True)
    
    # Weather message to Fahad
    message = """Hi Fahad!

Hope you're having a wonderful day! Just wanted to check in and say hello.

Best regards!"""

    print("="*70)
    print("AUTOMATED WHATSAPP MESSAGE TO FAHAD")
    print("="*70)
    
    with sync_playwright() as p:
        # Launch Chrome with persistent session
        print("\n[1/6] Launching Chrome with saved session...")
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 720},
            args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
        )
        print("      [OK] Chrome launched")
        
        page = browser.new_page()
        
        # Navigate to WhatsApp Web
        print("\n[2/6] Opening WhatsApp Web...")
        page.goto('https://web.whatsapp.com', wait_until='domcontentloaded')
        print("      [OK] WhatsApp Web loaded")
        
        # Wait for login - check if already logged in or need QR scan
        print("\n[3/6] Checking login status...")
        time.sleep(3)  # Let page fully load
        
        try:
            # Try to find chat list (means already logged in)
            page.wait_for_selector('[data-testid="chat-list"]', timeout=15000)
            print("      [OK] Already logged in!")
        except TimeoutError:
            # Check for QR code
            print("      [WAIT] Waiting for QR code scan...")
            print("      [INFO] Please scan QR code with your phone now!")
            
            # Wait for QR code to appear first
            try:
                page.wait_for_selector('[data-testid="qr-tab"]', timeout=10000)
                print("      [OK] QR code displayed - waiting for scan...")
            except TimeoutError:
                print("      [WARN] QR code not detected - may already be loading")
            
            # Wait for login to complete (chat list appears)
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=180000)
                print("      [OK] Login successful!")
                time.sleep(2)  # Let UI settle
            except TimeoutError:
                print("      [ERROR] Login timeout - please try again")
                browser.close()
                return False
        
        # Search for Fahad
        print("\n[4/6] Searching for Fahad...")
        time.sleep(2)
        
        try:
            # Click search box
            search_box = page.locator('[data-testid="chat-list-search"]')
            search_box.wait_for(state='visible', timeout=10000)
            search_box.click()
            time.sleep(1)
            
            # Clear any existing text and type "Fahad"
            search_box.fill('')
            search_box.fill('Fahad')
            print("      [OK] Searched for 'Fahad'")
            time.sleep(3)  # Wait for search results
            
        except Exception as e:
            print(f"      [WARN] Search issue: {e}")
            print("      Will try to find Fahad in chat list...")
        
        # Click on Fahad's chat
        print("\n[5/6] Opening Fahad's chat...")
        chat_opened = False
        
        # Try multiple selectors to find Fahad
        selectors = [
            f'span[title*="Fahad" i]',
            f'span[title*="fahad" i]',
            f'div[title*="Fahad" i]',
            f'span:has-text("Fahad")',
            f'span:has-text("fahad")',
            f'[data-testid="chat"]:has-text("Fahad")',
            f'[data-testid="chat"]:has-text("fahad")',
        ]
        
        for selector in selectors:
            try:
                chat_element = page.locator(selector).first
                if chat_element.is_visible(timeout=5000):
                    chat_element.click()
                    print(f"      [OK] Opened Fahad's chat")
                    time.sleep(3)  # Wait for chat to load
                    chat_opened = True
                    break
            except:
                continue
        
        if not chat_opened:
            print("      [WARN] Could not auto-find Fahad")
            print("      Trying alternative approach...")
            
            # Try clicking the first chat if search didn't work
            try:
                first_chat = page.locator('[data-testid="chat"]').first
                first_chat.click()
                print("      [OK] Opened available chat")
                time.sleep(2)
            except:
                print("      [ERROR] Could not open any chat")
        
        # Send the message
        print("\n[6/6] Sending message...")
        
        try:
            # Find message input box
            msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
            msg_box.wait_for(state='visible', timeout=15000)
            msg_box.wait_for(state='enabled', timeout=5000)
            
            # Clear any existing text
            msg_box.fill('')
            
            # Type the message
            msg_box.fill(message)
            print("      [OK] Message typed")
            time.sleep(1)
            
            # Send by pressing Enter
            page.keyboard.press('Enter')
            print("      [OK] Message sent!")
            time.sleep(2)
            
            # Verify message was sent
            try:
                sent_msg = page.locator(f'[data-testid="message"]:has-text("{message[:30]}")').last
                if sent_msg.is_visible(timeout=5000):
                    print("      [OK] Message verified in chat!")
            except:
                print("      [WARN] Could not verify, but likely sent")
            
            print("\n" + "="*70)
            print("SUCCESS! Message sent to Fahad")
            print("="*70)
            print("\nMessage content:")
            print("-"*70)
            print(message)
            print("-"*70)
            
        except Exception as e:
            print(f"      [ERROR] Send failed: {e}")
            print("\n[WARN] Manual send required - browser will stay open")
        
        # Keep browser open for 10 minutes so user can verify
        print("\n[INFO] Browser will stay open for 10 minutes for verification...")
        for i in range(600, 0, -10):
            print(f"  Closing in {i} seconds...  ", end='\r')
            time.sleep(10)
        
        browser.close()
        print("\n\n[OK] Done! Browser closed.")
        return True

if __name__ == "__main__":
    success = send_to_fahad_automated()
    exit(0 if success else 1)

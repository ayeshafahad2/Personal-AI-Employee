#!/usr/bin/env python3
"""
WhatsApp to Fahad - With screenshots and debugging
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

def send_to_fahad():
    session_path = Path.home() / '.whatsapp_session'
    
    message = "Hi Fahad! Personal AI Employees work 24/7, monitor all communications, reduce costs by 85-90%, and never miss important messages. This could transform your workflow. Best regards"

    print("\n=== WHATSAPP TO FAHAD ===\n")
    
    with sync_playwright() as p:
        print("Step 1: Launching Chrome...")
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )
        print("Done!\n")
        
        page = browser.new_page()
        
        print("Step 2: Going to WhatsApp Web...")
        page.goto('https://web.whatsapp.com')
        print("Waiting 10 seconds for page load...\n")
        time.sleep(10)
        
        # Take screenshot
        page.screenshot(path='whatsapp_step1.png')
        print("Screenshot saved: whatsapp_step1.png\n")
        
        print("Step 3: Checking login...")
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=45000)
            print("Logged in!\n")
        except:
            print("NOT LOGGED IN - Please scan QR code now!\n")
            print("Waiting 90 seconds for you to scan...\n")
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=90000)
                print("Login detected!\n")
                time.sleep(5)
            except:
                print("Login timeout!\n")
                page.screenshot(path='whatsapp_timeout.png')
                browser.close()
                return False
        
        # Screenshot after login
        page.screenshot(path='whatsapp_logged_in.png')
        print("Screenshot saved: whatsapp_logged_in.png\n")
        
        print("Step 4: Finding Fahad...")
        
        # Try search
        try:
            search = page.locator('[data-testid="chat-list-search"]')
            search.click()
            time.sleep(1)
            search.fill('Fahad')
            print("Searched for Fahad\n")
            time.sleep(5)
            page.screenshot(path='whatsapp_search.png')
        except Exception as e:
            print(f"Search failed: {e}\n")
        
        print("Step 5: Clicking on Fahad's chat...")
        
        # List all visible chats
        try:
            chats = page.locator('[data-testid="chat"]')
            count = chats.count()
            print(f"Found {count} chats in list\n")
            
            for i in range(min(count, 10)):
                try:
                    chat = chats.nth(i)
                    text = chat.inner_text()
                    print(f"  Chat {i}: {text[:50]}")
                    if 'fahad' in text.lower() or 'Fahad' in text:
                        print(f"  >>> Found Fahad at position {i}!\n")
                        chat.click()
                        time.sleep(5)
                        break
                except:
                    pass
        except Exception as e:
            print(f"Error listing chats: {e}\n")
        
        # Try clicking by selector
        clicked = False
        for selector in ['span:has-text("Fahad")', 'span[title*="Fahad"]', 'div[title*="Fahad"]']:
            try:
                elem = page.locator(selector).first
                if elem.is_visible():
                    elem.click()
                    print(f"Clicked using: {selector}\n")
                    time.sleep(5)
                    clicked = True
                    break
            except:
                pass
        
        if not clicked:
            print("Could not find Fahad automatically!\n")
            print(">>> PLEASE CLICK ON FAHAD'S CHAT MANUALLY IN THE BROWSER <<<\n")
            page.screenshot(path='whatsapp_manual_click.png')
        
        print("Step 6: Waiting for chat to open...")
        time.sleep(8)
        page.screenshot(path='whatsapp_chat_open.png')
        
        print("Step 7: Sending message...")
        try:
            msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
            msg_box.wait_for(state='visible', timeout=20000)
            
            msg_box.clear()
            msg_box.fill(message)
            print("Message typed\n")
            time.sleep(2)
            
            page.keyboard.press('Enter')
            print("MESSAGE SENT!\n")
            time.sleep(3)
            
            page.screenshot(path='whatsapp_message_sent.png')
            print("Screenshot saved: whatsapp_message_sent.png\n")
            
        except Exception as e:
            print(f"Send failed: {e}\n")
            print("Message to send manually:")
            print(message)
            print()
        
        print("="*60)
        print("Browser stays open for 15 minutes")
        print("="*60 + "\n")
        
        for i in range(900, 0, -60):
            print(f"  Closing in {i} seconds...  ", end='\r')
            time.sleep(60)
        
        print("\n\nDone!")
        browser.close()

if __name__ == "__main__":
    send_to_fahad()

#!/usr/bin/env python3
"""
Simple WhatsApp Sender - Send to Fahad with browser staying open
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

def send_message():
    session_path = Path.home() / '.whatsapp_session'
    
    message = "Hi Fahad! Personal AI Employees are the future of productivity. They work 24/7, monitor all communications, reduce costs by 85-90%, and never miss important messages. Would love to discuss how this could transform your workflow!"
    
    print("\n=== SENDING TO FAHAD ===\n")
    
    with sync_playwright() as p:
        print("Launching Chrome...")
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )
        print("Chrome launched!\n")
        
        page = browser.new_page()
        print("Going to WhatsApp Web...")
        page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=60000)
        print("WhatsApp loaded!\n")
        
        # Check login
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
            print("Logged in!\n")
        except:
            print("NOT LOGGED IN - Please scan QR code\n")
            print("Waiting 60 seconds for login...")
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
                print("Logged in!\n")
            except:
                print("Login timeout - browser stays open for manual login\n")
        
        # Search for Fahad
        print("Searching for 'Fahad'...")
        try:
            search = page.locator('[data-testid="chat-list-search"]')
            search.click()
            time.sleep(1)
            search.fill('Fahad')
            time.sleep(3)
            print("Search done\n")
        except Exception as e:
            print(f"Search error: {e}\n")
        
        # Click on Fahad chat
        print("Opening Fahad chat...")
        try:
            chat = page.locator('span:has-text("Fahad")').first
            chat.click()
            print("Chat opened!\n")
            time.sleep(5)
        except Exception as e:
            print(f"Could not open chat: {e}\n")
            print(">>> PLEASE CLICK ON FAHAD'S CHAT MANUALLY <<<\n")
            time.sleep(10)
        
        # Send message
        print("Sending message...")
        try:
            msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
            msg_box.wait_for(state='visible', timeout=20000)
            
            msg_box.fill(message)
            print("Message typed\n")
            time.sleep(2)
            
            page.keyboard.press('Enter')
            print("MESSAGE SENT!\n")
            time.sleep(3)
            
        except Exception as e:
            print(f"Send error: {e}\n")
            print(">>> PLEASE SEND MANUALLY <<<\n")
            print("Message to send:")
            print(message)
            print()
        
        print("="*60)
        print("Browser stays open for 15 MINUTES")
        print("="*60)
        print("\nCheck if message was sent to Fahad!\n")
        
        # 15 minutes
        for i in range(900, 0, -60):
            print(f"  Closing in {i} seconds...  ", end='\r')
            time.sleep(60)
        
        print("\n\nDone!")
        browser.close()

if __name__ == "__main__":
    send_message()

#!/usr/bin/env python3
"""Quick weather message to Fahad"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

def send_weather_message():
    session_path = Path.home() / '.whatsapp_session'
    
    message = """Hi Fahad! ☀️

Just wanted to share a quick weather update - hope you're having a great day!

Best regards"""

    print("Launching Chrome...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )
        
        page = browser.new_page()
        page.goto('https://web.whatsapp.com')
        
        print("WhatsApp Web loaded. Please wait for login...")
        time.sleep(5)
        
        # Wait for chat list
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
            print("Logged in!")
        except:
            print("Please scan QR code if needed...")
            page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
        
        # Search for Fahad
        print("Searching for Fahad...")
        try:
            search_box = page.locator('[data-testid="chat-list-search"]')
            search_box.click()
            search_box.fill('fahad')
            time.sleep(2)
            
            # Click on Fahad
            chat = page.locator('span:has-text("fahad"), span:has-text("Fahad")').first
            chat.click()
            time.sleep(3)
            
            # Type and send message
            msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
            msg_box.fill(message)
            page.keyboard.press('Enter')
            
            print("✅ Message sent to Fahad!")
            
        except Exception as e:
            print(f"Auto-send failed: {e}")
            print("Please send manually in the browser.")
        
        # Keep browser open for 10 minutes so user can see the message
        print("\nBrowser will stay open for 10 minutes...")
        for i in range(600, 0, -10):
            print(f"Closing in {i} seconds...  ", end='\r')
            time.sleep(10)
        
        browser.close()
        print("Done!")

if __name__ == "__main__":
    send_weather_message()

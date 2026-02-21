#!/usr/bin/env python3
"""Quick send to Fahad - assumes already logged in"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

session_path = Path.home() / '.whatsapp_session'

message = "Hi Fahad! Hope you're having a wonderful day! Just checking in. Best regards!"

print("Opening WhatsApp...")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1280, 'height': 720}
    )
    
    page = browser.new_page()
    page.goto('https://web.whatsapp.com')
    
    print("Waiting 5 seconds for page load...")
    time.sleep(5)
    
    # Click search
    print("Searching for Fahad...")
    try:
        search = page.locator('[data-testid="chat-list-search"]').first
        search.click()
        search.fill('Fahad')
        time.sleep(2)
        
        # Click Fahad chat
        print("Opening chat...")
        page.locator('span:has-text("Fahad"), span:has-text("fahad")').first.click()
        time.sleep(3)
        
        # Send message
        print("Sending message...")
        msg = page.locator('[data-testid="conversation-compose-box-input"]')
        msg.fill(message)
        page.keyboard.press('Enter')
        
        print("SUCCESS! Message sent to Fahad!")
        print(f"Message: {message}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Browser will stay open - try manually")
    
    print("\nBrowser open for 10 minutes...")
    for i in range(600, 0, -10):
        print(f"{i}s ", end='\r')
        time.sleep(10)
    
    browser.close()

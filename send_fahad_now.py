#!/usr/bin/env python3
"""Send WhatsApp to Fahad - Fixed version"""
from pathlib import Path
import time
import subprocess
from playwright.sync_api import sync_playwright

# Kill any existing Chrome processes
try:
    subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], capture_output=True, timeout=5)
    time.sleep(1)
except:
    pass

session_path = Path.home() / '.whatsapp_session'
message = "Hi Fahad! Hope you are having a great day! Just checking in."

print("=" * 60)
print("SENDING WHATSAPP TO FAHAD")
print("=" * 60)

with sync_playwright() as p:
    print("\n[1] Launching Chrome...")
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1280, 'height': 720},
        args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
    )
    
    page = browser.new_page()
    
    print("[2] Opening WhatsApp Web...")
    page.goto('https://web.whatsapp.com')
    
    print("[3] Waiting for login...")
    for i in range(45):
        time.sleep(2)
        try:
            if page.is_visible('[data-testid="chat-list"]'):
                print("    Logged in!")
                break
        except:
            pass
        if i % 10 == 0:
            print(f"    Waiting... {i*2}s")
    
    print("[4] Searching for Fahad...")
    time.sleep(2)
    
    try:
        search = page.locator('[data-testid="chat-list-search"]').first
        search.click()
        search.fill('Fahad')
        time.sleep(3)
        
        print("[5] Opening Fahad chat...")
        page.locator('span:has-text("Fahad"), span:has-text("fahad")').first.click()
        time.sleep(3)
        
        print("[6] Sending message...")
        msg = page.locator('[data-testid="conversation-compose-box-input"]')
        msg.fill(message)
        page.keyboard.press('Enter')
        time.sleep(2)
        
        print("\n" + "=" * 60)
        print("SUCCESS! MESSAGE SENT TO FAHAD")
        print("=" * 60)
        print(f"Message: {message}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Browser open - you can verify manually")
    
    print("\nBrowser open 10 minutes...")
    for i in range(600, 0, -10):
        print(f"{i}s  ", end='\r')
        time.sleep(10)
    
    browser.close()
    print("\nDone!")

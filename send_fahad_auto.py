#!/usr/bin/env python3
"""FULLY AUTOMATED - Send WhatsApp to Fahad"""
import sys
from pathlib import Path
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installing playwright...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright

session_path = Path.home() / '.whatsapp_session'
message = "Hi Fahad! Hope you are having a great day! Just checking in."

print("=" * 60)
print("SENDING WHATSAPP TO FAHAD AUTOMATICALLY")
print("=" * 60)

with sync_playwright() as p:
    print("\n[1] Launching Chrome...")
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1280, 'height': 720},
        timeout=60000
    )
    
    page = browser.new_page()
    
    print("[2] Going to WhatsApp Web...")
    page.goto('https://web.whatsapp.com')
    
    print("[3] Waiting for login (checking every 2 seconds)...")
    logged_in = False
    for i in range(60):  # Wait up to 2 minutes
        time.sleep(2)
        try:
            if page.is_visible('[data-testid="chat-list"]'):
                print("    LOGGED IN!")
                logged_in = True
                break
        except:
            pass
        if i % 5 == 0:
            print(f"    Waiting... {i*2}s")
    
    if not logged_in:
        print("ERROR: Not logged in. Please scan QR code manually.")
        print("Browser will stay open for you to login.")
    else:
        print("[4] Searching for Fahad...")
        time.sleep(2)
        
        try:
            # Click and search
            search_box = page.locator('[data-testid="chat-list-search"]')
            search_box.click()
            search_box.fill('Fahad')
            time.sleep(3)
            
            print("[5] Clicking on Fahad chat...")
            # Try different ways to find Fahad
            found = False
            for selector in ['span:has-text("Fahad")', 'span:has-text("fahad")', '[title*="Fahad" i]', '[title*="fahad" i]']:
                try:
                    chat = page.locator(selector).first
                    if chat.is_visible():
                        chat.click()
                        print("    Chat opened!")
                        found = True
                        time.sleep(3)
                        break
                except:
                    continue
            
            if found:
                print("[6] Sending message...")
                msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
                msg_box.fill(message)
                time.sleep(1)
                page.keyboard.press('Enter')
                time.sleep(2)
                
                print("\n" + "=" * 60)
                print("SUCCESS! MESSAGE SENT TO FAHAD")
                print("=" * 60)
                print(f"Message: {message}")
            else:
                print("Could not find Fahad. Please click manually.")
        
        except Exception as e:
            print(f"Error: {e}")
            print("Please send manually in the browser.")
    
    print("\nBrowser open for 10 minutes for verification...")
    for i in range(600, 0, -10):
        print(f"Closing in {i}s  ", end='\r')
        time.sleep(10)
    
    browser.close()
    print("\nDone!")

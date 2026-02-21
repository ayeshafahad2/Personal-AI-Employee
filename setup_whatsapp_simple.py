#!/usr/bin/env python3
"""
Setup WhatsApp Session - Login once, then reuse
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

def setup_session():
    session_path = Path.home() / '.whatsapp_session'
    session_path.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("WHATSAPP SESSION SETUP")
    print("="*70)
    print("\nInstructions:")
    print("1. Browser will open WhatsApp Web")
    print("2. Scan QR code with your phone (WhatsApp > Linked Devices)")
    print("3. Wait for chat list to appear")
    print("4. Session will be saved for future use")
    print("\nOpening browser in 3 seconds...")
    time.sleep(3)
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )
        
        page = browser.new_page()
        page.goto('https://web.whatsapp.com')
        
        print("\nWaiting for login (up to 3 minutes)...")
        print("Please scan QR code when it appears!")
        
        # Wait for chat list (login success)
        max_wait = 180  # 3 minutes
        for i in range(max_wait):
            try:
                if page.is_visible('[data-testid="chat-list"]'):
                    print("\n[OK] Login successful!")
                    time.sleep(5)  # Let UI settle
                    break
            except:
                pass
            
            if i % 10 == 0 and i > 0:
                print(f"  Waiting... ({i}/{max_wait}s)")
            time.sleep(1)
        
        # Verify login
        if page.is_visible('[data-testid="chat-list"]'):
            print("\n[SUCCESS] WhatsApp session saved!")
            print(f"Session location: {session_path}")
        else:
            print("\n[WARN] Login not completed, but keeping browser open")
        
        print("\nBrowser will stay open for 30 more seconds...")
        time.sleep(30)
        
        browser.close()
        print("\nDone!")

if __name__ == "__main__":
    setup_session()

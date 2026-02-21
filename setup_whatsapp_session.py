#!/usr/bin/env python3
"""
Setup WhatsApp Session - Interactive login helper
This script opens WhatsApp Web and waits for you to log in via QR code scan.
Once logged in, the session is saved for future WhatsApp watcher runs.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

def setup_whatsapp_session():
    print("=" * 60)
    print("WhatsApp Session Setup")
    print("=" * 60)
    print()
    
    # Session path - where login state will be saved
    session_path = Path.home() / '.whatsapp_session'
    session_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Session will be saved to: {session_path}")
    print()
    print("INSTRUCTIONS:")
    print("1. A browser window will open with WhatsApp Web")
    print("2. If you see a QR code, scan it with your phone:")
    print("   - Open WhatsApp on your phone")
    print("   - Go to Settings > Linked Devices")
    print("   - Tap 'Link a Device' and scan the QR code")
    print("3. Wait for the chat list to appear (login successful)")
    print("4. The browser will close automatically after 10 minutes")
    print()
    
    print("\nOpening WhatsApp Web in 3 seconds...")
    time.sleep(3)
    
    try:
        with sync_playwright() as p:
            # Use Google Chrome
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                channel='chrome',
                headless=False,
                viewport={'width': 1280, 'height': 800},
                args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
            )
            print("[OK] Launched Google Chrome")
            
            page = browser.new_page()
            
            print("\nNavigating to WhatsApp Web...")
            page.goto('https://web.whatsapp.com', wait_until='networkidle')
            
            print("\nWaiting for login...")
            print("Please scan the QR code when it appears...")
            
            # Wait longer for QR code to appear
            print("Waiting for QR code (up to 60 seconds)...")
            qr_detected = False
            try:
                page.wait_for_selector('[data-testid="qr-tab"]', timeout=60000)
                qr_detected = True
                print("[OK] QR code detected - Please scan it now!")
            except:
                print("Checking if already logged in...")
            
            # Wait for chat list (login success indicator) - give more time
            max_wait = 300  # 5 minutes max
            wait_interval = 5
            elapsed = 0
            
            print(f"\nWaiting for login completion (up to {max_wait} seconds)...")
            
            while elapsed < max_wait:
                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=5000)
                    print("\n[SUCCESS] LOGIN SUCCESSFUL!")
                    print("[SUCCESS] WhatsApp Web is now connected!")
                    break
                except:
                    elapsed += wait_interval
                    if qr_detected:
                        print(f"  Waiting for QR scan... ({elapsed}/{max_wait}s)")
                    else:
                        print(f"  Waiting for page to load... ({elapsed}/{max_wait}s)")
            
            # Verify login
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=5000)
                print("\n[OK] Session saved successfully!")
                print(f"[OK] Session location: {session_path}")
                print("\n[READY] WhatsApp is ready! Browser will stay open for 30 more seconds...")
                print("You can now test sending messages or run the watcher.")
            except:
                print("\n[WARNING] Login not completed within timeout.")
                print("The browser will remain open - you can still scan the QR code manually.")
            
            # Keep browser open for 10 minutes for user to verify
            print("\nBrowser will stay open for 10 minutes (600 seconds)...")
            print("Use this time to verify you're logged in and can see your chats.")
            time.sleep(600)
            
            browser.close()
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have a stable internet connection")
        print("2. Try running this script again")
        print("3. Make sure WhatsApp is installed on your phone")
        return False
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python test_whatsapp_connection.py")
    print("2. Or run the full orchestrator: python src/orchestrator/orchestrator.py")
    
    return True

if __name__ == "__main__":
    success = setup_whatsapp_session()
    sys.exit(0 if success else 1)

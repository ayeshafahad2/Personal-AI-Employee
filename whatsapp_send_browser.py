#!/usr/bin/env python3
"""
WhatsApp Sender - Browser Automation (No Twilio Required)
Send WhatsApp messages using your existing WhatsApp Web session

Usage:
    python whatsapp_send_browser.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Your WhatsApp number
YOUR_NUMBER = os.getenv('WHATSAPP_RECIPIENT_NUMBER', 'whatsapp:+923298374240')

print("=" * 70)
print("  WHATSAPP MESSAGE SENDER - BROWSER VERSION")
print("=" * 70)

print(f"\n  Your Number: {YOUR_NUMBER}")
print("\n  This will open WhatsApp Web in browser.")
print("  You can send messages directly.")

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    print("\n  Installing Playwright...")
    os.system('pip install playwright -q')
    os.system('playwright install msedge')
    from playwright.sync_api import sync_playwright

print("\n" + "=" * 70)
print("  COMPOSE MESSAGE")
print("=" * 70)

to_number = input("\n  Recipient number (with country code, e.g., 923298374240): ").strip()
message = input("  Your message: ").strip()

if not to_number or not message:
    print("\n  ERROR: Both number and message required")
    sys.exit(1)

print("\n" + "=" * 70)
print("  SENDING WHATSAPP MESSAGE")
print("=" * 70)

# Format number
if not to_number.startswith('+'):
    to_number = '+' + to_number

# Remove any formatting
to_number = to_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

print(f"\n  To: {to_number}")
print(f"  Message: {message}")

# Open WhatsApp Web
print("\n  Opening WhatsApp Web...")

session_path = Path.home() / '.whatsapp_session'

with sync_playwright() as p:
    try:
        # Launch browser
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1366, 'height': 768},
            timeout=120000
        )
        
        page = browser.new_page()
        
        # Create WhatsApp message URL
        # Remove + from number for URL
        clean_number = to_number.replace('+', '')
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        
        whatsapp_url = f"https://wa.me/{clean_number}?text={encoded_message}"
        
        print(f"\n  Opening: {whatsapp_url}")
        
        page.goto(whatsapp_url)
        page.wait_for_timeout(5000)  # Wait 5 seconds
        
        print("\n" + "=" * 70)
        print("  WHATSAPP OPENED")
        print("=" * 70)
        print("""
  INSTRUCTIONS:
  
  1. If this is your first time:
     - Scan QR code with WhatsApp on your phone
     - WhatsApp Web will connect
  
  2. WhatsApp will open a chat with the number
  3. Your message will be pre-filled
  4. Click "Send" button (paper plane icon)
  5. Done!
  
  Browser will stay open for 2 minutes.
  Close it when done.
""")
        
        # Wait for user to send
        import time
        for i in range(120, 0, -10):
            print(f"  Closing in {i} seconds...  ", end='\r')
            time.sleep(10)
        
        print("\n\n  Closing browser...")
        browser.close()
        
        print("\n" + "=" * 70)
        print("  DONE!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n  ERROR: {e}")
        print("\n  Make sure:")
        print("  1. Chrome is installed")
        print("  2. You have internet connection")
        print("  3. Number is correct with country code")

print("\n")

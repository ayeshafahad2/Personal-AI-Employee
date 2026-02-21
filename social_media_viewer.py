#!/usr/bin/env python3
"""
Social Media Quick Viewer
Just opens LinkedIn and WhatsApp for manual monitoring
No automation - just view your feeds in organized windows
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("  SOCIAL MEDIA QUICK VIEWER")
print("=" * 70)
print("\n  Opens LinkedIn and WhatsApp for manual monitoring")
print("  Browsers stay open for you to review")
print("=" * 70)

with sync_playwright() as p:
    # LinkedIn
    print("\n[1/3] Opening LinkedIn...")
    session_li = Path.home() / '.linkedin_session'
    browser_li = p.chromium.launch_persistent_context(
        str(session_li),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=120000
    )
    page_li = browser_li.new_page()
    page_li.goto('https://www.linkedin.com/feed/')
    print("      Done - LinkedIn open\n")
    
    # WhatsApp
    print("[2/3] Opening WhatsApp...")
    session_wa = Path.home() / '.whatsapp_session'
    browser_wa = p.chromium.launch_persistent_context(
        str(session_wa),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=120000
    )
    page_wa = browser_wa.new_page()
    page_wa.goto('https://web.whatsapp.com')
    print("      Done - WhatsApp open\n")
    
    # Instructions
    print("=" * 70)
    print("  BROWSERS OPENED")
    print("=" * 70)
    print("""
  WINDOW 1: LinkedIn Feed
  - Check notifications tab for latest activity
  - URL: https://www.linkedin.com/notifications/
  
  WINDOW 2: WhatsApp Web
  - Unread messages show with green badges
  - Click chats to view full messages
  
  Both browsers will stay open for 10 minutes.
  Close them manually or wait for auto-close.
""")
    print("=" * 70)
    
    # Keep open
    print("\n  Monitoring active...")
    for i in range(600, 0, -60):
        print(f"  Closing in {i} seconds...  ", end='\r')
        time.sleep(60)
    
    print("\n\n  Closing browsers...")
    browser_li.close()
    browser_wa.close()

print("\n" + "=" * 70)
print("  DONE")
print("=" * 70 + "\n")

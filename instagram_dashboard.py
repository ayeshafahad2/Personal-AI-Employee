#!/usr/bin/env python3
"""
Instagram Dashboard - Quick View
Opens Instagram for monitoring DMs and notifications
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("  INSTAGRAM DASHBOARD")
print("=" * 70)
print("\n  Opens Instagram for monitoring:")
print("  - Direct Messages (DMs)")
print("  - Notifications (likes, comments, follows)")
print("  - Feed activity")
print("\n  Browser stays open for 10 minutes")
print("=" * 70)

with sync_playwright() as p:
    # Launch
    print("\n[1/3] Launching Instagram...")
    session_path = Path.home() / '.instagram_session'
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=120000
    )
    page = browser.new_page()
    print("      Done\n")
    
    # Navigate
    print("[2/3] Opening Instagram...")
    page.goto('https://www.instagram.com/')
    time.sleep(5)
    print("      Done\n")
    
    # Instructions
    print("=" * 70)
    print("  INSTAGRAM OPENED")
    print("=" * 70)
    print("""
  QUICK NAVIGATION:
  
  📬 Direct Messages:
     Click the message icon (top right) or press:
     https://www.instagram.com/direct/inbox/
  
  🔔 Notifications:
     Click the heart icon or press:
     https://www.instagram.com/accounts/activity/
  
  📱 Feed:
     https://www.instagram.com/
  
  Browser will stay open for 10 minutes.
  Check your DMs and notifications manually.
""")
    print("=" * 70)
    
    # Keep open
    print("\n  Monitoring active...")
    for i in range(600, 0, -60):
        print(f"  Closing in {i} seconds...  ", end='\r')
        time.sleep(60)
    
    print("\n\n  Closing browser...")
    browser.close()

print("\n" + "=" * 70)
print("  DONE")
print("=" * 70 + "\n")

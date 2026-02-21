#!/usr/bin/env python3
"""
Twitter/X Dashboard - Quick Viewer
Opens Twitter for monitoring notifications and activity
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("  TWITTER/X DASHBOARD")
print("=" * 70)
print("\n  Opens Twitter for monitoring:")
print("  - Home feed")
print("  - Notifications")
print("  - Mentions")
print("  - Direct Messages")
print("\n  Browser stays open for 10 minutes")
print("=" * 70)

with sync_playwright() as p:
    # Launch
    print("\n[1/3] Launching Twitter...")
    session_path = Path.home() / '.twitter_session'
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
    print("[2/3] Opening Twitter/X...")
    page.goto('https://twitter.com/')
    time.sleep(5)
    print("      Done\n")
    
    # Instructions
    print("=" * 70)
    print("  TWITTER OPENED")
    print("=" * 70)
    print("""
  QUICK NAVIGATION:
  
  📬 Notifications:
     https://twitter.com/notifications
  
  🔔 Mentions:
     https://twitter.com/notifications/mentions
  
  💬 Direct Messages:
     https://twitter.com/messages
  
  📱 Home Feed:
     https://twitter.com/
  
  📊 Your Profile:
     https://twitter.com/your_username
  
  Browser will stay open for 10 minutes.
  Check your notifications and DMs manually.
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

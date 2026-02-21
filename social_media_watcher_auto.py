#!/usr/bin/env python3
"""
Social Media Watcher - Auto Run Mode
Opens both platforms, logs in, and shows unread activity
No interaction required - just watch the browsers
"""

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path
import json

print("=" * 70)
print("  SOCIAL MEDIA ACTIVE WATCHER - AUTO MODE")
print("=" * 70)
print("\n  This will:")
print("  1. Open LinkedIn and WhatsApp in separate browsers")
print("  2. Wait for you to log in to each")
print("  3. Fetch and display unread activity")
print("  4. Keep browsers open for monitoring")
print("\n  Press Ctrl+C to stop")
print("=" * 70)

with sync_playwright() as p:
    # ========== LINKEDIN ==========
    print("\n[1/6] Opening LinkedIn browser...")
    session_li = Path.home() / '.linkedin_session'
    browser_li = p.chromium.launch_persistent_context(
        str(session_li),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=120000
    )
    page_li = browser_li.new_page()
    print("      Done\n")
    
    # ========== WHATSAPP ==========
    print("[2/6] Opening WhatsApp browser...")
    session_wa = Path.home() / '.whatsapp_session'
    browser_wa = p.chromium.launch_persistent_context(
        str(session_wa),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=120000
    )
    page_wa = browser_wa.new_page()
    print("      Done\n")
    
    # ========== NAVIGATE ==========
    print("[3/6] Navigating to platforms...")
    page_li.goto('https://www.linkedin.com/feed/')
    page_wa.goto('https://web.whatsapp.com')
    print("      Done\n")
    
    # ========== LOGIN WAIT ==========
    print("=" * 70)
    print("  LOGIN REQUIRED")
    print("=" * 70)
    print("""
  TWO BROWSER WINDOWS ARE NOW OPEN:
  
  BROWSER 1 (LinkedIn):
  - If not logged in, sign in to your LinkedIn account
  
  BROWSER 2 (WhatsApp):
  - If not logged in, scan QR code:
    1. Open WhatsApp on your PHONE
    2. Settings > Linked Devices
    3. Tap 'Link a Device'
    4. Scan the QR code
  
  Waiting 90 seconds for login...
""")
    print("=" * 70)
    
    for i in range(90, 0, -10):
        print(f"  {i} seconds remaining...")
        time.sleep(10)
    
    # ========== FETCH LINKEDIN ==========
    print("\n[4/6] Fetching LinkedIn notifications...")
    
    li_notifications = []
    try:
        page_li.goto('https://www.linkedin.com/notifications/', wait_until='domcontentloaded')
        time.sleep(5)
        
        elements = page_li.query_selector_all('[data-id], .notification-item')
        for elem in elements[:10]:
            try:
                text = elem.inner_text()[:200]
                if text.strip():
                    is_unread = 'unread' in elem.get_attribute('class', '').lower() if elem.get_attribute('class') else False
                    li_notifications.append({
                        'text': text.strip(),
                        'unread': is_unread
                    })
            except:
                continue
        
        print(f"      Found {len(li_notifications)} notifications")
    except Exception as e:
        print(f"      Error: {e}")
    
    # ========== FETCH WHATSAPP ==========
    print("\n[5/6] Fetching WhatsApp unread messages...")
    
    wa_unread = []
    try:
        time.sleep(3)
        chat_rows = page_wa.query_selector_all('[data-testid="chat-list"] > div > div > div > div:first-child')
        
        if not chat_rows:
            chat_rows = page_wa.query_selector_all('div[role="row"]')
        
        for chat in chat_rows:
            try:
                name_elem = chat.query_selector('span[title], div[aria-label]')
                chat_name = name_elem.get_attribute('title') or name_elem.get_attribute('aria-label') or "Unknown" if name_elem else "Unknown"
                
                badge = chat.query_selector('[data-badge], .akvuzm1l')
                if badge:
                    count = 1
                    try:
                        badge_text = badge.inner_text()
                        count = int(badge_text) if badge_text.isdigit() else 1
                    except:
                        pass
                    
                    if chat_name != "Unknown":
                        wa_unread.append({
                            'name': chat_name.strip()[:50],
                            'count': count
                        })
            except:
                continue
        
        print(f"      Found {len(wa_unread)} chats with unread messages")
    except Exception as e:
        print(f"      Error: {e}")
    
    # ========== DISPLAY DASHBOARD ==========
    print("\n[6/6] Displaying dashboard...\n")
    
    print("\n" + "=" * 70)
    print("  SOCIAL MEDIA DASHBOARD - UNREAD ACTIVITY")
    print("=" * 70)
    print(f"  Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # LinkedIn
    print("\n" + "-" * 70)
    print("  LINKEDIN - LAST 5 NOTIFICATIONS")
    print("-" * 70)
    
    if li_notifications:
        for i, notif in enumerate(li_notifications[:5], 1):
            status = "[NEW]" if notif.get('unread', False) else "[READ]"
            print(f"\n  {i}. {status}")
            print(f"     {notif.get('text', 'No content')[:120]}")
    else:
        print("\n  No notifications found (check browser window)")
    
    # WhatsApp
    print("\n" + "-" * 70)
    print("  WHATSAPP - UNREAD MESSAGES")
    print("-" * 70)
    
    if wa_unread:
        for i, chat in enumerate(wa_unread, 1):
            print(f"\n  {i}. {chat['name']}")
            print(f"     Unread: {chat['count']} message(s)")
    else:
        print("\n  No unread messages found (check browser window)")
    
    print("\n" + "=" * 70)
    print("  BROWSERS REMAIN OPEN FOR MONITORING")
    print("  Check the browser windows for full details")
    print("=" * 70)
    
    # Save report
    report = {
        'timestamp': datetime.now().isoformat(),
        'linkedin_notifications': li_notifications[:5],
        'whatsapp_unread': wa_unread
    }
    
    report_path = Path('social_media_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n  Report saved: {report_path}\n")
    
    # Keep browsers open
    print("=" * 70)
    print("  Waiting 5 minutes (300 seconds)...")
    print("  Browsers will stay open for you to review")
    print("=" * 70)
    
    for i in range(300, 0, -30):
        print(f"  {i}s...  ", end='\r')
        time.sleep(30)
    
    print("\n\n  Closing browsers...")
    browser_li.close()
    browser_wa.close()

print("\n" + "=" * 70)
print("  DONE")
print("=" * 70 + "\n")

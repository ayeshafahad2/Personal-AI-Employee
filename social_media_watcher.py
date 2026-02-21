#!/usr/bin/env python3
"""
Social Media Active Watcher Dashboard
Unified monitoring for LinkedIn and WhatsApp
Shows: Last 5 LinkedIn notifications + All WhatsApp unread messages
"""

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path
import json

class SocialMediaWatcher:
    """Unified watcher for LinkedIn and WhatsApp"""
    
    def __init__(self):
        self.session_path_li = Path.home() / '.linkedin_session'
        self.session_path_wa = Path.home() / '.whatsapp_session'
        self.playwright = None
        self.browser_li = None
        self.browser_wa = None
        self.page_li = None
        self.page_wa = None
        
        self.linkedin_notifications = []
        self.whatsapp_unread = []
        
    def start(self):
        """Start browser sessions"""
        print("\n" + "=" * 70)
        print("SOCIAL MEDIA ACTIVE WATCHER")
        print("=" * 70)
        
        self.playwright = sync_playwright().start()
        
        # Launch LinkedIn browser
        print("\n[1/4] Launching LinkedIn browser...")
        self.browser_li = self.playwright.chromium.launch_persistent_context(
            str(self.session_path_li),
            channel='chrome',
            headless=False,
            viewport={'width': 1366, 'height': 768},
            timeout=120000
        )
        self.page_li = self.browser_li.new_page()
        print("      LinkedIn browser ready\n")
        
        # Launch WhatsApp browser
        print("[2/4] Launching WhatsApp browser...")
        self.browser_wa = self.playwright.chromium.launch_persistent_context(
            str(self.session_path_wa),
            channel='chrome',
            headless=False,
            viewport={'width': 1366, 'height': 768},
            timeout=120000
        )
        self.page_wa = self.browser_wa.new_page()
        print("      WhatsApp browser ready\n")
        
    def stop(self):
        """Stop browser sessions"""
        print("\nClosing browsers...")
        if self.browser_li:
            self.browser_li.close()
        if self.browser_wa:
            self.browser_wa.close()
        if self.playwright:
            self.playwright.stop()
        print("Done.\n")
        
    def login_linkedin(self, timeout=90):
        """Login to LinkedIn"""
        print("[LinkedIn] Opening LinkedIn...")
        self.page_li.goto('https://www.linkedin.com/feed/')
        time.sleep(5)
        
        # Check if logged in
        try:
            if self.page_li.query_selector('.feed-shared-update-v2'):
                print("[LinkedIn] Already logged in!\n")
                return True
        except:
            pass
        
        print("[LinkedIn] Please log in if needed")
        print(f"[LinkedIn] Waiting {timeout} seconds...\n")
        
        for i in range(timeout, 0, -10):
            if i % 30 == 0:
                print(f"[LinkedIn] {i} seconds remaining...")
            time.sleep(10)
            
            try:
                if self.page_li.query_selector('.feed-shared-update-v2'):
                    print("[LinkedIn] Login successful!\n")
                    return True
            except:
                pass
        
        return False
    
    def login_whatsapp(self, timeout=120):
        """Login to WhatsApp"""
        print("[WhatsApp] Opening WhatsApp Web...")
        self.page_wa.goto('https://web.whatsapp.com')
        time.sleep(5)
        
        # Check if logged in
        try:
            if self.page_wa.query_selector('[data-testid="chat-list"]'):
                print("[WhatsApp] Already logged in!\n")
                return True
        except:
            pass
        
        print("=" * 70)
        print("[WhatsApp] SCAN QR CODE:")
        print("1. Open WhatsApp on your PHONE")
        print("2. Settings > Linked Devices")
        print("3. Tap 'Link a Device'")
        print("4. Scan QR code in browser")
        print("=" * 70)
        print(f"\n[WhatsApp] Waiting {timeout} seconds...\n")
        
        for i in range(timeout, 0, -10):
            if i % 30 == 0:
                print(f"[WhatsApp] {i} seconds remaining...")
            time.sleep(10)
            
            try:
                if self.page_wa.query_selector('[data-testid="chat-list"]'):
                    print("[WhatsApp] Login successful!\n")
                    return True
            except:
                pass
        
        return False
    
    def get_linkedin_notifications(self):
        """Fetch last 5 LinkedIn notifications"""
        print("[LinkedIn] Fetching notifications...")
        
        try:
            self.page_li.goto('https://www.linkedin.com/notifications/', wait_until='domcontentloaded')
            time.sleep(5)
            
            notifications = []
            
            # Try to find notification items
            elements = self.page_li.query_selector_all('[data-id], .notification-item, .notifications-list__item')
            
            for elem in elements[:10]:
                try:
                    text = elem.inner_text()[:200]
                    if text.strip():
                        is_unread = False
                        try:
                            if elem.query_selector('.notification-badge') or \
                               'unread' in elem.get_attribute('class', '').lower():
                                is_unread = True
                        except:
                            pass
                        
                        notifications.append({
                            'text': text.strip(),
                            'unread': is_unread,
                            'source': 'LinkedIn'
                        })
                except:
                    continue
            
            self.linkedin_notifications = notifications[:5]
            print(f"[LinkedIn] Found {len(self.linkedin_notifications)} notifications\n")
            
        except Exception as e:
            print(f"[LinkedIn] Error: {e}\n")
            self.linkedin_notifications = []
    
    def get_whatsapp_unread(self):
        """Fetch WhatsApp unread messages"""
        print("[WhatsApp] Scanning unread messages...")
        
        try:
            unread_chats = []
            
            # Get all chat rows
            chat_rows = self.page_wa.query_selector_all('[data-testid="chat-list"] > div > div > div > div:first-child')
            
            if not chat_rows:
                chat_rows = self.page_wa.query_selector_all('div[role="row"]')
            
            for chat in chat_rows:
                try:
                    # Get chat name
                    name_elem = chat.query_selector('span[title], div[aria-label]')
                    chat_name = "Unknown"
                    if name_elem:
                        chat_name = name_elem.get_attribute('title') or name_elem.get_attribute('aria-label') or "Unknown"
                    
                    # Check for unread
                    is_unread = False
                    count = 0
                    
                    badge = chat.query_selector('[data-badge], .akvuzm1l')
                    if badge:
                        is_unread = True
                        try:
                            badge_text = badge.inner_text()
                            count = int(badge_text) if badge_text.isdigit() else 1
                        except:
                            count = 1
                    
                    if is_unread and chat_name != "Unknown":
                        unread_chats.append({
                            'name': chat_name.strip()[:50],
                            'count': count,
                            'source': 'WhatsApp'
                        })
                        
                except:
                    continue
            
            self.whatsapp_unread = unread_chats
            print(f"[WhatsApp] Found {len(unread_chats)} chats with unread messages\n")
            
        except Exception as e:
            print(f"[WhatsApp] Error: {e}\n")
            self.whatsapp_unread = []
    
    def display_dashboard(self):
        """Display unified dashboard"""
        print("\n")
        print("=" * 70)
        print("  SOCIAL MEDIA DASHBOARD - UNREAD ACTIVITY")
        print("=" * 70)
        print(f"  Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # LinkedIn Section
        print("\n" + "-" * 70)
        print("  LINKEDIN - LAST 5 NOTIFICATIONS")
        print("-" * 70)
        
        if self.linkedin_notifications:
            for i, notif in enumerate(self.linkedin_notifications, 1):
                status = "[NEW]" if notif.get('unread', False) else "[READ]"
                print(f"\n  {i}. {status}")
                print(f"     {notif.get('text', 'No content')[:120]}")
        else:
            print("\n  No new LinkedIn notifications")
        
        # WhatsApp Section
        print("\n" + "-" * 70)
        print("  WHATSAPP - UNREAD MESSAGES")
        print("-" * 70)
        
        if self.whatsapp_unread:
            for i, chat in enumerate(self.whatsapp_unread, 1):
                print(f"\n  {i}. {chat['name']}")
                print(f"     Unread: {chat['count']} message(s)")
        else:
            print("\n  No unread WhatsApp messages")
        
        print("\n" + "=" * 70)
        print("  BROWSERS ARE OPEN - Review manually if needed")
        print("=" * 70)
        print("\n")
    
    def save_report(self):
        """Save activity report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'linkedin_notifications': self.linkedin_notifications,
            'whatsapp_unread': self.whatsapp_unread
        }
        
        report_path = Path('social_media_activity.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"[Report] Saved: {report_path}\n")
    
    def watch(self, interval=60):
        """Continuous monitoring mode"""
        print("\n" + "=" * 70)
        print("  ACTIVE WATCHER MODE STARTED")
        print("=" * 70)
        print(f"  Checking every {interval} seconds")
        print("  Press Ctrl+C to stop")
        print("=" * 70)
        
        iteration = 0
        try:
            while True:
                iteration += 1
                print(f"\n--- Check #{iteration} --- {datetime.now().strftime('%H:%M:%S')}")
                
                # Refresh data
                self.get_linkedin_notifications()
                self.get_whatsapp_unread()
                
                # Display
                self.display_dashboard()
                
                # Save report every 5 checks
                if iteration % 5 == 0:
                    self.save_report()
                    
                    # Screenshots
                    try:
                        self.page_li.screenshot(path='linkedin_status.png')
                        print("[LinkedIn] Screenshot: linkedin_status.png")
                    except:
                        pass
                    
                    try:
                        self.page_wa.screenshot(path='whatsapp_status.png')
                        print("[WhatsApp] Screenshot: whatsapp_status.png")
                    except:
                        pass
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nWatcher stopped by user")
        except Exception as e:
            print(f"\nError: {e}")


def main():
    print("\n" + "=" * 70)
    print("  SOCIAL MEDIA ACTIVE WATCHER DASHBOARD")
    print("=" * 70)
    print("\n  Monitors:")
    print("  - LinkedIn: Last 5 notifications")
    print("  - WhatsApp: All unread messages")
    print("\n  Two browser windows will open for each platform.")
    print("=" * 70)
    
    watcher = SocialMediaWatcher()
    
    try:
        # Start browsers
        watcher.start()
        
        # Login to both platforms
        print("\n" + "=" * 70)
        print("  LOGIN PHASE")
        print("=" * 70 + "\n")
        
        li_logged = watcher.login_linkedin(timeout=90)
        wa_logged = watcher.login_whatsapp(timeout=120)
        
        if not li_logged:
            print("\n[Warning] LinkedIn login incomplete\n")
        if not wa_logged:
            print("\n[Warning] WhatsApp login incomplete\n")
        
        # Initial fetch
        print("\n" + "=" * 70)
        print("  FETCHING DATA")
        print("=" * 70 + "\n")
        
        if li_logged:
            watcher.get_linkedin_notifications()
        if wa_logged:
            watcher.get_whatsapp_unread()
        
        # Display
        watcher.display_dashboard()
        
        # Menu
        print("=" * 70)
        print("  OPTIONS")
        print("=" * 70)
        print("  1. Run once (show current activity)")
        print("  2. Continuous watch (check every 30 seconds)")
        print("  3. Save report and exit")
        print("  4. Keep browsers open for manual review (60 seconds)")
        print("=" * 70)
        
        choice = input("\n  Select option (1/2/3/4): ").strip()
        
        if choice == '1':
            watcher.display_dashboard()
        elif choice == '2':
            watcher.watch(interval=30)
        elif choice == '3':
            watcher.save_report()
        elif choice == '4':
            print("\n  Browsers open for manual review...")
            print("  Closing in 60 seconds...\n")
            time.sleep(60)
        else:
            print("  Invalid option")
        
        # Save final report
        watcher.save_report()
        
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        watcher.stop()
    
    print("\n" + "=" * 70)
    print("  DONE")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()

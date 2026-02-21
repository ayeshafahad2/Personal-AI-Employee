#!/usr/bin/env python3
"""
Instagram Active Watcher - Monitor DMs, comments, and activity
Shows unread messages and recent engagement
"""

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path
import json

class InstagramWatcher:
    """Active watcher for Instagram activity"""
    
    def __init__(self):
        self.session_path = Path.home() / '.instagram_session'
        self.browser = None
        self.page = None
        self.dms = []
        self.notifications = []
        
    def start(self):
        """Start browser session"""
        print("[Instagram] Launching browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(
            str(self.session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1366, 'height': 768},
            timeout=120000
        )
        self.page = self.browser.new_page()
        print("[Instagram] Browser launched\n")
        
    def stop(self):
        """Stop browser session"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("[Instagram] Session closed\n")
        
    def login(self, timeout=120):
        """Wait for user to log in"""
        print("[Instagram] Opening Instagram...")
        self.page.goto('https://www.instagram.com/')
        time.sleep(5)
        
        # Check if logged in
        try:
            if self.page.query_selector('svg[aria-label="Home"]'):
                print("[Instagram] Already logged in!\n")
                return True
        except:
            pass
        
        print("[Instagram] Please log in to your account")
        print(f"[Instagram] Waiting {timeout} seconds...\n")
        
        for i in range(timeout, 0, -10):
            if i % 30 == 0:
                print(f"[Instagram] {i} seconds remaining...")
            time.sleep(10)
            
            try:
                if self.page.query_selector('svg[aria-label="Home"]'):
                    print("[Instagram] Login successful!\n")
                    return True
            except:
                pass
        
        return False
    
    def get_dms(self):
        """Get unread direct messages"""
        print("[Instagram] Checking direct messages...")
        
        try:
            # Click on DM icon
            dm_selectors = [
                '[aria-label="Messages"]',
                'svg[aria-label="Direct"]',
                '[href*="/direct/inbox/"]'
            ]
            
            for selector in dm_selectors:
                try:
                    dm_btn = self.page.query_selector(selector)
                    if dm_btn and dm_btn.is_visible():
                        dm_btn.click()
                        time.sleep(3)
                        print(f"      Opened messages")
                        break
                except:
                    continue
            
            time.sleep(3)
            
            # Look for unread indicators
            unread_dms = []
            
            # Get all message threads
            threads = self.page.query_selector_all('[role="row"], [class*="message"]')
            
            for thread in threads[:20]:
                try:
                    text = thread.inner_text()[:150]
                    if text.strip():
                        # Check for unread indicator
                        is_unread = False
                        try:
                            # Look for blue dot or bold text
                            if thread.query_selector('[class*="unread"]') or \
                               thread.query_selector('svg circle[fill]'):
                                is_unread = True
                        except:
                            pass
                        
                        if is_unread or text.strip():
                            unread_dms.append({
                                'preview': text.strip(),
                                'unread': is_unread,
                                'type': 'dm'
                            })
                except:
                    continue
            
            self.dms = unread_dms[:10]
            print(f"[Instagram] Found {len(self.dms)} DM conversations\n")
            
            # Go back to feed
            try:
                self.page.goto('https://www.instagram.com/')
                time.sleep(2)
            except:
                pass
            
            return self.dms
            
        except Exception as e:
            print(f"[Instagram] Error checking DMs: {e}")
            return []
    
    def get_notifications(self):
        """Get recent notifications"""
        print("[Instagram] Fetching notifications...")
        
        try:
            # Navigate to notifications
            self.page.goto('https://www.instagram.com/accounts/activity/')
            time.sleep(5)
            
            notifications = []
            
            # Look for notification items
            notif_elements = self.page.query_selector_all('[class*="notification"]', 'div', 'article')
            
            if not notif_elements:
                # Try generic selectors
                notif_elements = self.page.query_selector_all('div > div > div > div:first-child')
            
            for elem in notif_elements[:15]:
                try:
                    text = elem.inner_text()[:200]
                    if text.strip() and len(text) > 10:
                        # Check if unread
                        is_unread = False
                        try:
                            if 'blue' in elem.get_attribute('style', '').lower() or \
                               'unread' in elem.get_attribute('class', '').lower():
                                is_unread = True
                        except:
                            pass
                        
                        notifications.append({
                            'text': text.strip(),
                            'unread': is_unread,
                            'type': 'notification'
                        })
                except:
                    continue
            
            self.notifications = notifications[:10]
            print(f"[Instagram] Found {len(self.notifications)} notifications\n")
            
            return self.notifications
            
        except Exception as e:
            print(f"[Instagram] Error fetching notifications: {e}")
            return []
    
    def display_dashboard(self):
        """Display formatted activity"""
        print("\n" + "=" * 70)
        print("  INSTAGRAM ACTIVITY DASHBOARD")
        print("=" * 70)
        print(f"  Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # DMs Section
        print("\n" + "-" * 70)
        print("  DIRECT MESSAGES (Last 10)")
        print("-" * 70)
        
        if self.dms:
            for i, dm in enumerate(self.dms, 1):
                status = "[UNREAD]" if dm.get('unread', False) else "[READ]"
                print(f"\n  {i}. {status}")
                print(f"     {dm.get('preview', 'No content')[:100]}")
        else:
            print("\n  No DM conversations found")
        
        # Notifications Section
        print("\n" + "-" * 70)
        print("  NOTIFICATIONS (Last 10)")
        print("-" * 70)
        
        if self.notifications:
            for i, notif in enumerate(self.notifications, 1):
                status = "[NEW]" if notif.get('unread', False) else "[READ]"
                print(f"\n  {i}. {status}")
                print(f"     {notif.get('text', 'No content')[:100]}")
        else:
            print("\n  No notifications found")
        
        print("\n" + "=" * 70)
        print("  Check browser window for full details")
        print("=" * 70)
        print("\n")
    
    def watch(self, interval=60, max_iterations=None):
        """Continuous watching mode"""
        print("\n" + "=" * 70)
        print("  INSTAGRAM ACTIVE WATCHER STARTED")
        print("=" * 70)
        print(f"  Checking every {interval} seconds")
        print("  Press Ctrl+C to stop")
        print("=" * 70)
        
        iteration = 0
        try:
            while True:
                iteration += 1
                print(f"\n--- Check #{iteration} --- {datetime.now().strftime('%H:%M:%S')}")
                
                # Fetch data
                self.get_dms()
                self.get_notifications()
                
                # Display
                self.display_dashboard()
                
                # Save report every 5 checks
                if iteration % 5 == 0:
                    self.save_report()
                    
                    # Screenshot
                    try:
                        self.page.screenshot(path='instagram_activity.png')
                        print("[Instagram] Screenshot: instagram_activity.png")
                    except:
                        pass
                
                if max_iterations and iteration >= max_iterations:
                    break
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n  Watcher stopped by user")
        except Exception as e:
            print(f"\n  Error: {e}")
    
    def save_report(self):
        """Save activity report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'dms': self.dms,
            'notifications': self.notifications
        }
        
        report_path = Path('instagram_activity.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"[Instagram] Report saved: {report_path}")


def main():
    print("\n" + "=" * 70)
    print("  INSTAGRAM ACTIVE WATCHER")
    print("=" * 70)
    print("\n  Monitors:")
    print("  - Direct Messages (DMs)")
    print("  - Notifications (likes, comments, follows)")
    print("\n  Browser will open for monitoring")
    print("=" * 70)
    
    watcher = InstagramWatcher()
    
    try:
        # Start
        watcher.start()
        
        # Login
        if not watcher.login(timeout=120):
            print("\n[Instagram] Login failed or timed out")
            watcher.stop()
            return
        
        # Initial fetch
        print("\n[Instagram] Fetching activity...")
        watcher.get_dms()
        watcher.get_notifications()
        
        # Display
        watcher.display_dashboard()
        
        # Menu
        print("=" * 70)
        print("  OPTIONS")
        print("=" * 70)
        print("  1. Run once (show current activity)")
        print("  2. Continuous watch (check every 30 seconds)")
        print("  3. Keep browser open for manual review (60 seconds)")
        print("=" * 70)
        
        choice = input("\n  Select option (1/2/3): ").strip()
        
        if choice == '1':
            watcher.display_dashboard()
        elif choice == '2':
            watcher.watch(interval=30)
        elif choice == '3':
            print("\n  Browser open for manual review...")
            print("  Closing in 60 seconds...\n")
            time.sleep(60)
        else:
            print("  Invalid option")
        
        # Save final report
        watcher.save_report()
        
    except Exception as e:
        print(f"\n[Instagram] Error: {e}")
    finally:
        watcher.stop()
    
    print("\n" + "=" * 70)
    print("  DONE")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()

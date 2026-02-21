#!/usr/bin/env python3
"""
LinkedIn Active Watcher - Monitor notifications and posts
Shows last 5 unread notifications in real-time
"""

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path

class LinkedInWatcher:
    """Active watcher for LinkedIn notifications and activity"""
    
    def __init__(self):
        self.session_path = Path.home() / '.linkedin_session'
        self.browser = None
        self.page = None
        self.notifications = []
        
    def start(self):
        """Start browser session"""
        print("[LinkedIn] Launching browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(
            str(self.session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1366, 'height': 768},
            timeout=120000
        )
        self.page = self.browser.new_page()
        print("[LinkedIn] Browser launched\n")
        
    def stop(self):
        """Stop browser session"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("[LinkedIn] Session closed\n")
        
    def login(self, timeout=120):
        """Wait for user to log in"""
        print("[LinkedIn] Opening LinkedIn...")
        self.page.goto('https://www.linkedin.com/feed/')
        
        print("[LinkedIn] Checking login status...")
        time.sleep(5)
        
        # Check if already logged in
        try:
            if self.page.query_selector('.feed-shared-update-v2'):
                print("[LinkedIn] Already logged in!\n")
                return True
        except:
            pass
        
        print("[LinkedIn] Please log in to your account")
        print(f"[LinkedIn] Waiting {timeout} seconds...\n")
        
        # Wait for login
        for i in range(timeout, 0, -10):
            if i % 30 == 0:
                print(f"[LinkedIn] {i} seconds remaining...")
            time.sleep(10)
            
            # Check if logged in
            try:
                if self.page.query_selector('.feed-shared-update-v2'):
                    print("[LinkedIn] Login successful!\n")
                    return True
            except:
                pass
        
        return False
    
    def get_notifications(self):
        """Fetch unread notifications"""
        print("[LinkedIn] Fetching notifications...")
        
        # Navigate to notifications page
        try:
            self.page.goto('https://www.linkedin.com/notifications/', wait_until='domcontentloaded')
            time.sleep(5)
            
            # Find notification items
            notifications = []
            
            # Look for notification containers
            notification_selectors = [
                'div.notification-item',
                'li.notification-item__container',
                '.notifications-list__item',
                '[data-id]'  # LinkedIn notifications have data-id attribute
            ]
            
            for selector in notification_selectors:
                elements = self.page.query_selector_all(selector)
                if elements:
                    print(f"[LinkedIn] Found {len(elements)} notifications using: {selector}")
                    
                    for elem in elements[:10]:  # Get up to 10
                        try:
                            # Extract notification data
                            text = elem.inner_text()[:200] if elem.inner_text() else ""
                            
                            # Check if unread (usually has unread indicator)
                            is_unread = False
                            try:
                                if elem.query_selector('.notification-badge') or \
                                   elem.query_selector('[class*="unread"]') or \
                                   'unread' in elem.get_attribute('class', '').lower():
                                    is_unread = True
                            except:
                                pass
                            
                            # Get timestamp if available
                            timestamp = ""
                            try:
                                time_elem = elem.query_selector('time, [datetime]')
                                if time_elem:
                                    timestamp = time_elem.get_attribute('datetime', '') or time_elem.inner_text()
                            except:
                                pass
                            
                            if text.strip():
                                notifications.append({
                                    'text': text.strip(),
                                    'unread': is_unread,
                                    'timestamp': timestamp,
                                    'type': 'notification'
                                })
                        except Exception as e:
                            continue
                    
                    break
            
            # If no notifications found with selectors, try generic approach
            if not notifications:
                print("[LinkedIn] Trying alternative method...")
                
                # Get all text content from notifications area
                try:
                    content = self.page.content()
                    # Look for notification patterns in HTML
                    if 'notification' in content.lower():
                        notifications.append({
                            'text': 'Notifications page loaded - check browser for details',
                            'unread': True,
                            'timestamp': datetime.now().isoformat(),
                            'type': 'system'
                        })
                except:
                    pass
            
            self.notifications = notifications[:5]  # Keep last 5
            print(f"[LinkedIn] Retrieved {len(self.notifications)} notifications\n")
            
            return self.notifications
            
        except Exception as e:
            print(f"[LinkedIn] Error fetching notifications: {e}")
            return []
    
    def get_feed_activity(self):
        """Get recent feed activity"""
        print("[LinkedIn] Fetching feed activity...")
        
        try:
            self.page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded')
            time.sleep(5)
            
            activities = []
            
            # Look for feed posts
            posts = self.page.query_selector_all('.feed-shared-update-v2')
            
            for post in posts[:5]:
                try:
                    text = post.inner_text()[:300]
                    if text.strip():
                        activities.append({
                            'text': text.strip(),
                            'type': 'feed_post'
                        })
                except:
                    continue
            
            print(f"[LinkedIn] Found {len(activities)} recent posts\n")
            return activities
            
        except Exception as e:
            print(f"[LinkedIn] Error fetching feed: {e}")
            return []
    
    def display_notifications(self):
        """Display formatted notifications"""
        print("\n" + "=" * 70)
        print("LINKEDIN - LAST 5 NOTIFICATIONS")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70 + "\n")
        
        if not self.notifications:
            print("No notifications found.\n")
            return
        
        for i, notif in enumerate(self.notifications, 1):
            status = "[UNREAD]" if notif.get('unread', False) else "[READ]"
            print(f"{i}. {status}")
            print(f"   {notif.get('text', 'No content')[:150]}")
            if notif.get('timestamp'):
                print(f"   Time: {notif.get('timestamp')}")
            print()
        
        print("=" * 70)
    
    def watch(self, interval=60, max_iterations=None):
        """Continuous watching mode"""
        print("\n" + "=" * 70)
        print("LINKEDIN ACTIVE WATCHER STARTED")
        print("=" * 70)
        print(f"Checking every {interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        iteration = 0
        try:
            while True:
                iteration += 1
                print(f"\n[Check {iteration}] {datetime.now().strftime('%H:%M:%S')}")
                
                # Get notifications
                self.get_notifications()
                
                # Display
                self.display_notifications()
                
                # Screenshot every 5 checks
                if iteration % 5 == 0:
                    try:
                        self.page.screenshot(path='linkedin_notifications.png')
                        print("[LinkedIn] Screenshot saved: linkedin_notifications.png")
                    except:
                        pass
                
                if max_iterations and iteration >= max_iterations:
                    break
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n[LinkedIn] Watcher stopped by user")
        except Exception as e:
            print(f"[LinkedIn] Error: {e}")


def main():
    print("=" * 70)
    print("LINKEDIN ACTIVE WATCHER")
    print("=" * 70)
    print("\nThis will monitor your LinkedIn notifications in real-time")
    print("Showing last 5 unread notifications\n")
    
    watcher = LinkedInWatcher()
    
    try:
        # Start
        watcher.start()
        
        # Login
        if not watcher.login(timeout=90):
            print("[LinkedIn] Login failed or timed out")
            watcher.stop()
            return
        
        # Initial fetch
        watcher.get_notifications()
        watcher.display_notifications()
        
        # Ask user for watch mode
        print("\n" + "=" * 70)
        print("OPTIONS:")
        print("=" * 70)
        print("1. Run once (show current notifications)")
        print("2. Continuous watch (check every 30 seconds)")
        print("3. Open notifications in browser for manual review")
        print("=" * 70)
        
        choice = input("\nSelect option (1/2/3): ").strip()
        
        if choice == '1':
            watcher.display_notifications()
        elif choice == '2':
            watcher.watch(interval=30)
        elif choice == '3':
            print("\n[LinkedIn] Notifications page is open in browser")
            print("Review manually. Browser will close in 60 seconds...")
            time.sleep(60)
        else:
            print("Invalid option")
            
    except Exception as e:
        print(f"[LinkedIn] Error: {e}")
    finally:
        watcher.stop()
    
    print("\n[LinkedIn] Done\n")


if __name__ == '__main__':
    main()

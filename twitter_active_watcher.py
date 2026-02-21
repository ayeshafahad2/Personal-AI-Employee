#!/usr/bin/env python3
"""
Twitter/X Active Watcher - Monitor notifications, mentions, DMs
Shows unread activity in real-time
"""

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path
import json

class TwitterWatcher:
    """Active watcher for Twitter/X activity"""
    
    def __init__(self):
        self.session_path = Path.home() / '.twitter_session'
        self.browser = None
        self.page = None
        self.notifications = []
        self.dms = []
        
    def start(self):
        """Start browser session"""
        print("[Twitter] Launching browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(
            str(self.session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1366, 'height': 768},
            timeout=120000
        )
        self.page = self.browser.new_page()
        print("[Twitter] Browser launched\n")
        
    def stop(self):
        """Stop browser session"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("[Twitter] Session closed\n")
        
    def login(self, timeout=120):
        """Wait for user to log in"""
        print("[Twitter] Opening Twitter/X...")
        self.page.goto('https://twitter.com/')
        time.sleep(5)
        
        # Check if logged in
        try:
            if self.page.query_selector('[data-testid="tweetButton"]'):
                print("[Twitter] Already logged in!\n")
                return True
        except:
            pass
        
        print("[Twitter] Please log in to your account")
        print(f"[Twitter] Waiting {timeout} seconds...\n")
        
        for i in range(timeout, 0, -10):
            if i % 30 == 0:
                print(f"[Twitter] {i} seconds remaining...")
            time.sleep(10)
            
            try:
                if self.page.query_selector('[data-testid="tweetButton"]'):
                    print("[Twitter] Login successful!\n")
                    return True
            except:
                pass
        
        return False
    
    def get_notifications(self):
        """Get recent notifications"""
        print("[Twitter] Fetching notifications...")
        
        try:
            # Navigate to notifications
            self.page.goto('https://twitter.com/notifications')
            time.sleep(5)
            
            notifications = []
            
            # Look for notification items
            notif_elements = self.page.query_selector_all('[data-testid="notification"]')
            
            for elem in notif_elements[:15]:
                try:
                    text = elem.inner_text()[:200]
                    if text.strip():
                        # Check if unread
                        is_unread = False
                        try:
                            style = elem.get_attribute('style', '')
                            if 'blue' in style.lower() or 'rgb(29' in style:  # Twitter blue
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
            print(f"[Twitter] Found {len(self.notifications)} notifications\n")
            
            return self.notifications
            
        except Exception as e:
            print(f"[Twitter] Error fetching notifications: {e}")
            return []
    
    def get_mentions(self):
        """Get recent mentions"""
        print("[Twitter] Fetching mentions...")
        
        try:
            self.page.goto('https://twitter.com/notifications/mentions')
            time.sleep(5)
            
            mentions = []
            
            # Look for tweets
            tweets = self.page.query_selector_all('[data-testid="tweet"]')
            
            for tweet in tweets[:10]:
                try:
                    text = tweet.inner_text()[:200]
                    if text.strip():
                        mentions.append({
                            'text': text.strip(),
                            'type': 'mention'
                        })
                except:
                    continue
            
            print(f"[Twitter] Found {len(mentions)} mentions\n")
            return mentions
            
        except Exception as e:
            print(f"[Twitter] Error fetching mentions: {e}")
            return []
    
    def get_dms(self):
        """Get unread DMs"""
        print("[Twitter] Checking DMs...")
        
        try:
            self.page.goto('https://twitter.com/messages')
            time.sleep(5)
            
            dms = []
            
            # Look for conversation items
            conversations = self.page.query_selector_all('[data-testid="Conversation"]')
            
            for conv in conversations[:10]:
                try:
                    text = conv.inner_text()[:150]
                    if text.strip():
                        dms.append({
                            'preview': text.strip(),
                            'type': 'dm'
                        })
                except:
                    continue
            
            self.dms = dms
            print(f"[Twitter] Found {len(dms)} DM conversations\n")
            
            return dms
            
        except Exception as e:
            print(f"[Twitter] Error checking DMs: {e}")
            return []
    
    def display_dashboard(self):
        """Display formatted activity"""
        print("\n" + "=" * 70)
        print("  TWITTER/X ACTIVITY DASHBOARD")
        print("=" * 70)
        print(f"  Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Notifications
        print("\n" + "-" * 70)
        print("  RECENT NOTIFICATIONS")
        print("-" * 70)
        
        if self.notifications:
            for i, notif in enumerate(self.notifications, 1):
                status = "[NEW]" if notif.get('unread', False) else "[READ]"
                print(f"\n  {i}. {status}")
                print(f"     {notif.get('text', 'No content')[:100]}")
        else:
            print("\n  No notifications found")
        
        # DMs
        print("\n" + "-" * 70)
        print("  DIRECT MESSAGES")
        print("-" * 70)
        
        if self.dms:
            for i, dm in enumerate(self.dms, 1):
                print(f"\n  {i}. {dm.get('preview', 'No content')[:100]}")
        else:
            print("\n  No DMs found")
        
        print("\n" + "=" * 70)
        print("  Check browser for full details")
        print("=" * 70)
        print("\n")
    
    def watch(self, interval=60, max_iterations=None):
        """Continuous watching mode"""
        print("\n" + "=" * 70)
        print("  TWITTER ACTIVE WATCHER STARTED")
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
                self.get_notifications()
                self.get_dms()
                
                # Display
                self.display_dashboard()
                
                # Save report every 5 checks
                if iteration % 5 == 0:
                    self.save_report()
                
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
            'notifications': self.notifications,
            'dms': self.dms
        }
        
        report_path = Path('twitter_activity.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"[Twitter] Report saved: {report_path}")


def main():
    print("\n" + "=" * 70)
    print("  TWITTER/X ACTIVE WATCHER")
    print("=" * 70)
    print("\n  Monitors:")
    print("  - Notifications (likes, retweets, follows)")
    print("  - Mentions")
    print("  - Direct Messages")
    print("\n  Browser will open for monitoring")
    print("=" * 70)
    
    watcher = TwitterWatcher()
    
    try:
        watcher.start()
        
        if not watcher.login(timeout=120):
            print("\n[Twitter] Login failed or timed out")
            watcher.stop()
            return
        
        # Initial fetch
        print("\n[Twitter] Fetching activity...")
        watcher.get_notifications()
        watcher.get_dms()
        
        # Display
        watcher.display_dashboard()
        
        # Menu
        print("=" * 70)
        print("  OPTIONS")
        print("=" * 70)
        print("  1. Run once (show current activity)")
        print("  2. Continuous watch (check every 30 seconds)")
        print("  3. Keep browser open (60 seconds)")
        print("=" * 70)
        
        choice = input("\n  Select option (1/2/3): ").strip()
        
        if choice == '1':
            watcher.display_dashboard()
        elif choice == '2':
            watcher.watch(interval=30)
        elif choice == '3':
            print("\n  Browser open for manual review...")
            time.sleep(60)
        else:
            print("  Invalid option")
        
        watcher.save_report()
        
    except Exception as e:
        print(f"\n[Twitter] Error: {e}")
    finally:
        watcher.stop()
    
    print("\n" + "=" * 70)
    print("  DONE")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()

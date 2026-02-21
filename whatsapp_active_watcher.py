#!/usr/bin/env python3
"""
WhatsApp Active Watcher - Monitor unread messages
Shows all unread messages in real-time
"""

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path

class WhatsAppWatcher:
    """Active watcher for WhatsApp unread messages"""
    
    def __init__(self):
        self.session_path = Path.home() / '.whatsapp_session'
        self.browser = None
        self.page = None
        self.unread_messages = []
        
    def start(self):
        """Start browser session"""
        print("[WhatsApp] Launching browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(
            str(self.session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1366, 'height': 768},
            timeout=120000
        )
        self.page = self.browser.new_page()
        print("[WhatsApp] Browser launched\n")
        
    def stop(self):
        """Stop browser session"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("[WhatsApp] Session closed\n")
        
    def login(self, timeout=180):
        """Wait for user to log in via QR scan"""
        print("[WhatsApp] Opening WhatsApp Web...")
        self.page.goto('https://web.whatsapp.com')
        
        print("[WhatsApp] Checking login status...")
        time.sleep(5)
        
        # Check if already logged in
        try:
            if self.page.query_selector('[data-testid="chat-list"]'):
                print("[WhatsApp] Already logged in!\n")
                return True
        except:
            pass
        
        # Need to scan QR code
        print("=" * 70)
        print("WHATSAPP LOGIN REQUIRED:")
        print("=" * 70)
        print("1. Open WhatsApp on your PHONE")
        print("2. Go to: Settings > Linked Devices")
        print("3. Tap 'Link a Device'")
        print("4. Scan the QR code shown in the browser")
        print("=" * 70)
        print(f"\nWaiting {timeout} seconds for login...\n")
        
        # Wait for login
        for i in range(timeout, 0, -10):
            if i % 30 == 0:
                print(f"[WhatsApp] {i} seconds remaining...")
            time.sleep(10)
            
            # Check if logged in
            try:
                if self.page.query_selector('[data-testid="chat-list"]'):
                    print("[WhatsApp] Login successful!\n")
                    time.sleep(3)
                    return True
            except:
                pass
        
        print("[WhatsApp] Login timeout\n")
        return False
    
    def get_unread_chats(self):
        """Get list of chats with unread messages"""
        print("[WhatsApp] Scanning for unread messages...")
        
        try:
            # Look for unread chat indicators
            unread_selectors = [
                '[data-testid="chat-list"] span:has-text("@")',
                '[data-badge]',
                '.akvuzm1l',  # WhatsApp unread badge class
                '[class*="unread"]'
            ]
            
            unread_chats = []
            
            # Get all chat rows
            chat_rows = self.page.query_selector_all('[data-testid="chat-list"] > div > div > div > div:first-child')
            
            if not chat_rows:
                # Alternative selector
                chat_rows = self.page.query_selector_all('div[role="row"]')
            
            print(f"[WhatsApp] Found {len(chat_rows)} total chats")
            
            for chat in chat_rows:
                try:
                    # Get chat name
                    name_elem = chat.query_selector('span[title], div[aria-label]')
                    chat_name = "Unknown"
                    if name_elem:
                        chat_name = name_elem.get_attribute('title') or name_elem.get_attribute('aria-label') or "Unknown"
                    
                    # Check for unread indicator
                    is_unread = False
                    unread_count = 0
                    
                    # Look for unread badge
                    badge = chat.query_selector('[data-badge], .akvuzm1l, [class*="unread"]')
                    if badge:
                        is_unread = True
                        try:
                            badge_text = badge.inner_text()
                            if badge_text.isdigit():
                                unread_count = int(badge_text)
                            else:
                                unread_count = 1
                        except:
                            unread_count = 1
                    
                    # Also check for green dot (unread indicator)
                    if not is_unread:
                        try:
                            if chat.query_selector('[class*="unread-indicator"]'):
                                is_unread = True
                                unread_count = 1
                        except:
                            pass
                    
                    if is_unread and chat_name != "Unknown":
                        unread_chats.append({
                            'name': chat_name.strip()[:50],
                            'count': unread_count,
                            'type': 'chat'
                        })
                        
                except Exception as e:
                    continue
            
            self.unread_chats = unread_chats
            print(f"[WhatsApp] Found {len(unread_chats)} chats with unread messages\n")
            
            return unread_chats
            
        except Exception as e:
            print(f"[WhatsApp] Error scanning chats: {e}")
            return []
    
    def get_unread_messages_from_chat(self, chat_name, max_messages=10):
        """Open a chat and get unread messages"""
        print(f"[WhatsApp] Getting messages from: {chat_name}")
        
        try:
            # Search for the chat
            search_box = self.page.locator('[data-testid="chat-list-search"]')
            search_box.click()
            time.sleep(1)
            search_box.fill(chat_name)
            time.sleep(3)
            
            # Click on the chat
            chat_elem = self.page.locator(f'span[title*="{chat_name}"]').first
            if chat_elem.is_visible():
                chat_elem.click()
                time.sleep(3)
            
            # Get messages
            messages = []
            msg_elements = self.page.query_selector_all('[data-testid="message"]')
            
            for msg in msg_elements[-max_messages:]:
                try:
                    text = msg.inner_text()
                    if text.strip():
                        # Check if unread (no checkmarks or single grey check)
                        is_read = False
                        try:
                            if msg.query_selector('[data-testid="msg-status"]'):
                                is_read = True
                        except:
                            pass
                        
                        messages.append({
                            'text': text.strip()[:200],
                            'read': is_read,
                            'type': 'message'
                        })
                except:
                    continue
            
            print(f"[WhatsApp] Retrieved {len(messages)} messages\n")
            return messages
            
        except Exception as e:
            print(f"[WhatsApp] Error getting messages: {e}")
            return []
    
    def display_unread(self):
        """Display formatted unread messages"""
        print("\n" + "=" * 70)
        print("WHATSAPP - UNREAD MESSAGES")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70 + "\n")
        
        if not hasattr(self, 'unread_chats') or not self.unread_chats:
            print("No unread messages found.\n")
            return
        
        print(f"Chats with unread messages: {len(self.unread_chats)}\n")
        
        for i, chat in enumerate(self.unread_chats, 1):
            print(f"{i}. {chat['name']}")
            print(f"   Unread count: {chat['count']}")
            print()
        
        print("=" * 70)
        print("TIP: Click on a chat in the browser to view full messages")
        print("=" * 70)
    
    def watch(self, interval=30, max_iterations=None):
        """Continuous watching mode"""
        print("\n" + "=" * 70)
        print("WHATSAPP ACTIVE WATCHER STARTED")
        print("=" * 70)
        print(f"Checking every {interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        iteration = 0
        try:
            while True:
                iteration += 1
                print(f"\n[Check {iteration}] {datetime.now().strftime('%H:%M:%S')}")
                
                # Get unread chats
                self.get_unread_chats()
                
                # Display
                self.display_unread()
                
                # Screenshot every 5 checks
                if iteration % 5 == 0:
                    try:
                        self.page.screenshot(path='whatsapp_unread.png')
                        print("[WhatsApp] Screenshot saved: whatsapp_unread.png")
                    except:
                        pass
                
                if max_iterations and iteration >= max_iterations:
                    break
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n[WhatsApp] Watcher stopped by user")
        except Exception as e:
            print(f"[WhatsApp] Error: {e}")


def main():
    print("=" * 70)
    print("WHATSAPP ACTIVE WATCHER")
    print("=" * 70)
    print("\nThis will monitor your WhatsApp unread messages in real-time\n")
    
    watcher = WhatsAppWatcher()
    
    try:
        # Start
        watcher.start()
        
        # Login
        if not watcher.login(timeout=180):
            print("[WhatsApp] Login failed or timed out")
            watcher.stop()
            return
        
        # Initial scan
        watcher.get_unread_chats()
        watcher.display_unread()
        
        # Ask user for watch mode
        print("\n" + "=" * 70)
        print("OPTIONS:")
        print("=" * 70)
        print("1. Run once (show current unread messages)")
        print("2. Continuous watch (check every 30 seconds)")
        print("3. Open WhatsApp Web for manual review")
        print("=" * 70)
        
        choice = input("\nSelect option (1/2/3): ").strip()
        
        if choice == '1':
            watcher.display_unread()
        elif choice == '2':
            watcher.watch(interval=30)
        elif choice == '3':
            print("\n[WhatsApp] WhatsApp Web is open in browser")
            print("Review manually. Browser will close in 60 seconds...")
            time.sleep(60)
        else:
            print("Invalid option")
            
    except Exception as e:
        print(f"[WhatsApp] Error: {e}")
    finally:
        watcher.stop()
    
    print("\n[WhatsApp] Done\n")


if __name__ == '__main__':
    main()

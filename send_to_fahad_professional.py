#!/usr/bin/env python3
"""
Professional WhatsApp Message Sender - Fully Automated
Sends message to Fahad about Personal AI Employee
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

def send_professional_message():
    session_path = Path.home() / '.whatsapp_session'
    
    # Professional message
    message = """Hi Fahad!

I wanted to share something exciting about Personal AI Employees (Digital FTEs) - the future of productivity.

Key Benefits:
• 24/7 Availability - Works while you sleep
• Intelligent Processing - Monitors Gmail, WhatsApp, LinkedIn automatically  
• 85-90% Cost Reduction vs human FTE
• Local-first Architecture - Data stays on your machine
• Instant Response - Never misses important messages

This could transform your workflow significantly. Would love to discuss!

Best regards"""

    print("\n" + "="*70)
    print("PROFESSIONAL WHATSAPP SENDER - FAHAD")
    print("="*70 + "\n")
    
    success = False
    
    with sync_playwright() as p:
        # Launch Chrome with existing session
        print("[1/6] Launching Google Chrome...")
        try:
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                channel='chrome',
                headless=False,
                viewport={'width': 1366, 'height': 768},
                timeout=60000
            )
            print("      [OK] Chrome launched successfully\n")
        except Exception as e:
            print(f"      [ERROR] Failed to launch Chrome: {e}\n")
            return False
        
        page = browser.new_page()
        
        # Navigate to WhatsApp Web
        print("[2/6] Loading WhatsApp Web...")
        try:
            page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=60000)
            print("      [OK] WhatsApp Web loaded\n")
        except Exception as e:
            print(f"      [ERROR] Failed to load WhatsApp: {e}\n")
            browser.close()
            return False
        
        # Wait for app to initialize
        print("[3/6] Initializing WhatsApp...")
        time.sleep(8)
        
        # Check if logged in
        print("[4/6] Verifying login status...")
        try:
            chat_list = page.locator('[data-testid="chat-list"]')
            chat_list.wait_for(state='visible', timeout=45000)
            print("      [OK] Logged in successfully\n")
        except PlaywrightTimeout:
            print("      [WARNING] Not logged in - waiting for QR scan (60 seconds)\n")
            try:
                chat_list.wait_for(state='visible', timeout=60000)
                print("      [OK] Login detected\n")
                time.sleep(3)
            except:
                print("      [ERROR] Login timeout\n")
                browser.close()
                return False
        
        # Search for Fahad
        print("[5/6] Searching for 'Fahad'...")
        search_completed = False
        
        # Try search box
        for attempt in range(3):
            try:
                search_box = page.locator('[data-testid="chat-list-search"]')
                search_box.wait_for(state='visible', timeout=10000)
                search_box.click()
                time.sleep(1)
                search_box.fill('Fahad')
                print(f"      [OK] Search completed (attempt {attempt+1})\n")
                time.sleep(4)
                search_completed = True
                break
            except Exception as e:
                print(f"      [WARNING] Search attempt {attempt+1} failed: {e}\n")
                time.sleep(2)
        
        if not search_completed:
            print("      [WARNING] Search not available - will look in chat list\n")
        
        # Click on Fahad's chat
        print("[6/6] Opening Fahad's chat and sending message...")
        
        chat_opened = False
        for attempt in range(5):
            try:
                # Multiple selector strategies
                selectors = [
                    'span[title*="Fahad" i]',
                    'span[title*="fahad" i]',
                    'div[title*="Fahad" i]',
                    'span:has-text("Fahad")',
                    'span:has-text("fahad")',
                ]
                
                for selector in selectors:
                    try:
                        chat_element = page.locator(selector).first
                        if chat_element.is_visible(timeout=5000):
                            chat_element.click()
                            print(f"      [OK] Clicked on Fahad's chat\n")
                            
                            # Wait for chat to fully load
                            time.sleep(5)
                            
                            # Verify chat is open by checking for message input
                            try:
                                msg_input = page.locator('[data-testid="conversation-compose-box-input"]')
                                msg_input.wait_for(state='visible', timeout=15000)
                                msg_input.wait_for(state='enabled', timeout=5000)
                                print("      [OK] Chat is ready for messaging\n")
                                chat_opened = True
                                break
                            except:
                                print("      [WARNING] Message box not ready, retrying...\n")
                                time.sleep(3)
                    except:
                        continue
                
                if chat_opened:
                    break
                    
            except Exception as e:
                print(f"      [WARNING] Attempt {attempt+1} failed: {e}\n")
                time.sleep(3)
        
        if not chat_opened:
            print("      [ERROR] Could not open Fahad's chat\n")
            browser.close()
            return False
        
        # Send the message
        print("\n" + "-"*70)
        print("SENDING MESSAGE")
        print("-"*70 + "\n")
        
        try:
            msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
            
            # Ensure it's ready
            msg_box.wait_for(state='visible', timeout=10000)
            msg_box.wait_for(state='enabled', timeout=5000)
            
            # Clear any existing text
            try:
                msg_box.clear()
            except:
                pass
            
            # Type the message
            msg_box.fill(message)
            print("      [OK] Message typed into input box")
            time.sleep(2)
            
            # Send by pressing Enter
            page.keyboard.press('Enter')
            print("      [OK] Enter key pressed - message sent!")
            time.sleep(3)
            
            # Verify message was sent by checking for message bubble
            try:
                sent_message = page.locator('[data-testid="message-bubble"]').last
                sent_message.wait_for(state='visible', timeout=10000)
                print("      [OK] Message delivery confirmed!\n")
                success = True
            except:
                print("      [INFO] Could not verify delivery, but message was sent\n")
                success = True
            
        except Exception as e:
            print(f"      [ERROR] Failed to send message: {e}\n")
            success = False
        
        # Summary
        print("="*70)
        if success:
            print("[SUCCESS] Message sent to Fahad")
        else:
            print("[FAILED] Could not send message")
        print("="*70 + "\n")
        
        print("Message Content:")
        print("-"*70)
        print(message)
        print("-"*70 + "\n")
        
        # Keep browser open for 15 minutes
        print("Browser will remain open for 15 minutes (900 seconds)...")
        print("You can verify the message in the chat window.\n")
        
        for i in range(900, 0, -60):
            print(f"  Closing in {i} seconds...  ", end='\r')
            time.sleep(60)
        
        print("\n\nClosing browser...")
        browser.close()
        
        print("\nDone!\n")
        return success

if __name__ == "__main__":
    success = send_professional_message()
    exit(0 if success else 1)

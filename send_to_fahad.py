#!/usr/bin/env python3
"""
Send WhatsApp message to Fahad about Personal AI Employee importance
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

def send_to_fahad():
    session_path = Path.home() / '.whatsapp_session'
    
    # Professional message about Personal AI Employee
    message = """Hi Fahad!

I wanted to share something exciting about the future of productivity - Personal AI Employees (Digital FTEs).

Why Personal AI Employees Matter:

🤖 24/7 AVAILABILITY
- Works around the clock without breaks
- Handles communications while you sleep
- Never misses important messages

📊 INTELLIGENT PROCESSING
- Monitors Gmail, WhatsApp, LinkedIn automatically
- Identifies urgent/important communications
- Creates action plans and tracks completion

💼 BUSINESS VALUE
- 85-90% cost reduction vs human FTE
- Instant response to routine queries
- Consistent performance without fatigue

🔒 SECURITY & CONTROL
- Local-first architecture (data stays on your machine)
- Human-in-the-loop for critical actions
- Complete audit trail of all activities

📈 SCALABILITY
- Duplicate instantly without proportional cost
- Learn and adapt to your preferences
- Generate executive briefings automatically

The future is here - having a Personal AI Employee is like having a dedicated assistant who never sleeps, never takes a day off, and continuously learns to serve you better.

Would love to discuss how this could transform your workflow!

Best regards"""

    print("\n" + "="*70)
    print("SENDING MESSAGE TO FAHAD")
    print("="*70 + "\n")
    
    with sync_playwright() as p:
        # Launch Chrome
        print("[1/5] Launching Chrome...")
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 720},
            timeout=60000
        )
        print("      Done!\n")
        
        page = browser.new_page()
        page.goto('https://web.whatsapp.com')
        
        print("[2/5] Loading WhatsApp Web...")
        time.sleep(5)
        
        # Check if logged in
        print("[3/5] Checking login status...")
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
            print("      Logged in! ✓\n")
        except:
            print("      Need to login - scanning QR code required\n")
            print("      Please scan QR code if it appears...\n")
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
                print("      Login successful! ✓\n")
            except:
                print("      Login timeout\n")
                browser.close()
                return False
        
        print("[4/5] Finding Fahad's chat...")
        
        # Search for Fahad
        try:
            search_box = page.locator('[data-testid="chat-list-search"]')
            search_box.click()
            time.sleep(1)
            search_box.fill('fahad')
            print("      Searched for 'fahad'\n")
            time.sleep(3)
        except:
            print("      Search not available\n")
        
        # Click on Fahad
        chat_opened = False
        for attempt in range(3):
            try:
                selectors = [
                    'span:has-text("fahad")',
                    'span:has-text("Fahad")',
                    'div[title*="fahad" i]',
                    'span[title*="fahad" i]',
                ]
                
                for selector in selectors:
                    try:
                        chat = page.locator(selector).first
                        if chat.is_visible():
                            chat.click()
                            print(f"      Opened Fahad's chat (attempt {attempt+1})\n")
                            time.sleep(5)
                            
                            # Check if message box is visible
                            try:
                                msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
                                msg_box.wait_for(state='visible', timeout=10000)
                                print("      Chat ready! ✓\n")
                                chat_opened = True
                                break
                            except:
                                print("      Message box not ready, retrying...\n")
                    except:
                        continue
                
                if chat_opened:
                    break
                    
            except Exception as e:
                print(f"      Attempt {attempt+1} error: {e}\n")
                time.sleep(3)
        
        if not chat_opened:
            print("      Could not open Fahad's chat automatically\n")
            print("      >>> PLEASE MANUALLY CLICK ON FAHAD'S CHAT <<<\n")
            time.sleep(15)
        
        print("[5/5] Sending message about Personal AI Employee...\n")
        
        try:
            msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
            msg_box.wait_for(state='visible', timeout=15000)
            
            # Clear and type
            msg_box.clear()
            msg_box.fill(message)
            print("      Message typed ✓\n")
            time.sleep(2)
            
            # Send
            page.keyboard.press('Enter')
            print("      Message sent to Fahad! ✓\n")
            time.sleep(3)
            
            print("="*70)
            print("SUCCESS! Message sent to Fahad")
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"      Could not send automatically: {e}\n")
            print("      >>> PLEASE SEND THE MESSAGE MANUALLY <<<\n")
        
        # Show message preview
        print("Message sent:")
        print("-"*70)
        print(message)
        print("-"*70 + "\n")
        
        # Keep browser open for 15 minutes
        print("Browser will stay open for 15 minutes (900 seconds)...")
        print("You can verify the message or send more messages.\n")
        for i in range(900, 0, -60):
            print(f"  Closing in {i} seconds...  ", end='\r')
            time.sleep(60)
        
        print("\n\nClosing browser...")
        browser.close()
        
        print("Done!\n")
        return True

if __name__ == "__main__":
    send_to_fahad()

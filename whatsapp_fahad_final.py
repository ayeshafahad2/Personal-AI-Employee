#!/usr/bin/env python3
"""
WhatsApp Send to Fahad - With fresh login if needed
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

def send_to_fahad():
    session_path = Path.home() / '.whatsapp_session'
    
    message = """Hi Fahad!

I wanted to share something exciting about Personal AI Employees (Digital FTEs) - the future of productivity.

Key Benefits:
- 24/7 Availability - Works while you sleep
- Intelligent Processing - Monitors Gmail, WhatsApp, LinkedIn automatically
- 85-90% Cost Reduction vs human FTE
- Local-first Architecture - Data stays on your machine
- Instant Response - Never misses important messages

This could transform your workflow significantly. Would love to discuss!

Best regards"""

    print("\n" + "="*70)
    print("WHATSAPP MESSAGE TO FAHAD - PERSONAL AI EMPLOYEE")
    print("="*70 + "\n")
    
    with sync_playwright() as p:
        print("[1/7] Launching Chrome...")
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 720},
            timeout=60000
        )
        print("      Chrome launched\n")
        
        page = browser.new_page()
        
        print("[2/7] Opening WhatsApp Web...")
        page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=60000)
        print("      WhatsApp opened\n")
        
        print("[3/7] Checking login status...")
        time.sleep(3)
        
        logged_in = False
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
            print("      Already logged in!\n")
            logged_in = True
        except:
            print("      Need to login\n")
        
        if not logged_in:
            print("="*70)
            print("PLEASE SCAN QR CODE:")
            print("1. Open WhatsApp on your phone")
            print("2. Settings > Linked Devices")
            print("3. Tap 'Link a Device'")
            print("4. Scan the QR code on screen")
            print("="*70 + "\n")
            
            print("Waiting for login (2 minutes)...")
            try:
                page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
                print("      Login successful!\n")
                time.sleep(5)
            except:
                print("      Login timeout\n")
                browser.close()
                return False
        
        print("[4/7] Searching for Fahad...")
        try:
            search_box = page.locator('[data-testid="chat-list-search"]')
            search_box.click()
            time.sleep(1)
            search_box.fill('Fahad')
            print("      Searching...\n")
            time.sleep(4)
        except Exception as e:
            print(f"      Search error: {e}\n")
        
        print("[5/7] Opening Fahad's chat...")
        chat_found = False
        for i in range(5):
            try:
                # Try different selectors
                for selector in ['span:has-text("Fahad")', 'span[title*="Fahad"]', 'div[title*="Fahad"]']:
                    try:
                        chat = page.locator(selector).first
                        if chat.is_visible():
                            chat.click()
                            print(f"      Clicked on Fahad (attempt {i+1})\n")
                            time.sleep(6)
                            
                            # Check if message box is ready
                            try:
                                msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
                                msg_box.wait_for(state='visible', timeout=10000)
                                print("      Chat ready!\n")
                                chat_found = True
                                break
                            except:
                                print("      Not ready, retrying...\n")
                    except:
                        pass
                if chat_found:
                    break
            except:
                time.sleep(2)
        
        if not chat_found:
            print("      Could not open chat - please click on Fahad manually\n")
            time.sleep(15)
        
        print("[6/7] Sending message...")
        try:
            msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
            msg_box.wait_for(state='visible', timeout=15000)
            
            msg_box.clear()
            msg_box.fill(message)
            print("      Message typed\n")
            time.sleep(2)
            
            page.keyboard.press('Enter')
            print("      MESSAGE SENT!\n")
            time.sleep(3)
            
            print("[7/7] Verifying delivery...")
            time.sleep(2)
            print("      Done!\n")
            
        except Exception as e:
            print(f"      Send error: {e}\n")
            print("      Please send manually:\n")
            print(message)
            print()
        
        print("="*70)
        print("MESSAGE SENT TO FAHAD")
        print("="*70 + "\n")
        print("Message:")
        print("-"*70)
        print(message)
        print("-"*70 + "\n")
        
        print("Browser stays open for 15 minutes (900 seconds)...")
        print("You can verify the message in the chat.\n")
        
        for i in range(900, 0, -60):
            print(f"  Closing in {i} seconds...  ", end='\r')
            time.sleep(60)
        
        print("\n\nClosing browser...")
        browser.close()
        print("Done!\n")
        
        return True

if __name__ == "__main__":
    send_to_fahad()

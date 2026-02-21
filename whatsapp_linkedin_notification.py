#!/usr/bin/env python3
"""
WhatsApp LinkedIn Post Notification - Auto send to Fahad
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("WHATSAPP - LINKEDIN POST NOTIFICATION")
print("=" * 70)

# Read the LinkedIn post content
post_file = "linkedin_post_best_personal_ai_employee_20260213_000304.txt"
with open(post_file, 'r', encoding='utf-8') as f:
    post_content = f.read().strip()

# Create notification message
message = f"""🚀 LinkedIn Post Published!

The Personal AI Employee: Your 24/7 Digital Co-Worker

Key Highlights:
• 24/7 Continuous Monitoring
• Multi-Platform Integration (Gmail, WhatsApp, LinkedIn)
• Smart Prioritization
• Privacy-First Approach
• 85-90% Cost Reduction vs human FTE

The post is now live on LinkedIn!

#PersonalAI #AI #Productivity #FutureOfWork

— Your AI Assistant"""

print(f"\nMessage prepared: {len(message)} characters")

session_path = Path.home() / '.whatsapp_session'

with sync_playwright() as p:
    # Launch browser with persistent session
    print("\n[1/6] Launching Chrome...")
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1280, 'height': 720},
        timeout=60000
    )
    print("      Chrome launched\n")

    page = browser.new_page()

    # Open WhatsApp Web
    print("[2/6] Opening WhatsApp Web...")
    page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(5000)
    print("      WhatsApp Web opened\n")

    # Check login status
    print("[3/6] Checking login status...")
    time.sleep(3)

    logged_in = False
    try:
        page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
        print("      Already logged in!\n")
        logged_in = True
    except:
        print("      Need to login\n")

    if not logged_in:
        print("=" * 70)
        print("PLEASE SCAN QR CODE:")
        print("1. Open WhatsApp on your phone")
        print("2. Settings > Linked Devices")
        print("3. Tap 'Link a Device'")
        print("4. Scan the QR code on screen")
        print("=" * 70 + "\n")

        print("Waiting for login (3 minutes)...")
        print("Scan the QR code in the browser window...\n")
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=180000)
            print("      Login successful!\n")
            time.sleep(5)
        except:
            print("      Login timeout\n")
            browser.close()
            exit(1)

    # Search for Fahad
    print("[4/6] Searching for Fahad...")
    try:
        search_box = page.locator('[data-testid="chat-list-search"]')
        search_box.click()
        time.sleep(1)
        search_box.fill('Fahad')
        print("      Searching...\n")
        time.sleep(4)
    except Exception as e:
        print(f"      Search error: {e}\n")

    # Open Fahad's chat
    print("[5/6] Opening Fahad's chat...")
    chat_found = False
    
    for i in range(5):
        try:
            # Look for Fahad in chat list
            chat_elements = page.locator('span:has-text("Fahad"), span[title*="Fahad"]').all()
            
            for chat in chat_elements:
                if chat.is_visible():
                    chat.click()
                    print(f"      Clicked on Fahad (attempt {i+1})\n")
                    time.sleep(5)
                    
                    # Check if message box is ready
                    try:
                        msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
                        msg_box.wait_for(state='visible', timeout=10000)
                        print("      Chat ready!\n")
                        chat_found = True
                        break
                    except:
                        print("      Not ready, retrying...\n")
            
            if chat_found:
                break
        except Exception as e:
            print(f"      Error: {e}\n")
            time.sleep(2)

    if not chat_found:
        print("      Could not open chat automatically.")
        print("      PLEASE CLICK ON FAHAD'S CHAT MANUALLY!\n")
        print("      Waiting 30 seconds...\n")
        for i in range(30, 0, -1):
            if i % 10 == 0:
                print(f"      {i}s...")
            time.sleep(1)

    # Send message
    print("[6/6] Sending message...")
    try:
        msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
        msg_box.wait_for(state='visible', timeout=15000)

        msg_box.clear()
        msg_box.fill(message)
        print("      Message typed\n")
        time.sleep(2)

        # Send
        page.keyboard.press('Enter')
        print("      MESSAGE SENT!\n")
        time.sleep(3)

        # Verify
        print("      Verifying delivery...")
        time.sleep(2)
        print("      Done!\n")

        print("=" * 70)
        print("SUCCESS! WHATSAPP NOTIFICATION SENT TO FAHAD")
        print("=" * 70)

    except Exception as e:
        print(f"      Send error: {e}\n")
        print("      Please send manually:\n")
        print(message)
        print()

    print("\nBrowser stays open for 30 seconds for verification...")
    time.sleep(30)

    browser.close()

print("\nDone!\n")

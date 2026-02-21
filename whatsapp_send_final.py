#!/usr/bin/env python3
"""
WhatsApp Send - Final version with better selectors
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 70)
print("WHATSAPP NOTIFICATION - LinkedIn Post")
print("=" * 70)

# Message to send (without emojis for Windows compatibility)
message = """LinkedIn Post Published!

The Personal AI Employee: Your 24/7 Digital Co-Worker

Key Highlights:
- 24/7 Continuous Monitoring
- Multi-Platform Integration (Gmail, WhatsApp, LinkedIn)
- Smart Prioritization
- Privacy-First Approach
- 85-90% Cost Reduction vs human FTE

The post is now live on LinkedIn!

#PersonalAI #AI #Productivity #FutureOfWork

- Your AI Assistant"""

session_path = Path.home() / '.whatsapp_session'

print("\nLaunching browser...")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1280, 'height': 800},
        timeout=120000
    )

    page = browser.new_page()

    print("Opening WhatsApp Web...")
    page.goto('https://web.whatsapp.com')

    print("\n" + "=" * 70)
    print("LOGIN INSTRUCTIONS:")
    print("=" * 70)
    print("""
1. Open WhatsApp on your PHONE
2. Go to: Settings > Linked Devices  
3. Tap "Link a Device"
4. Scan the QR code shown in the browser

The browser will stay open for 5 minutes for you to log in.
""")
    print("=" * 70)

    # Wait for login
    print("\nWaiting for login (5 minutes max)...")
    logged_in = False
    for i in range(60):
        time.sleep(5)
        try:
            if page.query_selector('[data-testid="chat-list"]'):
                print("Login detected!")
                logged_in = True
                break
        except:
            pass
        if (i + 1) * 5 % 30 == 0:
            print(f"  {(i + 1) * 5} seconds elapsed...")

    if not logged_in:
        print("\nLogin not detected. Continuing anyway...")

    print("\nWaiting 20 seconds for you to be ready...")
    for i in range(20, 0, -1):
        if i % 5 == 0:
            print(f"  {i}s...")
        time.sleep(1)

    # Search for Fahad
    print("\nSearching for Fahad...")
    try:
        search = page.locator('[data-testid="chat-list-search"]')
        if search.is_visible():
            search.click()
            time.sleep(1)
            search.fill('Fahad')
            time.sleep(3)
            print("Searched for Fahad")
    except Exception as e:
        print(f"Search error: {e}")

    # Click on Fahad
    chat_clicked = False
    for selector in ['span:has-text("Fahad")', 'span[title*="Fahad"]', 'div[title*="Fahad"]']:
        try:
            chat = page.locator(selector).first
            if chat.is_visible():
                chat.click()
                print("Clicked on Fahad's chat")
                time.sleep(5)
                chat_clicked = True
                break
        except:
            continue

    if not chat_clicked:
        print("\nCould not find Fahad automatically.")
        print("PLEASE CLICK ON FAHAD'S CHAT MANUALLY!")
        print("Waiting 60 seconds...\n")
        for i in range(60, 0, -1):
            if i % 10 == 0:
                print(f"  {i}s...")
            time.sleep(1)

    # Type and send message
    print("\nTyping message...")
    time.sleep(2)

    try:
        # Try multiple selectors for message box
        msg_box = None
        for selector in [
            'div[contenteditable="true"]',
            '[data-testid="conversation-compose-box-input"]',
            '[data-tab="10"]',
            'footer div[contenteditable="true"]'
        ]:
            try:
                msg_box = page.locator(selector).first
                if msg_box.is_visible(timeout=5000):
                    print(f"Found message box: {selector}")
                    break
                msg_box = None
            except:
                msg_box = None

        if msg_box:
            msg_box.fill(message)
            print("Message typed!")
            time.sleep(2)

            print("Sending...")
            page.keyboard.press('Enter')
            time.sleep(3)
            print("MESSAGE SENT!")

            # Screenshot
            page.screenshot(path='whatsapp_sent.png')
            print("\nScreenshot saved: whatsapp_sent.png")
        else:
            print("Could not find message box.")
            print("PLEASE SEND MANUALLY. Message content below:")
            print("\n" + "-" * 70)
            print(message)
            print("-" * 70)

    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease send manually. Message content:")
        print("\n" + "-" * 70)
        print(message)
        print("-" * 70)

    print("\n" + "=" * 70)
    print("Waiting 30 seconds before closing...")
    print("=" * 70)
    time.sleep(30)

    browser.close()

print("\nDone!\n")

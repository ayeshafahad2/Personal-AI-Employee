#!/usr/bin/env python3
"""
WhatsApp Send - Simple with long wait for QR scan
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("WHATSAPP NOTIFICATION - LinkedIn Post")
print("=" * 70)

# Message to send
message = """🚀 LinkedIn Post Published!

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
After login, the script will help you send the message.
""")
    print("=" * 70)

    # Wait for login - check every 5 seconds
    print("\nWaiting for login...")
    logged_in = False
    for i in range(60):  # 5 minutes max
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

    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("""
1. Click on Fahad's chat in WhatsApp Web
2. The script will type and send the message
3. Message will be sent automatically

Waiting 30 seconds for you to be ready...
""")
    for i in range(30, 0, -1):
        if i % 10 == 0:
            print(f"  {i}s...")
        time.sleep(1)

    # Try to find and click Fahad's chat
    print("\nLooking for Fahad's chat...")
    try:
        # Search for Fahad
        search = page.locator('[data-testid="chat-list-search"]')
        if search.is_visible():
            search.click()
            time.sleep(1)
            search.fill('Fahad')
            time.sleep(3)
            print("Searched for Fahad")
    except:
        print("Search not available, looking in chat list...")

    # Click on Fahad
    chat_clicked = False
    for selector in ['span:has-text("Fahad")', 'span[title*="Fahad"]']:
        try:
            chat = page.locator(selector).first
            if chat.is_visible():
                chat.click()
                print("Clicked on Fahad's chat")
                time.sleep(3)
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
        msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
        msg_box.wait_for(state='visible', timeout=15000)
        msg_box.fill(message)
        print("Message typed!")
        time.sleep(2)

        print("Sending...")
        page.keyboard.press('Enter')
        time.sleep(2)
        print("MESSAGE SENT!")

        # Screenshot
        page.screenshot(path='whatsapp_sent.png')
        print("\nScreenshot saved: whatsapp_sent.png")

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

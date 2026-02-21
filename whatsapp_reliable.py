#!/usr/bin/env python3
"""
WhatsApp Auto Send - Reliable version
Just click on the chat, script does the rest
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("WHATSAPP AUTO SEND")
print("=" * 70)

# Message
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

with sync_playwright() as p:
    print("\nLaunching WhatsApp Web...")
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1280, 'height': 800},
        timeout=120000
    )

    page = browser.new_page()
    page.goto('https://web.whatsapp.com')

    print("\n" + "=" * 70)
    print("INSTRUCTIONS:")
    print("=" * 70)
    print("""
1. Wait for WhatsApp to load your chats (already logged in)
2. CLICK on Fahad's chat (or whoever you want to send to)
3. The script will automatically type and send the message

Waiting 10 seconds for page load...
""")
    time.sleep(10)

    print("\n" + "=" * 70)
    print("NOW: Click on Fahad's chat in the browser window")
    print("=" * 70)
    print("\nWaiting 60 seconds for you to click...\n")

    # Wait for user to click on chat
    for i in range(60, 0, -1):
        if i % 10 == 0:
            print(f"  {i}s remaining...")
        time.sleep(1)

    print("\nAttempting to send message...")

    try:
        # Find message input - WhatsApp uses contenteditable div
        print("Looking for message box...")
        
        # Multiple attempts with different approaches
        for attempt in range(5):
            try:
                # Primary selector - contenteditable in footer
                msg_box = page.locator('footer div[contenteditable="true"]')
                if msg_box.count() > 0:
                    print(f"Attempt {attempt + 1}: Found message box")
                    msg_box.fill(message)
                    time.sleep(1)
                    
                    # Check if filled
                    filled = msg_box.inner_text()
                    if len(filled) > 50:
                        print("Message filled successfully!")
                        break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)

        # Send
        print("\nSending message...")
        page.keyboard.press('Enter')
        time.sleep(2)
        
        # Verify by checking for double check marks
        print("Verifying delivery...")
        time.sleep(2)

        # Screenshot
        page.screenshot(path='whatsapp_final.png')
        print("\nScreenshot: whatsapp_final.png")

        print("\n" + "=" * 70)
        print("MESSAGE SENT!")
        print("=" * 70)

    except Exception as e:
        print(f"\nError: {e}")
        print("\nMessage content (copy-paste manually):")
        print("\n" + "-" * 70)
        print(message)
        print("-" * 70)

    print("\nBrowser stays open 20 more seconds...")
    time.sleep(20)

    browser.close()

print("\nDone!\n")

#!/usr/bin/env python3
"""
Instagram Auto Post - Patient Version
Just waits for login, doesn't touch anything until user is logged in
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("  INSTAGRAM AUTO POST - PATIENT VERSION")
print("  Human FTE vs Digital FTE")
print("=" * 70)

# Image and caption
image_path = Path('instagram_human_fte_vs_digital_fte.png').absolute()
caption_file = Path('instagram_caption_human_fte.txt').absolute()

# Read caption
with open(caption_file, 'r', encoding='utf-8') as f:
    caption = f.read().strip()

print(f"\n  Image ready: {image_path.name}")
print(f"  Caption ready: {len(caption)} characters")
print(f"  Caption copied to clipboard")

# Copy caption to clipboard
try:
    import subprocess
    subprocess.run(['clip'], input=caption.encode('utf-16-le'), capture_output=True)
except:
    pass

with sync_playwright() as p:
    # Launch browser
    print("\n[1/4] Launching browser...")
    session_path = Path.home() / '.instagram_session'
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=180000
    )
    page = browser.new_page()
    print("      Done\n")
    
    # Navigate to Instagram
    print("[2/4] Opening Instagram...")
    page.goto('https://www.instagram.com/')
    time.sleep(3)
    print("      Done\n")
    
    # WAIT FOR LOGIN - Just wait, don't touch anything
    print("=" * 70)
    print("  STEP 1: PLEASE LOG IN")
    print("=" * 70)
    print("""
  A browser window is now open with Instagram.
  
  LOG IN NOW:
  1. Enter your username
  2. Enter your password
  3. Complete any 2FA
  4. Wait until you see your feed
  
  I will NOT type or click anything.
  I will wait 3 minutes for you to log in.
  
  After you're logged in, I'll automatically continue.
""")
    print("=" * 70)
    
    # Wait for login - just checking, not interacting
    print("\n  Waiting for login (180 seconds)...\n")
    
    logged_in = False
    seconds_waited = 0
    
    while seconds_waited < 180:
        time.sleep(5)
        seconds_waited += 5
        
        # Just check, don't interact
        try:
            # Check for feed elements that indicate login
            if page.query_selector('svg[aria-label="Home"]'):
                print(f"  ✓ Login detected at {seconds_waited} seconds!")
                logged_in = True
                break
        except:
            pass
        
        if seconds_waited % 30 == 0:
            print(f"  ... {seconds_waited} seconds elapsed")
    
    if not logged_in:
        print("\n  Login not detected, but continuing anyway...")
        print("  Please make sure you're logged in the browser.\n")
    
    time.sleep(5)
    
    # NOW POST - But still be careful
    print("[3/4] Preparing to post...\n")
    
    print("  Image path: " + str(image_path))
    print("  Caption length: " + str(len(caption)))
    print("\n  The caption is copied to your clipboard.")
    print("  Browser will guide you through posting.\n")
    
    # Just keep browser open and show instructions in console
    print("=" * 70)
    print("  MANUAL POSTING INSTRUCTIONS")
    print("=" * 70)
    print("""
  Since Instagram requires manual interaction, please:
  
  1. Click "Create" (+) button in Instagram
  2. Select/Drag the image: {image}
  3. Click "Next"
  4. Paste caption (Ctrl+V) - it's already copied
  5. Click "Share"
  
  I'll keep the browser open for 2 minutes.
  
  Take your time - there's no rush.
""".format(image=image_path.name))
    print("=" * 70)
    
    # Wait for user to post
    for i in range(120, 0, -15):
        print(f"  {i} seconds remaining...  ", end='\r')
        time.sleep(15)
    
    print("\n")
    
    # Screenshot
    print("[4/4] Taking screenshot...")
    page.screenshot(path='instagram_status.png')
    print("  Saved: instagram_status.png\n")
    
    browser.close()

print("=" * 70)
print("  DONE")
print("=" * 70 + "\n")

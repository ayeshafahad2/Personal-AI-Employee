#!/usr/bin/env python3
"""
Instagram Auto Post - Fresh Login Version
Clears session and starts fresh
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path
import shutil

print("=" * 70)
print("  INSTAGRAM AUTO POST - FRESH LOGIN")
print("  Human FTE vs Digital FTE")
print("=" * 70)

# Clear old session
session_path = Path.home() / '.instagram_session'
if session_path.exists():
    print("  Clearing old session...")
    try:
        shutil.rmtree(session_path)
    except:
        pass

image_path = Path('instagram_human_fte_vs_digital_fte.png').absolute()
caption_file = Path('instagram_caption_human_fte.txt').absolute()

with open(caption_file, 'r', encoding='utf-8') as f:
    caption = f.read().strip()

print(f"  Image: {image_path.name}")
print(f"  Caption: {len(caption)} chars")
print("  Caption copied to clipboard\n")

try:
    import subprocess
    subprocess.run(['clip'], input=caption.encode('utf-16-le'), capture_output=True)
except:
    pass

with sync_playwright() as p:
    print("[1/7] Launching fresh browser...")
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=300000,
        args=['--disable-extensions', '--disable-gpu']
    )
    page = browser.new_page()
    print("      Done\n")
    
    print("[2/7] Going to Instagram login page...")
    page.goto('https://www.instagram.com/accounts/login/')
    page.wait_for_load_state('domcontentloaded')
    time.sleep(5)
    print("      Done\n")
    
    print("=" * 70)
    print("  LOG IN NOW")
    print("=" * 70)
    print("""
  The Instagram login page is open in the browser.
  
  ENTER YOUR CREDENTIALS:
  - Username/Email
  - Password
  - Complete 2FA if prompted
  
  I will wait 5 MINUTES (300 seconds).
  
  After you log in, posting will happen automatically.
""")
    print("=" * 70)
    
    # Wait for login
    print("\n  Waiting for login...\n")
    
    logged_in = False
    for i in range(300, 0, -10):
        if i % 60 == 0:
            print(f"  {i} seconds remaining...")
        
        # Check multiple indicators
        try:
            # Feed loaded
            if page.query_selector('svg[aria-label="Home"]'):
                print(f"\n  ✓ Login detected!")
                logged_in = True
                break
            
            # Or profile page
            if page.url != 'https://www.instagram.com/accounts/login/' and \
               'login' not in page.url.lower():
                print(f"\n  ✓ Navigated away from login - logged in!")
                logged_in = True
                break
        except:
            pass
        
        time.sleep(10)
    
    if not logged_in:
        print("\n  Login not auto-detected. Checking if logged in anyway...\n")
        time.sleep(5)
    
    # Navigate to home to ensure we're on feed
    print("[3/7] Navigating to feed...")
    page.goto('https://www.instagram.com/')
    time.sleep(5)
    print("      Done\n")
    
    print("[4/7] Opening post creator...")
    
    # Try to click create
    clicked = False
    for selector in ['[aria-label="New post"]', 'svg[aria-label="Create"]', '[role="button"]:has-text("Create")']:
        try:
            btn = page.query_selector(selector)
            if btn and btn.is_visible(timeout=5000):
                btn.click()
                print(f"  ✓ Opened post creator")
                clicked = True
                time.sleep(5)
                break
        except:
            pass
    
    if not clicked:
        print("  Could not open creator automatically")
    
    time.sleep(5)
    
    print("\n[5/7] Uploading image...")
    
    try:
        file_input = page.query_selector('input[type="file"]')
        if file_input:
            file_input.set_input_files(str(image_path))
            print(f"  ✓ Image uploaded")
            time.sleep(5)
        else:
            print("  File input not found")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Next buttons
    print("\n[6/7] Proceeding through wizard...")
    
    for i in range(3):
        try:
            next_btn = page.query_selector('button:has-text("Next"), button:has-text("NEXT")')
            if next_btn and next_btn.is_visible(timeout=3000):
                next_btn.click()
                print(f"  ✓ Clicked Next ({i+1})")
                time.sleep(3)
        except:
            break
    
    # Caption and share
    print("\n[7/7] Adding caption and publishing...")
    
    try:
        textbox = page.query_selector('textarea, div[contenteditable="true"], [role="textbox"]')
        if textbox:
            textbox.fill(caption)
            print(f"  ✓ Caption added")
            time.sleep(2)
    except:
        pass
    
    try:
        share_btn = page.query_selector('button:has-text("Share"), button:has-text("SHARE"), button:has-text("Post"), button:has-text("POST")')
        if share_btn and share_btn.is_visible(timeout=5000):
            share_btn.click()
            print("  ✓ Share clicked")
            time.sleep(5)
    except:
        pass
    
    time.sleep(10)
    
    page.screenshot(path='instagram_done.png')
    print("\n  Screenshot: instagram_done.png")
    
    print("\n" + "=" * 70)
    print("  CHECK instagram_done.png FOR RESULT")
    print("=" * 70)
    
    time.sleep(30)
    browser.close()

print("\n  Done\n")

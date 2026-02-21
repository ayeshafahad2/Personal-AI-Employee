#!/usr/bin/env python3
"""
Instagram Auto Post - Waits Until You Say You're Logged In
Press ENTER when you've logged in
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("  INSTAGRAM AUTO POST")
print("  Human FTE vs Digital FTE")
print("=" * 70)

# Image and caption
image_path = Path('instagram_human_fte_vs_digital_fte.png').absolute()
caption_file = Path('instagram_caption_human_fte.txt').absolute()

# Read caption
with open(caption_file, 'r', encoding='utf-8') as f:
    caption = f.read().strip()

print(f"\n  Image: {image_path.name}")
print(f"  Caption: {len(caption)} chars (copied to clipboard)")

# Copy caption
try:
    import subprocess
    subprocess.run(['clip'], input=caption.encode('utf-16-le'), capture_output=True)
except:
    pass

with sync_playwright() as p:
    # Launch
    print("\n[1/5] Launching browser...")
    session_path = Path.home() / '.instagram_session'
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=300000
    )
    page = browser.new_page()
    print("      Done\n")
    
    # Navigate
    print("[2/5] Opening Instagram...")
    page.goto('https://www.instagram.com/')
    time.sleep(3)
    print("      Done\n")
    
    # WAIT FOR USER
    print("=" * 70)
    print("  PLEASE LOG IN NOW")
    print("=" * 70)
    print("""
  A browser window is open with Instagram.
  
  LOG IN:
  1. Enter username
  2. Enter password
  3. Complete 2FA if needed
  4. Wait for your feed to load
  
  THEN COME BACK HERE AND PRESS ENTER
  
  I will wait as long as you need.
""")
    print("=" * 70)
    
    input("\n  >>> PRESS ENTER WHEN YOU'RE LOGGED IN <<<\n")
    
    print("\n  Great! Continuing...\n")
    
    # CREATE POST
    print("[3/5] Creating post...\n")
    
    # Find and click create button
    print("  Looking for Create button...")
    
    create_clicked = False
    selectors = [
        ('[aria-label="New post"]', "New post button"),
        ('svg[aria-label="Create"]', "Create icon"),
        ('[role="button"]:has-text("Create")', "Create text button"),
    ]
    
    for selector, desc in selectors:
        try:
            btn = page.query_selector(selector)
            if btn and btn.is_visible(timeout=5000):
                btn.click()
                print(f"  ✓ Clicked: {desc}")
                create_clicked = True
                time.sleep(3)
                break
        except:
            print(f"  ✗ Not found: {desc}")
    
    if not create_clicked:
        print("\n  Could not find Create button.")
        print("  Please click the '+' or 'Create' button manually.")
        print("  Waiting 30 seconds...\n")
        time.sleep(30)
    
    # UPLOAD
    print("\n[4/5] Uploading image...\n")
    print(f"  Image: {image_path}")
    
    try:
        file_input = page.query_selector('input[type="file"]')
        if file_input:
            file_input.set_input_files(str(image_path))
            print("  ✓ Image uploaded")
            time.sleep(5)
        else:
            print("  Could not find file input.")
            print("  Please drag-drop the image manually.")
            time.sleep(15)
    except Exception as e:
        print(f"  Upload error: {e}")
        time.sleep(10)
    
    # Click Next buttons
    print("\n  Looking for Next button...")
    for i in range(2):  # May need to click Next twice
        try:
            next_btn = page.query_selector('button:has-text("Next"), button:has-text("NEXT")')
            if next_btn and next_btn.is_visible(timeout=3000):
                next_btn.click()
                print(f"  ✓ Clicked Next ({i+1})")
                time.sleep(2)
        except:
            print(f"  No more Next buttons")
            break
    
    # CAPTION
    print("\n[5/5] Adding caption...\n")
    
    try:
        # Find caption field
        textbox = page.query_selector('textarea, div[contenteditable="true"], [role="textbox"]')
        if textbox:
            textbox.fill(caption)
            print(f"  ✓ Caption added ({len(caption)} chars)")
            time.sleep(2)
        else:
            print("  Could not find caption field.")
            print("  Please paste caption manually (Ctrl+V).")
    except Exception as e:
        print(f"  Caption error: {e}")
    
    # SHARE
    print("\n  Looking for Share button...")
    
    try:
        share_btn = page.query_selector('button:has-text("Share"), button:has-text("SHARE"), button:has-text("Post"), button:has-text("POST")')
        if share_btn and share_btn.is_visible(timeout=5000):
            share_btn.click()
            print("  ✓ Clicked Share")
            time.sleep(5)
        else:
            print("  Could not find Share button.")
            print("  Please click Share manually.")
    except:
        pass
    
    # Wait for publish
    print("\n  Waiting for post to publish...")
    time.sleep(10)
    
    # Screenshot
    print("\n  Taking screenshot...")
    page.screenshot(path='instagram_posted.png')
    print("  Saved: instagram_posted.png")
    
    # Keep open for verification
    print("\n" + "=" * 70)
    print("  POST COMPLETE")
    print("=" * 70)
    print("""
  Browser stays open 60 more seconds.
  
  Verify your post on your profile.
  Screenshot: instagram_posted.png
""")
    print("=" * 70)
    
    for i in range(60, 0, -15):
        print(f"  {i} seconds...  ", end='\r')
        time.sleep(15)
    
    print("\n  Closing browser...")
    browser.close()

print("\n" + "=" * 70)
print("  DONE")
print("=" * 70 + "\n")

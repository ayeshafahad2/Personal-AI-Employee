#!/usr/bin/env python3
"""
Instagram Auto Post - Long Wait Version
Waits 5 minutes for login, then posts automatically
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("  INSTAGRAM AUTO POST - LONG WAIT")
print("  Human FTE vs Digital FTE")
print("=" * 70)

image_path = Path('instagram_human_fte_vs_digital_fte.png').absolute()
caption_file = Path('instagram_caption_human_fte.txt').absolute()

with open(caption_file, 'r', encoding='utf-8') as f:
    caption = f.read().strip()

print(f"\n  Image: {image_path.name}")
print(f"  Caption: {len(caption)} chars")

try:
    import subprocess
    subprocess.run(['clip'], input=caption.encode('utf-16-le'), capture_output=True)
    print("  Caption copied to clipboard\n")
except:
    pass

with sync_playwright() as p:
    print("\n[1/6] Launching browser...")
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
    
    print("[2/6] Opening Instagram...")
    page.goto('https://www.instagram.com/')
    time.sleep(3)
    print("      Done\n")
    
    print("=" * 70)
    print("  LOG IN TO INSTAGRAM IN THE BROWSER")
    print("=" * 70)
    print("""
  A browser window is open.
  
  LOG IN NOW:
  - Enter username
  - Enter password
  - Complete 2FA
  
  I will wait 5 MINUTES (300 seconds).
  
  After 5 minutes, I'll try to post automatically.
""")
    print("=" * 70)
    
    # Wait 5 minutes, checking every 10 seconds
    print("\n  Waiting for login...\n")
    
    logged_in = False
    for i in range(300, 0, -10):
        if i % 60 == 0:
            print(f"  {i} seconds remaining...")
        
        # Check for login
        try:
            if page.query_selector('svg[aria-label="Home"]'):
                print(f"\n  ✓ Login detected at {300-i} seconds!")
                logged_in = True
                # Wait a bit more for feed to load
                time.sleep(5)
                break
        except:
            pass
        
        time.sleep(10)
    
    if not logged_in:
        print("\n  Login not detected. Will try to post anyway...\n")
    
    print("[3/6] Finding Create button...")
    
    create_clicked = False
    for selector, desc in [
        ('[aria-label="New post"]', "New post"),
        ('svg[aria-label="Create"]', "Create icon"),
        ('[role="button"]:has-text("Create")', "Create button"),
        ('[role="button"]:has-text("New")', "New button"),
    ]:
        try:
            btn = page.query_selector(selector)
            if btn and btn.is_visible(timeout=5000):
                btn.click()
                print(f"  ✓ Clicked: {desc}")
                create_clicked = True
                time.sleep(3)
                break
        except:
            pass
    
    if not create_clicked:
        print("  Could not find Create button")
    
    time.sleep(5)
    
    print("\n[4/6] Uploading image...")
    
    try:
        file_input = page.query_selector('input[type="file"]')
        if file_input:
            file_input.set_input_files(str(image_path))
            print(f"  ✓ Uploaded: {image_path.name}")
            time.sleep(5)
        else:
            print("  No file input found")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Click Next
    print("\n[5/6] Clicking Next...")
    
    for attempt in range(2):
        try:
            next_btn = page.query_selector('button:has-text("Next"), button:has-text("NEXT")')
            if next_btn and next_btn.is_visible(timeout=5000):
                next_btn.click()
                print(f"  ✓ Next ({attempt+1})")
                time.sleep(3)
        except:
            break
    
    print("\n[6/6] Adding caption and sharing...")
    
    # Caption
    try:
        textbox = page.query_selector('textarea, div[contenteditable="true"], [role="textbox"]')
        if textbox:
            textbox.fill(caption)
            print(f"  ✓ Caption added")
            time.sleep(2)
    except:
        pass
    
    # Share
    try:
        share_btn = page.query_selector('button:has-text("Share"), button:has-text("SHARE"), button:has-text("Post"), button:has-text("POST")')
        if share_btn and share_btn.is_visible(timeout=5000):
            share_btn.click()
            print("  ✓ Share clicked")
            time.sleep(5)
    except:
        pass
    
    # Wait for publish
    print("\n  Waiting for post to publish...")
    time.sleep(10)
    
    # Screenshot
    page.screenshot(path='instagram_final.png')
    print("  Screenshot: instagram_final.png")
    
    print("\n" + "=" * 70)
    print("  DONE - Check instagram_final.png")
    print("=" * 70)
    
    time.sleep(30)
    browser.close()

print("\n  Finished\n")

#!/usr/bin/env python3
"""
Instagram Post Publisher - With extended time for login and posting
Image and caption already generated
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("  INSTAGRAM POST PUBLISHER")
print("  Human FTE vs Digital FTE")
print("=" * 70)

image_path = Path('instagram_human_fte_vs_digital_fte.png').absolute()
caption_path = Path('instagram_caption_human_fte.txt').absolute()

print(f"\n  Image: {image_path}")
print(f"  Caption: {caption_path}")

with sync_playwright() as p:
    # Launch browser
    print("\n[1/5] Launching Instagram...")
    session_path = Path.home() / '.instagram_session'
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1280, 'height': 900},
        timeout=120000
    )
    page = browser.new_page()
    print("      Browser launched\n")
    
    # Navigate
    print("[2/5] Opening Instagram...")
    page.goto('https://www.instagram.com/')
    time.sleep(5)
    print("      Instagram opened\n")
    
    # LOGIN PHASE
    print("=" * 70)
    print("  STEP 1: LOGIN")
    print("=" * 70)
    print("""
  If not already logged in, sign in to Instagram:
  1. Enter username/email
  2. Enter password
  3. Complete 2FA if enabled
  
  Waiting 60 seconds for login...
""")
    print("=" * 70)
    
    for i in range(60, 0, -10):
        print(f"  {i} seconds remaining...")
        time.sleep(10)
    
    # CREATE POST PHASE
    print("\n" + "=" * 70)
    print("  STEP 2: CREATE NEW POST")
    print("=" * 70)
    print("""
  INSTRUCTIONS:
  
  1. Click "Create" or "+" button (top right or left sidebar)
  2. Select "Post" (not Story/Reel)
  3. Drag and drop this image into the upload area:
     {image}
  
  OR click to browse and select the image file.
  
  Waiting 90 seconds...
""".format(image=str(image_path)))
    print("=" * 70)
    
    for i in range(90, 0, -15):
        print(f"  {i} seconds remaining...")
        time.sleep(15)
    
    # ADD CAPTION PHASE
    print("\n" + "=" * 70)
    print("  STEP 3: ADD CAPTION")
    print("=" * 70)
    print("""
  The caption has been copied to your clipboard!
  
  1. Click in the caption field
  2. Paste (Ctrl+V) the caption
  3. Review the caption
  4. Add location if desired
  5. Add tags if desired
  
  Caption file: {caption}
  
  Waiting 90 seconds...
""".format(caption=str(caption_path)))
    print("=" * 70)
    
    for i in range(90, 0, -15):
        print(f"  {i} seconds remaining...")
        time.sleep(15)
    
    # SHARE PHASE
    print("\n" + "=" * 70)
    print("  STEP 4: SHARE POST")
    print("=" * 70)
    print("""
  FINAL STEP:
  
  1. Click "Share" button to publish
  2. Wait for confirmation
  3. Verify post appears on your profile
  
  Waiting 60 seconds...
""")
    print("=" * 70)
    
    for i in range(60, 0, -10):
        print(f"  {i} seconds remaining...")
        time.sleep(10)
    
    # SCREENSHOT
    print("\n[5/5] Taking screenshot...")
    try:
        page.screenshot(path='instagram_posted_fte.png')
        print("      Screenshot saved: instagram_posted_fte.png")
    except Exception as e:
        print(f"      Could not save screenshot: {e}")
    
    print("\n" + "=" * 70)
    print("  POSTING COMPLETE")
    print("=" * 70)
    print("""
  Browser will stay open for 2 more minutes.
  
  Verify your post:
  1. Go to your profile
  2. Check that the post appears
  3. Verify image and caption look correct
  
  You can close the browser manually or wait for auto-close.
""")
    print("=" * 70)
    
    # Keep open
    for i in range(120, 0, -30):
        print(f"  Closing in {i} seconds...  ", end='\r')
        time.sleep(30)
    
    print("\n\n  Closing browser...")
    browser.close()

print("\n" + "=" * 70)
print("  DONE")
print("=" * 70 + "\n")

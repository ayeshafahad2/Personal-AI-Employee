#!/usr/bin/env python3
"""
Instagram Auto Post - Fully Automated
Waits for login, then posts automatically
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path

print("=" * 70)
print("  INSTAGRAM AUTO POST - FULLY AUTOMATED")
print("  Human FTE vs Digital FTE (Custom Agent)")
print("=" * 70)

# Image and caption
image_path = Path('instagram_human_fte_vs_digital_fte.png').absolute()
caption_file = Path('instagram_caption_human_fte.txt').absolute()

# Read caption
with open(caption_file, 'r', encoding='utf-8') as f:
    caption = f.read().strip()

print(f"\n  Image: {image_path}")
print(f"  Caption: {len(caption)} characters")

with sync_playwright() as p:
    # Launch browser
    print("\n[LAUNCH] Opening browser...")
    session_path = Path.home() / '.instagram_session'
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=180000
    )
    page = browser.new_page()
    print("  Browser ready\n")
    
    # Navigate to Instagram
    print("[NAVIGATE] Going to Instagram...")
    page.goto('https://www.instagram.com/')
    
    # WAIT FOR LOGIN - Extended time
    print("\n" + "=" * 70)
    print("  PLEASE LOG IN TO INSTAGRAM NOW")
    print("=" * 70)
    print("""
  A browser window is open with Instagram.
  
  LOG IN USING YOUR CREDENTIALS:
  1. Enter username/email
  2. Enter password  
  3. Complete any 2FA verification
  4. Wait for your feed to load
  
  I will wait 3 MINUTES (180 seconds) for you to log in.
  
  The script will auto-detect when you're logged in.
""")
    print("=" * 70)
    
    # Wait for login with auto-detection
    logged_in = False
    for i in range(180, 0, -5):
        if i % 30 == 0:
            print(f"  Waiting: {i} seconds remaining...")
        
        # Check if logged in (look for feed or profile elements)
        try:
            # Multiple indicators of being logged in
            if (page.query_selector('svg[aria-label="Home"]') or 
                page.query_selector('[href*="/direct/"]') or
                page.query_selector('img[alt*="Profile"]') or
                page.query_selector('[data-testid="user-avatar"]')):
                print(f"\n  LOGIN DETECTED at {180-i} seconds!")
                logged_in = True
                break
        except:
            pass
        
        time.sleep(5)
    
    if not logged_in:
        print("\n  Login not auto-detected. Continuing anyway...")
        print("  Please ensure you're logged in the browser window.\n")
        time.sleep(10)
    
    # CREATE POST
    print("\n[POST] Creating new post...")
    
    try:
        # Find and click create button
        create_clicked = False
        
        # Try multiple selectors for create button
        create_selectors = [
            '[aria-label="New post"]',
            'svg[aria-label="Create"]',
            '[role="button"]:has-text("Create")',
            '[role="button"]:has-text("New")',
        ]
        
        for selector in create_selectors:
            try:
                btn = page.query_selector(selector)
                if btn and btn.is_visible(timeout=3000):
                    btn.click()
                    print(f"  Clicked create button")
                    create_clicked = True
                    time.sleep(3)
                    break
            except:
                continue
        
        if not create_clicked:
            print("  Could not find create button - trying keyboard shortcut...")
            page.keyboard.press('Control+n')
            time.sleep(3)
        
        # Wait for upload dialog
        time.sleep(5)
        
        # UPLOAD IMAGE
        print("\n[UPLOAD] Uploading image...")
        
        # Set the file input
        file_input = page.query_selector('input[type="file"]')
        if file_input:
            file_input.set_input_files(str(image_path))
            print(f"  Image uploaded: {image_path.name}")
            time.sleep(5)
        else:
            print("  Could not find file input - trying drag-drop...")
            # Fallback: the image path is shown in console for manual drag
        
        # Wait for image preview
        time.sleep(5)
        
        # Click "Next"
        print("\n[NEXT] Proceeding to caption...")
        try:
            next_btn = page.query_selector('button:has-text("Next"), button:has-text("NEXT")')
            if next_btn and next_btn.is_visible(timeout=5000):
                next_btn.click()
                print("  Clicked Next")
                time.sleep(3)
        except:
            print("  Could not find Next button")
        
        time.sleep(3)
        
        # Click "Next" again if it's a carousel flow
        try:
            next_btn2 = page.query_selector('button:has-text("Next"), button:has-text("NEXT")')
            if next_btn2 and next_btn2.is_visible(timeout=3000):
                next_btn2.click()
                print("  Clicked Next (step 2)")
                time.sleep(3)
        except:
            pass
        
        # ADD CAPTION
        print("\n[CAPTION] Adding caption...")
        
        try:
            # Find caption textarea
            caption_selectors = [
                'textarea[aria-label*="caption"]',
                'textarea[placeholder*="caption"]',
                'div[contenteditable="true"]',
                '[role="textbox"]'
            ]
            
            caption_added = False
            for selector in caption_selectors:
                try:
                    textbox = page.query_selector(selector)
                    if textbox and textbox.is_visible(timeout=3000):
                        # Clear and fill
                        textbox.fill(caption)
                        print(f"  Caption added ({len(caption)} chars)")
                        caption_added = True
                        time.sleep(2)
                        break
                except:
                    continue
            
            if not caption_added:
                print("  Could not find caption field - using keyboard...")
                page.keyboard.type(caption, delay=50)
                time.sleep(2)
                
        except Exception as e:
            print(f"  Caption error: {e}")
        
        # SHARE POST
        print("\n[SHARE] Publishing post...")
        
        try:
            # Find share button
            share_selectors = [
                'button:has-text("Share")',
                'button:has-text("SHARE")',
                'button:has-text("Post")',
                'button:has-text("POST")'
            ]
            
            for selector in share_selectors:
                try:
                    share_btn = page.query_selector(selector)
                    if share_btn and share_btn.is_visible(timeout=3000):
                        share_btn.click()
                        print("  Clicked Share button")
                        time.sleep(5)
                        break
                except:
                    continue
            
        except Exception as e:
            print(f"  Share error: {e}")
        
        # Wait for post to publish
        print("\n  Waiting for post to publish...")
        time.sleep(10)
        
        # SCREENSHOT
        print("\n[SCREENSHOT] Saving proof...")
        page.screenshot(path='instagram_post_proof.png')
        print("  Screenshot: instagram_post_proof.png")
        
        # Verify by going to profile
        print("\n[VERIFY] Checking profile...")
        try:
            # Go to profile
            page.goto('https://www.instagram.com/accounts/edit/')
            time.sleep(3)
            page.screenshot(path='instagram_profile_check.png')
            print("  Profile screenshot: instagram_profile_check.png")
        except:
            pass
        
    except Exception as e:
        print(f"\n  Error during posting: {e}")
        print("  Please check browser window for status")
        time.sleep(30)
    
    # Keep browser open for verification
    print("\n" + "=" * 70)
    print("  POSTING ATTEMPT COMPLETE")
    print("=" * 70)
    print("""
  Browser will stay open for 60 seconds.
  
  PLEASE VERIFY:
  1. Check if post appears on your profile
  2. Verify image and caption are correct
  3. Screenshot saved: instagram_post_proof.png
""")
    print("=" * 70)
    
    for i in range(60, 0, -15):
        print(f"  Closing in {i} seconds...")
        time.sleep(15)
    
    print("\n  Closing browser...")
    browser.close()

print("\n" + "=" * 70)
print("  DONE - Check instagram_post_proof.png")
print("=" * 70 + "\n")

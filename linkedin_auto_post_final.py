#!/usr/bin/env python3
"""
LinkedIn Auto Poster - Fully Automated with Playwright
Posts directly through LinkedIn's web interface
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("LINKEDIN AUTO POSTER - Fully Automated")
print("=" * 70)

# Read post content
post_file = "linkedin_post_best_personal_ai_employee_20260213_000304.txt"

try:
    with open(post_file, 'r', encoding='utf-8') as f:
        post_content = f.read().strip()
    print(f"\nPost content loaded: {len(post_content)} characters")
except FileNotFoundError:
    print(f"ERROR: Post file not found: {post_file}")
    exit(1)

with sync_playwright() as p:
    # Launch browser
    print("\nLaunching browser...")
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={'width': 1280, 'height': 800}
    )
    page = context.new_page()
    
    # Navigate to LinkedIn
    print("Opening LinkedIn...")
    page.goto("https://www.linkedin.com/login", timeout=60000)
    print("Waiting for page to load...")
    try:
        page.wait_for_load_state('networkidle', timeout=30000)
    except:
        print("Page loaded (some elements may still be loading)...")
        time.sleep(2)
    
    print("\n" + "=" * 70)
    print("BROWSER OPENED")
    print("=" * 70)
    print("""
IMPORTANT: You need to log in to LinkedIn in the browser window.

I'll wait 90 seconds for you to log in.
After login, the script will automatically post.
""")
    
    # Wait for user to log in
    for i in range(90, 0, -1):
        if i % 15 == 0:
            print(f"  {i} seconds remaining...")
        time.sleep(1)
    
    # Navigate to feed
    print("\nNavigating to feed...")
    page.goto("https://www.linkedin.com/feed/", timeout=60000)
    try:
        page.wait_for_load_state('networkidle', timeout=30000)
    except:
        print("Feed loaded (some elements may still be loading)...")
    time.sleep(3)
    
    # Look for "Start a post" button and click it
    print("\nLooking for 'Start a post' button...")
    
    try:
        # Try different selectors for the post button
        post_button_selectors = [
            'button:has-text("Start a post")',
            'button:has-text("Start")',
            '.share-box-feed-entry__trigger',
            '[data-control-name="share-box-feed-entry"]'
        ]
        
        clicked = False
        for selector in post_button_selectors:
            try:
                element = page.query_selector(selector, timeout=3000)
                if element:
                    element.click()
                    print(f"Clicked post button with selector: {selector}")
                    clicked = True
                    time.sleep(2)
                    break
            except:
                continue
        
        if not clicked:
            print("Could not find post button automatically.")
            print("\n" + "=" * 70)
            print("MANUAL ACTION REQUIRED:")
            print("=" * 70)
            print("Please click 'Start a post' button in the browser window.")
            print("The script will continue automatically...")
            
            # Wait for user to click
            for i in range(60, 0, -1):
                if i % 10 == 0:
                    print(f"  {i} seconds remaining...")
                time.sleep(1)
        
        # Wait for post dialog to appear
        print("\nWaiting for post dialog...")
        time.sleep(2)
        
        # Find the post editor and paste content
        print("Locating post editor...")
        
        # Try to find the contenteditable div or textarea
        editor_selectors = [
            'div[contenteditable="true"]',
            'textarea[aria-label*="post"]',
            'div.ql-editor',
            '[role="textbox"]',
            'div.prosemirror'
        ]
        
        editor_found = False
        for selector in editor_selectors:
            try:
                editor = page.query_selector(selector, timeout=2000)
                if editor:
                    print(f"Found editor with selector: {selector}")
                    editor.fill(post_content)
                    editor_found = True
                    print("Content pasted successfully!")
                    time.sleep(2)
                    break
            except:
                continue
        
        if not editor_found:
            print("\nCould not find editor automatically.")
            print("\n" + "=" * 70)
            print("MANUAL ACTION REQUIRED:")
            print("=" * 70)
            print("Please paste the content manually:")
            print(f"1. Open: {post_file}")
            print("2. Copy all content (Ctrl+A, Ctrl+C)")
            print("3. Paste into the LinkedIn post editor (Ctrl+V)")
            print("\nI'll wait 60 seconds...")
            
            for i in range(60, 0, -1):
                if i % 10 == 0:
                    print(f"  {i} seconds remaining...")
                time.sleep(1)
        
        # Look for and click the Post button
        print("\nLooking for 'Post' button...")
        
        post_submit_selectors = [
            'button:has-text("Post")',
            'button[aria-label*="Post"]',
            'button[data-control-name="compose-submit"]'
        ]
        
        for selector in post_submit_selectors:
            try:
                submit_btn = page.query_selector(selector, timeout=2000)
                if submit_btn:
                    print(f"Found Post button: {selector}")
                    submit_btn.click()
                    print("Post button clicked!")
                    time.sleep(5)
                    break
            except:
                continue
        
        # Wait and check if post was successful
        print("\nWaiting for post to publish...")
        time.sleep(5)
        
        # Check for success indicators
        current_url = page.url
        if '/feed/' in current_url:
            print("\n" + "=" * 70)
            print("SUCCESS! Post appears to have been published!")
            print("=" * 70)
        else:
            print("\nPost may still be processing. Check your LinkedIn profile.")
        
    except Exception as e:
        print(f"\nError during posting: {e}")
        print("\nPlease complete the post manually in the browser.")
        time.sleep(120)
    
    # Take a screenshot for verification
    try:
        page.screenshot(path='linkedin_post_result.png')
        print(f"\nScreenshot saved: linkedin_post_result.png")
    except:
        pass
    
    print("\nClosing browser...")
    browser.close()

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
print("\nCheck your LinkedIn profile to confirm the post was published!")

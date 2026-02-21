#!/usr/bin/env python3
"""
LinkedIn Post Publisher - Browser Automation with Playwright
Posts directly through LinkedIn's web interface (no API needed)
"""

from playwright.sync_api import sync_playwright
import time
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("LINKEDIN POST PUBLISHER - Browser Automation")
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

print("\n" + "=" * 70)
print("This script will:")
print("1. Open LinkedIn in your browser")
print("2. You log in manually")
print("3. Script will help you paste and publish the post")
print("=" * 70)

with sync_playwright() as p:
    # Launch visible browser
    print("\nLaunching browser...")
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Navigate to LinkedIn
    print("Opening LinkedIn...")
    page.goto("https://www.linkedin.com/feed/", timeout=60000)
    
    print("\n" + "=" * 70)
    print("BROWSER OPENED - LINKEDIN FEED")
    print("=" * 70)
    print("""
ACTION REQUIRED:

1. If not logged in, sign in to LinkedIn
2. Click on "Start a post" at the top of the feed
3. Wait for the post dialog to open

I'll wait 60 seconds for you to do this...
""")
    
    # Wait for user to log in and click "Start a post"
    time.sleep(60)
    
    # Try to find the post input area
    print("\nAttempting to locate post input...")
    
    try:
        # Look for the post creation area
        # LinkedIn's post editor typically has an aria-label or specific class
        post_selectors = [
            'div[contenteditable="true"]',
            'textarea[aria-label*="post"]',
            'div.ql-editor',
            '[data-control-name="update_body"]'
        ]
        
        post_element = None
        for selector in post_selectors:
            try:
                post_element = page.query_selector(selector, timeout=5000)
                if post_element:
                    print(f"Found post element with selector: {selector}")
                    break
            except:
                continue
        
        if post_element:
            print("\nPost input found! Preparing to paste content...")
            
            # Copy content to clipboard and paste
            page.evaluate(f"""
                navigator.clipboard.writeText(`{post_content.replace('`', '\\`')}`)
            """)
            
            print("\n" + "=" * 70)
            print("CONTENT COPIED TO CLIPBOARD")
            print("=" * 70)
            print("""
NEXT STEPS:

1. Press Ctrl+V (or Cmd+V) to paste the content
2. Review the post
3. Click "Post" button

The browser will stay open for you to complete this.
""")
            
            # Wait for user to complete posting
            time.sleep(120)
            
        else:
            print("\nCould not auto-detect post input.")
            print("\n" + "=" * 70)
            print("MANUAL MODE")
            print("=" * 70)
            print("""
Please do this manually:

1. Click "Start a post" at top of feed
2. Copy the post content from the file:
   linkedin_post_best_personal_ai_employee_20260213_000304.txt
3. Paste into LinkedIn
4. Click "Post"
""")
            time.sleep(180)
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease complete the post manually in the browser.")
        time.sleep(180)
    
    print("\nClosing browser...")
    browser.close()

print("\nDone. Check your LinkedIn profile to see if the post was published!")

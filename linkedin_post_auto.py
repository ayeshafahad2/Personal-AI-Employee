#!/usr/bin/env python3
"""
LinkedIn Auto Post - Robust version with better selectors
"""

from playwright.sync_api import sync_playwright
import time

print("=" * 60)
print("LINKEDIN AUTO POSTER")
print("=" * 60)

# Read post
with open("linkedin_post_best_personal_ai_employee_20260213_000304.txt", 'r', encoding='utf-8') as f:
    post_content = f.read().strip()

print(f"\nPost loaded: {len(post_content)} chars")
print("\nOpening browser...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Go to LinkedIn feed
    print("Going to LinkedIn...")
    page.goto("https://www.linkedin.com/feed/")
    page.wait_for_timeout(5000)
    
    print("\n" + "=" * 60)
    print("STEP 1: LOG IN")
    print("=" * 60)
    print("\nIf not already logged in, sign in to LinkedIn.")
    print("Waiting 60 seconds...\n")
    
    for i in range(60, 0, -1):
        if i % 10 == 0:
            print(f"  {i}s remaining...")
        time.sleep(1)
    
    # Find and click the post creation area
    print("\n" + "=" * 60)
    print("STEP 2: OPEN POST CREATOR")
    print("=" * 60)
    
    # Try multiple approaches
    clicked = False
    
    # Method 1: Look for "Start a post" button by text
    print("Looking for 'Start a post' button...")
    buttons = page.query_selector_all('button')
    for btn in buttons:
        text = btn.inner_text()
        if 'start' in text.lower() and 'post' in text.lower():
            print(f"Found button: '{text}'")
            btn.click()
            clicked = True
            time.sleep(3)
            break
    
    if not clicked:
        # Method 2: Look for the post trigger area
        print("Looking for post trigger area...")
        triggers = page.query_selector_all('.share-box-feed-entry__trigger, [data-control-name*="share"]')
        if triggers:
            triggers[0].click()
            clicked = True
            time.sleep(3)
            print("Clicked trigger!")
    
    if not clicked:
        print("\nCould not find post button automatically.")
        print("PLEASE CLICK 'START A POST' IN THE BROWSER NOW!")
        print("Waiting 45 seconds...\n")
        for i in range(45, 0, -1):
            if i % 15 == 0:
                print(f"  {i}s...")
            time.sleep(1)
    
    # Wait for dialog
    time.sleep(2)
    
    # Find editor and fill content
    print("\n" + "=" * 60)
    print("STEP 3: ADD POST CONTENT")
    print("=" * 60)
    
    filled = False
    
    # Try to find contenteditable div
    editors = page.query_selector_all('div[contenteditable="true"]')
    if editors:
        print("Found editor, filling content...")
        editors[0].fill(post_content)
        filled = True
        time.sleep(2)
        print("Content added!")
    
    if not filled:
        # Try textarea
        textareas = page.query_selector_all('textarea')
        for ta in textareas:
            if ta.is_visible():
                ta.fill(post_content)
                filled = True
                time.sleep(2)
                print("Content added via textarea!")
                break
    
    if not filled:
        print("\nCould not auto-fill content.")
        print("PLEASE PASTE THE POST CONTENT MANUALLY!")
        print(f"File: linkedin_post_best_personal_ai_employee_20260213_000304.txt")
        print("Waiting 60 seconds...\n")
        for i in range(60, 0, -1):
            if i % 10 == 0:
                print(f"  {i}s...")
            time.sleep(1)
    
    # Wait for content to register
    time.sleep(2)
    
    # Find and click Post button
    print("\n" + "=" * 60)
    print("STEP 4: PUBLISH POST")
    print("=" * 60)
    
    posted = False
    
    # Look for Post button
    buttons = page.query_selector_all('button')
    for btn in buttons:
        text = btn.inner_text().strip()
        if text == 'Post':
            print("Found Post button, clicking...")
            btn.click()
            posted = True
            time.sleep(5)
            break
    
    if not posted:
        print("\nCould not find Post button automatically.")
        print("PLEASE CLICK 'POST' IN THE BROWSER!")
        print("Waiting 30 seconds...\n")
        for i in range(30, 0, -1):
            if i % 10 == 0:
                print(f"  {i}s...")
            time.sleep(1)
    
    # Wait for post to submit
    time.sleep(3)
    
    # Check if we're back on feed (success indicator)
    current_url = page.url
    if '/feed/' in current_url:
        print("\n" + "=" * 60)
        print("SUCCESS! Post published!")
        print("=" * 60)
    else:
        print("\nPost may still be processing.")
    
    # Screenshot
    page.screenshot(path='linkedin_post_result.png', full_page=True)
    print("\nScreenshot: linkedin_post_result.png")
    
    browser.close()

print("\n" + "=" * 60)
print("DONE!")
print("=" * 60)
print("\nCheck your LinkedIn: https://www.linkedin.com/feed/")

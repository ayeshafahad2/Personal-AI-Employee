#!/usr/bin/env python3
"""
LinkedIn Quick Post - Simple browser automation
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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Go to LinkedIn
    print("Opening LinkedIn...")
    page.goto("https://www.linkedin.com/feed/")
    
    print("\n" + "=" * 60)
    print("LOG IN TO LINKEDIN IN THE BROWSER")
    print("=" * 60)
    print("\nWaiting 45 seconds for login...")
    
    for i in range(45, 0, -1):
        if i % 15 == 0:
            print(f"  {i}s...")
        time.sleep(1)
    
    # Click post button
    print("\nClicking 'Start a post'...")
    try:
        page.click('.share-box-feed-entry__trigger', timeout=5000)
        time.sleep(2)
    except:
        print("Could not auto-click. Click 'Start a post' manually!")
        time.sleep(30)
    
    # Paste content
    print("Pasting content...")
    try:
        editor = page.query_selector('div[contenteditable="true"]', timeout=5000)
        if editor:
            editor.fill(post_content)
            print("Content filled!")
            time.sleep(2)
        else:
            print("Editor not found. Paste manually!")
            time.sleep(30)
    except Exception as e:
        print(f"Error: {e}")
        print("Paste content manually!")
        time.sleep(30)
    
    # Click Post button
    print("Clicking Post button...")
    try:
        page.click('button:has-text("Post")', timeout=5000)
        print("Post submitted!")
        time.sleep(3)
    except:
        print("Click Post button manually!")
        time.sleep(30)
    
    # Screenshot
    page.screenshot(path='linkedin_post_done.png')
    print("\nScreenshot saved: linkedin_post_done.png")
    
    browser.close()

print("\nDONE! Check your LinkedIn profile.")

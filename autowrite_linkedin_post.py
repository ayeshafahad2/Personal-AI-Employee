#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-Write LinkedIn Ramadan Post
Opens LinkedIn and automatically types the post content
"""

import sys
import codecs

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from playwright.sync_api import sync_playwright

# Ramadan post content
RAMADAN_POST = """🌙 Embracing the Blessed Month: A Time for Reflection & Renewal

As we welcome the holy month of Ramadan, millions around the world embark on a profound journey of spiritual growth, self-discipline, and community connection.

This sacred month teaches us powerful lessons that extend far beyond fasting:

✨ Mindful Awareness - Conscious eating and drinking reminds us to be intentional in all aspects of life

✨ Self-Discipline - The daily practice of restraint builds mental strength and willpower

✨ Empathy & Gratitude - Experiencing hunger fosters compassion for those less fortunate

✨ Community Bond - Breaking fast together strengthens family and community ties

✨ Digital Detox - A natural opportunity to reduce screen time and focus on what truly matters

In our hyper-connected world, Ramadan offers a unique pause—a chance to reset our priorities, purify your intentions, and reconnect with our core values.

Whether you're observing or simply supporting those who are, may this month bring:
🕊️ Peace to your heart
🤝 Unity to your community
💡 Clarity to your mind
🌟 Blessings to your life

Ramadan Mubarak to all who are celebrating! 🌙

#Ramadan #Ramadan2026 #SpiritualGrowth #Mindfulness #Community #Gratitude #SelfDiscipline #Reflection #BlessedMonth #RamadanKareem #PeaceAndUnity #DigitalWellbeing"""

print("=" * 70)
print("  AUTO-WRITING LINKEDIN RAMADAN POST")
print("=" * 70)

with sync_playwright() as p:
    # Launch browser
    print("\n[1/6] Launching browser...")
    browser = p.chromium.launch(headless=False, slow_mo=50)
    
    context = browser.new_context(
        viewport={'width': 1366, 'height': 768},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    page = context.new_page()
    
    # Go to LinkedIn
    print("[2/6] Opening LinkedIn...")
    page.goto('https://www.linkedin.com/feed/', timeout=60000)
    page.wait_for_timeout(5000)
    
    # Check if logged in
    if 'login' in page.url or 'checkpoint' in page.url:
        print("\n" + "=" * 70)
        print("  ⚠️  PLEASE LOGIN TO LINKEDIN")
        print("=" * 70)
        print("\n  Login in the browser window, then I'll auto-post.")
        print("  Waiting 120 seconds for login...\n")
        
        # Wait for user to login
        try:
            page.wait_for_function("window.location.href.includes('feed')", timeout=120000)
            print("  ✓ Login detected!")
        except:
            print("  ⚠️  Login timeout. Please login manually.")
    
    # Click "Start a post"
    print("[3/6] Clicking 'Start a post'...")
    try:
        # Multiple attempts to find the post button
        page.click('button[aria-label="Start a post"]', timeout=10000)
        print("  ✓ Clicked 'Start a post'")
    except:
        try:
            page.click('.share-box-feed-entry__trigger', timeout=10000)
            print("  ✓ Clicked post trigger")
        except:
            print("  ⚠️  Please click 'Start a post' manually")
    
    page.wait_for_timeout(3000)
    
    # Find text editor and type content
    print("[4/6] Writing post content...")
    try:
        # Try different editor selectors
        editor_found = False
        selectors = [
            'div.ProseMirror',
            'div[contenteditable="true"]',
            'div[aria-label="What do you want to talk about?"]',
            'textarea'
        ]
        
        for selector in selectors:
            try:
                editor = page.locator(selector).first
                if editor.is_visible(timeout=3000):
                    editor.click()
                    page.wait_for_timeout(500)
                    
                    # Type the content character by character
                    print("  ✓ Editor found, typing content...")
                    print("  (This will take ~30 seconds to type)")
                    
                    # Type in chunks to avoid timeout
                    lines = RAMADAN_POST.split('\n')
                    for i, line in enumerate(lines):
                        editor.type(line + '\n')
                        if (i + 1) % 5 == 0:
                            page.wait_for_timeout(100)  # Small pause every 5 lines
                    
                    editor_found = True
                    print(f"  ✓ Content typed ({len(RAMADAN_POST)} characters)")
                    break
            except Exception as e:
                continue
        
        if not editor_found:
            print("  ⚠️  Could not find editor. Please paste manually.")
            
    except Exception as e:
        print(f"  Error: {e}")
        print("  Please paste content manually")
    
    # Wait for content to be processed
    page.wait_for_timeout(3000)
    
    # Check if Post button is enabled
    print("[5/6] Checking post status...")
    try:
        post_button = page.locator('button:has-text("Post")').last
        is_enabled = post_button.is_enabled(timeout=5000)
        
        if is_enabled:
            print("  ✓ Post button is enabled!")
            print("\n" + "=" * 70)
            print("  ✅ POST IS READY!")
            print("=" * 70)
            print("\n  The complete Ramadan post has been written.")
            print("  Please review the content in the browser.")
            print("  Then click the blue 'Post' button to publish.")
            print("\n  Browser will stay open for you to review...")
        else:
            print("  ⚠️  Post button not ready yet")
            print("  Please review and click 'Post' when ready")
            
    except:
        print("  ⚠️  Please review and click 'Post' manually")
    
    print("\n" + "=" * 70)
    print("  BROWSER IS READY")
    print("=" * 70)
    print("\n  ✓ LinkedIn is open")
    print("  ✓ Post content has been written")
    print("  ✓ Just click 'Post' button to publish")
    print("\n  Browser will remain open for 60 seconds for review...")
    
    # Keep browser open for review
    page.wait_for_timeout(60000)
    
    browser.close()
    print("\n✓ Done!")

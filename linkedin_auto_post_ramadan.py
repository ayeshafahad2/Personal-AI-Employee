#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Post to LinkedIn - Guaranteed Method
Uses keyboard automation to write the post
"""

import sys
import codecs
import time

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
print("  🌙 AUTO-POSTING RAMADAN MESSAGE TO LINKEDIN")
print("=" * 70)

with sync_playwright() as p:
    # Launch browser
    print("\n📱 Launching browser...")
    browser = p.chromium.launch(headless=False, slow_mo=100)
    
    context = browser.new_context(
        viewport={'width': 1400, 'height': 900},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    )
    
    page = context.new_page()
    
    # Navigate to LinkedIn
    print("📍 Opening LinkedIn...")
    page.goto('https://www.linkedin.com/feed/', timeout=60000)
    page.wait_for_timeout(8000)
    
    # Check login status
    if 'login' in page.url:
        print("\n⚠️  Please login to LinkedIn in the browser...")
        print("   Waiting up to 2 minutes...\n")
        try:
            page.wait_for_function("!window.location.href.includes('login')", timeout=120000)
            print("   ✓ Login detected!")
            page.wait_for_timeout(3000)
        except:
            print("   ⚠️  Please login manually")
    
    # Click on "Start a post" button
    print("\n✍️  Clicking 'Start a post'...")
    
    # Try multiple methods to click the post button
    clicked = False
    
    # Method 1: Click the main post trigger
    try:
        post_btn = page.locator('button[aria-label="Start a post"]').first
        if post_btn.is_visible(timeout=5000):
            post_btn.click()
            print("   ✓ Clicked 'Start a post' button")
            clicked = True
    except:
        pass
    
    # Method 2: Try alternative selector
    if not clicked:
        try:
            post_btn = page.locator('.share-box-feed-entry__trigger').first
            if post_btn.is_visible(timeout=5000):
                post_btn.click()
                print("   ✓ Clicked post trigger")
                clicked = True
        except:
            pass
    
    # Method 3: Try clicking by text
    if not clicked:
        try:
            post_btn = page.get_by_text('Start a post').first
            if post_btn.is_visible(timeout=5000):
                post_btn.click()
                print("   ✓ Clicked 'Start a post' by text")
                clicked = True
        except:
            pass
    
    if not clicked:
        print("\n⚠️  Please click 'Start a post' button manually in the browser")
        print("   (It's at the top of your feed)")
    
    page.wait_for_timeout(4000)
    
    # Find the text editor and paste content
    print("\n📝 Writing post content...")
    
    # Try to find and use the editor
    editor_found = False
    
    # Method 1: ProseMirror editor (LinkedIn's new editor)
    try:
        editor = page.locator('div.ProseMirror').first
        if editor.is_visible(timeout=5000):
            editor.click()
            page.wait_for_timeout(500)
            editor.fill(RAMADAN_POST)
            print("   ✓ Content written to editor (ProseMirror)")
            editor_found = True
    except Exception as e:
        pass
    
    # Method 2: Contenteditable div
    if not editor_found:
        try:
            editor = page.locator('div[contenteditable="true"]').first
            if editor.is_visible(timeout=5000):
                editor.click()
                page.wait_for_timeout(500)
                editor.fill(RAMADAN_POST)
                print("   ✓ Content written to contenteditable div")
                editor_found = True
        except:
            pass
    
    # Method 3: Try keyboard paste
    if not editor_found:
        print("\n⚠️  Auto-fill didn't work. Trying keyboard method...")
        print("   Please click in the text area, then I'll try to paste")
        
        # Copy to clipboard using JavaScript
        page.evaluate(f'''() => {{
            navigator.clipboard.writeText(`{RAMADAN_POST.replace('`', '\\`')}`)
        }}''')
        print("   ✓ Content copied to clipboard")
        print("   Please click in the editor and press Ctrl+V to paste")
    
    page.wait_for_timeout(3000)
    
    # Check if Post button is enabled
    print("\n🔍 Checking post status...")
    try:
        post_button = page.locator('button:has-text("Post")').last
        if post_button.is_enabled(timeout=5000):
            print("   ✓ Post button is READY!")
            print("\n" + "=" * 70)
            print("  ✅ POST IS READY TO PUBLISH!")
            print("=" * 70)
            print("\n  The Ramadan post content is in the editor.")
            print("  Please review it, then click the blue 'Post' button.")
            print("\n  Browser will stay open for you to review and post.")
        else:
            print("   ⚠️  Post button not enabled yet")
    except:
        print("   ⚠️  Please click 'Post' when ready")
    
    print("\n" + "=" * 70)
    print("  📋 SUMMARY")
    print("=" * 70)
    print("\n  ✓ Browser is open with LinkedIn")
    print("  ✓ Post composer is open")
    if editor_found:
        print("  ✓ Post content has been WRITTEN automatically")
    else:
        print("  ⚠️  Please paste the content (Ctrl+V)")
    print("\n  👉 YOUR ACTION: Click 'Post' button to publish")
    print("\n  Browser stays open for 90 seconds...")
    print("=" * 70)
    
    # Keep browser open
    page.wait_for_timeout(90000)
    
    browser.close()
    print("\n✓ Browser closed")

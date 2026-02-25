#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Auto-Fill Poster
Automatically fills the post content - you just click Post
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
print("  🌙 LINKEDIN AUTO-FILL - RAMADAN POST")
print("=" * 70)
print("\n  I will fill the content automatically.")
print("  You just login, review, and click 'Post'!")
print("=" * 70)

with sync_playwright() as p:
    # Launch browser
    print("\n[1/6] Launching browser...")
    browser = p.chromium.launch(headless=False, slow_mo=100)
    
    context = browser.new_context(
        viewport={'width': 1400, 'height': 900},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    )
    
    page = context.new_page()
    
    # Go to LinkedIn
    print("[2/6] Opening LinkedIn...")
    page.goto('https://www.linkedin.com/feed/', timeout=60000)
    
    # Wait for page load
    page.wait_for_timeout(8000)
    
    # Check if login needed
    if 'login' in page.url or 'checkpoint' in page.url:
        print("\n" + "=" * 70)
        print("  [INFO] Please login to LinkedIn")
        print("=" * 70)
        print("\n  ⏰ Waiting up to 5 minutes for you to login...\n")
        
        # Wait for navigation away from login page (up to 5 minutes)
        start_time = time.time()
        timeout = 300  # 5 minutes
        
        while time.time() - start_time < timeout:
            if 'feed' in page.url:
                print("  ✓ Login detected!")
                break
            time.sleep(2)
            elapsed = int(time.time() - start_time)
            if elapsed % 30 == 0:
                print(f"  ⏱️  Waiting... {elapsed}s / {timeout}s")
        
        page.wait_for_timeout(3000)
    
    # Click "Start a post"
    print("\n[3/6] Opening post composer...")
    
    clicked = False
    selectors = [
        'button[aria-label="Start a post"]',
        '.share-box-feed-entry__trigger',
        'button:has-text("Start a post")'
    ]
    
    for selector in selectors:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=5000):
                btn.click()
                print(f"  ✓ Clicked 'Start a post'")
                clicked = True
                break
        except:
            continue
    
    if not clicked:
        print("  ⚠️  Please click 'Start a post' manually")
    
    page.wait_for_timeout(4000)
    
    # Fill the content
    print("\n[4/6] Filling post content...")
    
    # Try different editor selectors
    editors = [
        'div.ProseMirror',
        'div[contenteditable="true"]',
        'div[aria-label="What do you want to talk about?"]',
        'textarea[aria-label="What do you want to talk about?"]',
        'textarea'
    ]
    
    filled = False
    for selector in editors:
        try:
            editor = page.locator(selector).first
            if editor.is_visible(timeout=3000):
                editor.click()
                page.wait_for_timeout(500)
                
                # Fill content
                editor.fill(RAMADAN_POST)
                print(f"  ✓ Content filled automatically!")
                filled = True
                break
        except Exception as e:
            continue
    
    if not filled:
        print("  ⚠️  Could not auto-fill. Trying alternative method...")
        
        # Alternative: Use keyboard to paste from clipboard
        import pyperclip
        pyperclip.copy(RAMADAN_POST)
        
        try:
            editor = page.locator('div[contenteditable="true"]').first
            if editor.is_visible(timeout=3000):
                editor.click()
                page.wait_for_timeout(500)
                page.keyboard.press('Control+v')
                print("  ✓ Content pasted using keyboard shortcut")
                filled = True
        except:
            print("  ⚠️  Please paste content manually (Ctrl+V)")
    
    page.wait_for_timeout(3000)
    
    # Verify content is there
    print("\n[5/6] Verifying content...")
    try:
        # Check if Post button is enabled
        post_btn = page.locator('button:has-text("Post")').last
        if post_btn.is_enabled(timeout=5000):
            print("  ✓ Post button is enabled - content is ready!")
        else:
            print("  ⚠️  Post button not ready yet")
    except:
        print("  ⚠️  Please verify content manually")
    
    # Keep browser open
    print("\n[6/6] Browser ready for review...")
    print("\n" + "=" * 70)
    print("  ✅ POST IS READY!")
    print("=" * 70)
    print("\n  ✓ LinkedIn is open")
    print("  ✓ Post composer is open")
    if filled:
        print("  ✓ Content is FILLED - ready to review")
    print("\n  👉 YOUR ACTION:")
    print("     1. Review the content in the browser")
    print("     2. Click the blue 'Post' button")
    print("\n  ⏰ Browser stays open for 5 minutes (300 seconds)")
    print("=" * 70)
    
    # Keep browser open for 5 minutes with countdown
    for remaining in range(300, 0, -10):
        if remaining % 60 == 0:
            mins = remaining // 60
            print(f"  ⏱️  {mins} minute(s) remaining...")
        time.sleep(10)
    
    browser.close()
    
    print("\n" + "=" * 70)
    print("  Session ended")
    print("=" * 70)
    print("\n  If you need more time, run:")
    print("  python linkedin_autofill_post.py")
    print("\n🌙 Ramadan Mubarak!")

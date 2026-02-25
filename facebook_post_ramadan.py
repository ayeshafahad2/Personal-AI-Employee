#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook Auto-Poster - Ramadan Post
Opens Facebook and fills the same content as LinkedIn
"""

import sys
import codecs
import time

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from playwright.sync_api import sync_playwright

# Ramadan post content (same as LinkedIn)
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
print("  📘 FACEBOOK AUTO-POSTER - RAMADAN MESSAGE")
print("=" * 70)
print("\n  I'll open Facebook and fill the content.")
print("  You just click 'Post'!")
print("=" * 70)

with sync_playwright() as p:
    # Launch browser
    print("\n🚀 Launching browser...")
    browser = p.chromium.launch(headless=False, slow_mo=100)
    
    context = browser.new_context(
        viewport={'width': 1400, 'height': 900},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    )
    
    page = context.new_page()
    
    # Go to Facebook
    print("📍 Opening Facebook...")
    page.goto('https://www.facebook.com/', timeout=60000)
    page.wait_for_timeout(8000)
    
    # Check if login needed
    if 'login' in page.url:
        print("\n" + "=" * 70)
        print("  ⏰ Please login to Facebook")
        print("=" * 70)
        print("\n  Waiting up to 5 minutes for login...\n")
        
        start = time.time()
        while time.time() - start < 300:
            if 'facebook.com' in page.url and 'login' not in page.url:
                print("  ✓ Login detected!")
                break
            time.sleep(2)
            elapsed = int(time.time() - start)
            if elapsed % 30 == 0:
                print(f"  ⏱️  {elapsed}s elapsed...")
        
        page.wait_for_timeout(3000)
    
    # Click on "What's on your mind?" post box
    print("\n✍️  Opening post composer...")
    
    clicked = False
    selectors = [
        '[data-testid="create_post"]',
        'div[role="button"]:has-text("What\'s on your mind?")',
        'div[role="button"]:has-text("What is on your mind?")',
        '.x1n2onr6'
    ]
    
    for selector in selectors:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=5000):
                btn.click()
                print(f"  ✓ Opened post composer")
                clicked = True
                break
        except:
            continue
    
    if not clicked:
        print("  ⚠️  Please click 'What's on your mind?' manually")
    
    page.wait_for_timeout(4000)
    
    # Find the text editor and fill content
    print("\n📝 Filling post content...")
    
    # Try different editor selectors
    editors = [
        'div[contenteditable="true"][data-contents="true"]',
        'div[contenteditable="true"]',
        'textarea',
        'div[aria-label="What\'s on your mind?"]',
        'span[data-offset-key]'
    ]
    
    filled = False
    for selector in editors:
        try:
            editor = page.locator(selector).first
            if editor.is_visible(timeout=5000):
                editor.click()
                page.wait_for_timeout(500)
                
                # Try to fill content
                try:
                    editor.fill(RAMADAN_POST)
                    print(f"  ✓ Content filled automatically!")
                    filled = True
                    break
                except:
                    # If fill doesn't work, try keyboard paste
                    import pyperclip
                    pyperclip.copy(RAMADAN_POST)
                    page.keyboard.press('Control+v')
                    print(f"  ✓ Content pasted via keyboard!")
                    filled = True
                    break
        except Exception as e:
            continue
    
    if not filled:
        print("  ⚠️  Auto-fill didn't work. Copying to clipboard...")
        import pyperclip
        pyperclip.copy(RAMADAN_POST)
        print("  ✓ Content copied to clipboard - please paste manually (Ctrl+V)")
    
    page.wait_for_timeout(3000)
    
    # Check if Post button is available
    print("\n🔍 Checking post status...")
    try:
        post_btn = page.locator('button:has-text("Post")').last
        if post_btn.is_enabled(timeout=5000):
            print("  ✓ Post button is READY!")
        else:
            print("  ⚠️  Post button not ready yet")
    except:
        pass
    
    print("\n" + "=" * 70)
    print("  ✅ FACEBOOK POST READY!")
    print("=" * 70)
    print("\n  ✓ Facebook is open")
    print("  ✓ Post composer is open")
    if filled:
        print("  ✓ Content is FILLED - same as LinkedIn post")
    print("\n  👉 YOUR ACTION:")
    print("     1. Review the content")
    print("     2. Click blue 'Post' button")
    print("\n  ⏰ Browser stays open for 5 minutes (300 seconds)")
    print("=" * 70)
    
    # Keep browser open for 5 minutes
    for i in range(300, 0, -10):
        if i % 60 == 0:
            print(f"  ⏱️  {i//60} minute(s) remaining...")
        time.sleep(10)
    
    browser.close()
    
    print("\n" + "=" * 70)
    print("  Session ended")
    print("=" * 70)
    print("\n🌙 Ramadan Mubarak!")

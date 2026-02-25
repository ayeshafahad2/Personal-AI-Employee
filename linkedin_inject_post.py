#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Auto-Fill with JavaScript Injection
Directly injects content into LinkedIn editor
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
print("  🌙 AUTO-FILLING LINKEDIN POST")
print("  You just click 'Post' - I'll do the rest!")
print("=" * 70)

with sync_playwright() as p:
    print("\n🚀 Launching browser...")
    browser = p.chromium.launch(headless=False)
    
    context = browser.new_context(viewport={'width': 1400, 'height': 900})
    page = context.new_page()
    
    print("📍 Opening LinkedIn...")
    page.goto('https://www.linkedin.com/feed/', timeout=60000)
    page.wait_for_timeout(5000)
    
    # Wait for login
    if 'login' in page.url:
        print("\n⏰ Waiting for login (5 minutes max)...")
        print("   Please login in the browser window\n")
        start = time.time()
        while time.time() - start < 300:
            if 'feed' in page.url:
                print("   ✓ Logged in!")
                break
            time.sleep(2)
            if int(time.time() - start) % 30 == 0:
                print(f"   ⏱️  {int(time.time()-start)}s elapsed...")
    
    page.wait_for_timeout(3000)
    
    # Click Start a post
    print("\n✍️  Opening post composer...")
    try:
        page.click('button[aria-label="Start a post"]', timeout=10000)
        print("   ✓ Opened post composer")
        page.wait_for_timeout(3000)
    except:
        print("   ⚠️  Please click 'Start a post' manually")
    
    # Use JavaScript to inject content
    print("\n📝 Injecting post content...")
    
    # Escape the post content for JavaScript
    escaped_post = RAMADAN_POST.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    
    # JavaScript to inject content into LinkedIn editor
    js_code = f"""
    () => {{
        // Find the editor
        const editor = document.querySelector('div.ProseMirror') || 
                      document.querySelector('div[contenteditable="true"]') ||
                      document.querySelector('textarea');
        
        if (editor) {{
            // Set the content
            editor.innerText = `{escaped_post}`;
            
            // Trigger input event
            const event = new InputEvent('input', {{ bubbles: true }});
            editor.dispatchEvent(event);
            
            return 'SUCCESS';
        }}
        return 'NOT_FOUND';
    }}
    """
    
    try:
        result = page.evaluate(js_code)
        if result == 'SUCCESS':
            print("   ✓ Content injected via JavaScript!")
        else:
            print("   ⚠️  Editor not found")
    except Exception as e:
        print(f"   Error: {e}")
        print("   Trying alternative method...")
        
        # Fallback: Use fill on textarea
        try:
            textarea = page.locator('textarea').first
            if textarea.is_visible(timeout=5000):
                textarea.fill(RAMADAN_POST)
                print("   ✓ Content filled in textarea")
        except:
            print("   ⚠️  Manual paste may be needed")
    
    page.wait_for_timeout(3000)
    
    # Check status
    print("\n🔍 Checking post status...")
    try:
        post_btn = page.locator('button:has-text("Post")').last
        if post_btn.is_enabled(timeout=5000):
            print("   ✓ Post button is ENABLED!")
        else:
            print("   ⚠️  Post button not ready")
    except:
        pass
    
    print("\n" + "=" * 70)
    print("  ✅ READY FOR YOU TO POST!")
    print("=" * 70)
    print("\n  Browser is open with LinkedIn")
    print("  Post content should be filled in")
    print("\n  👉 YOUR ACTION:")
    print("     1. Review the content")
    print("     2. Click blue 'Post' button")
    print("\n  ⏰ Browser stays open for 5 minutes...")
    print("=" * 70)
    
    # Keep open for 5 minutes
    for i in range(300, 0, -10):
        if i % 60 == 0:
            print(f"  ⏱️  {i//60} min remaining...")
        time.sleep(10)
    
    browser.close()
    print("\n🌙 Ramadan Mubarak!")

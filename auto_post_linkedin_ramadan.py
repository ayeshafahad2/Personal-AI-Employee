#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Post to LinkedIn using Playwright
This will automatically post the Ramadan message to LinkedIn
"""

import sys
import codecs

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installing Playwright...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
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

In our hyper-connected world, Ramadan offers a unique pause—a chance to reset our priorities, purify our intentions, and reconnect with our core values.

Whether you're observing or simply supporting those who are, may this month bring:
🕊️ Peace to your heart
🤝 Unity to your community
💡 Clarity to your mind
🌟 Blessings to your life

Ramadan Mubarak to all who are celebrating! 🌙

#Ramadan #Ramadan2026 #SpiritualGrowth #Mindfulness #Community #Gratitude #SelfDiscipline #Reflection #BlessedMonth #RamadanKareem #PeaceAndUnity #DigitalWellbeing"""

print("=" * 70)
print("  LINKEDIN AUTO POSTER - RAMADAN MESSAGE")
print("=" * 70)

def post_to_linkedin():
    with sync_playwright() as p:
        # Launch browser
        print("\n[1/5] Launching browser...")
        browser = p.chromium.launch(headless=False, slow_mo=100)
        
        # Create new context
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = context.new_page()
        
        # Go to LinkedIn
        print("[2/5] Opening LinkedIn...")
        page.goto('https://www.linkedin.com/feed/', timeout=60000)
        
        # Wait for page to load
        page.wait_for_timeout(5000)
        
        # Check if logged in
        try:
            if 'login' in page.url:
                print("[!] You need to login to LinkedIn first")
                print("    Please login, then I'll continue posting...")
                # Wait for user to login
                page.wait_for_function("window.location.href.includes('feed')", timeout=120000)
                print("    Login detected! Continuing...")
        except:
            pass
        
        # Click on "Start a post"
        print("[3/5] Clicking 'Start a post'...")
        try:
            # Try different selectors for the post button
            selectors = [
                'button[aria-label="Start a post"]',
                'div.ipy2:has-text("Start a post")',
                'button:has-text("Start a post")',
                '.share-box-feed-entry__trigger'
            ]
            
            clicked = False
            for selector in selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible(timeout=3000):
                        element.click()
                        clicked = True
                        print(f"    ✓ Clicked using selector: {selector[:50]}")
                        break
                except:
                    continue
            
            if not clicked:
                print("    ⚠ Could not find 'Start a post' button automatically")
                print("    Please click 'Start a post' manually...")
                page.wait_for_timeout(3000)
                
        except Exception as e:
            print(f"    Error: {e}")
        
        # Wait for post dialog
        page.wait_for_timeout(3000)
        
        # Find the text editor and paste content
        print("[4/5] Pasting post content...")
        try:
            # Try different selectors for the text editor
            editors = [
                'div.ProseMirror',
                'div[contenteditable="true"]',
                'textarea[aria-label="What do you want to talk about?"]',
                'div[aria-label="What do you want to talk about?"]'
            ]
            
            for selector in editors:
                try:
                    editor = page.locator(selector).first
                    if editor.is_visible(timeout=2000):
                        editor.click()
                        page.wait_for_timeout(500)
                        editor.fill(RAMADAN_POST)
                        print(f"    ✓ Content pasted using selector: {selector[:50]}")
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"    Error pasting: {e}")
            print("    Please paste the content manually from the terminal")
        
        # Wait for Post button to be enabled
        page.wait_for_timeout(3000)
        
        # Click Post button
        print("[5/5] Looking for Post button...")
        try:
            post_button = page.locator('button:has-text("Post")').last
            if post_button.is_enabled(timeout=3000):
                print("    ✓ Post button found!")
                print("\n" + "=" * 70)
                print("  READY TO POST!")
                print("=" * 70)
                print("\n  The post content is in the editor.")
                print("  Click the 'Post' button to publish!")
                print("\n  Auto-clicking in 3 seconds...")
                page.wait_for_timeout(3000)
                post_button.click()
                print("\n✅ POST PUBLISHED!")
            else:
                print("    ⚠ Post button not enabled yet")
                print("    Please review and click 'Post' manually")
        except Exception as e:
            print(f"    Error: {e}")
            print("    Please click 'Post' manually")
        
        print("\n" + "=" * 70)
        print("  DONE!")
        print("=" * 70)
        print("\n  LinkedIn is open with your post ready to publish.")
        print("  Please click 'Post' if it hasn't been posted automatically.")
        
        # Keep browser open
        print("\n  Browser will stay open for 30 seconds...")
        page.wait_for_timeout(30000)
        
        browser.close()

if __name__ == "__main__":
    try:
        post_to_linkedin()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nManual posting instructions:")
        print("1. Go to https://www.linkedin.com/feed/")
        print("2. Click 'Start a post'")
        print("3. Copy and paste the Ramadan post content")
        print("4. Click 'Post'")

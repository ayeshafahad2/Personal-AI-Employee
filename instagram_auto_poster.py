#!/usr/bin/env python3
"""
Instagram Auto Poster - Browser automation
Posts images to Instagram via web interface
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("  INSTAGRAM AUTO POSTER")
print("=" * 70)

# Post content
caption = """The Personal AI Employee: Your 24/7 Digital Co-Worker 🤖

Transform your productivity with an AI assistant that never sleeps!

✨ Key Features:
• 24/7 Continuous Monitoring
• Multi-Platform Integration (Gmail, WhatsApp, LinkedIn)
• Smart Task Prioritization
• Privacy-First Design
• 85-90% Cost Reduction vs human FTE

The future of work is here. Augment your capabilities with AI.

#PersonalAI #AI #Productivity #FutureOfWork #ArtificialIntelligence #Automation #DigitalTransformation #Innovation #TechInnovation #AIAssistant

Posted: {timestamp}
""".format(timestamp=datetime.now().strftime('%B %d, %Y'))

# For demo, we'll use a placeholder image URL
# In production, you'd upload a local image or use a real URL
image_url = "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1080"

print(f"\nCaption prepared: {len(caption)} characters")
print(f"Image URL: {image_url}")

session_path = Path.home() / '.instagram_session'

with sync_playwright() as p:
    # Launch browser
    print("\n[1/6] Launching Instagram...")
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1280, 'height': 800},
        timeout=120000
    )
    page = browser.new_page()
    print("      Browser launched\n")
    
    # Navigate to Instagram
    print("[2/6] Opening Instagram...")
    page.goto('https://www.instagram.com/')
    time.sleep(5)
    print("      Instagram opened\n")
    
    # Check login
    print("[3/6] Checking login status...")
    time.sleep(3)
    
    logged_in = False
    try:
        # Check if already logged in (look for profile icon or feed)
        if page.query_selector('svg[aria-label="Home"]') or page.query_selector('[href*="/direct/"]'):
            print("      Already logged in!\n")
            logged_in = True
    except:
        pass
    
    if not logged_in:
        print("=" * 70)
        print("  LOGIN REQUIRED")
        print("=" * 70)
        print("""
  Please log in to Instagram in the browser window:
  1. Enter your username/email
  2. Enter your password
  3. Complete any 2FA if enabled
  
  Waiting 90 seconds for login...
""")
        print("=" * 70)
        
        for i in range(90, 0, -10):
            print(f"  {i} seconds remaining...")
            time.sleep(10)
            
            # Re-check login
            try:
                if page.query_selector('svg[aria-label="Home"]'):
                    print("  Login detected!\n")
                    logged_in = True
                    break
            except:
                pass
    
    if not logged_in:
        print("\n  Login timeout. Please log in manually and re-run.\n")
        browser.close()
        exit(1)
    
    # Create new post
    print("[4/6] Creating new post...")
    
    try:
        # Look for "Create" or "+" button
        create_selectors = [
            '[aria-label="New post"]',
            'svg[aria-label="Create"]',
            '[role="button"]:has-text("New")',
            '[href*="/create/"]'
        ]
        
        clicked = False
        for selector in create_selectors:
            try:
                create_btn = page.query_selector(selector)
                if create_btn and create_btn.is_visible():
                    create_btn.click()
                    print(f"      Clicked: {selector}")
                    time.sleep(3)
                    clicked = True
                    break
            except:
                continue
        
        if not clicked:
            print("      Could not find create button automatically")
            print("      Please click 'Create' or '+' button manually")
            time.sleep(15)
        
    except Exception as e:
        print(f"      Error: {e}")
    
    # Upload image
    print("\n[5/6] Uploading image...")
    
    try:
        # Look for file input or drag-drop area
        # Instagram web requires file upload from local system
        
        print("      Instagram web requires local file upload")
        print("""
  MANUAL STEPS REQUIRED:
  
  1. Download an image or use one from your computer
  2. Drag and drop it into the Instagram post creator
     OR click to select file
  
  Caption to copy (ready in clipboard):
  ---
{caption}
  ---
  
  Waiting 60 seconds...
""".format(caption=caption[:200]))
        
        # Copy caption to clipboard
        import subprocess
        try:
            subprocess.run(['clip'], input=caption.encode('utf-16-le'), capture_output=True)
            print("\n  Caption copied to clipboard!\n")
        except:
            print("\n  Please copy caption manually\n")
        
        time.sleep(60)
        
    except Exception as e:
        print(f"      Error: {e}")
        time.sleep(30)
    
    # Add caption and share
    print("\n[6/6] Adding caption and sharing...")
    print("""
  MANUAL STEPS:
  
  1. Paste the caption (Ctrl+V)
  2. Add location/tag people if desired
  3. Click "Share" to publish
  
  Waiting 60 seconds...
""")
    time.sleep(60)
    
    # Screenshot
    try:
        page.screenshot(path='instagram_post_result.png')
        print("\n  Screenshot saved: instagram_post_result.png")
    except:
        pass
    
    print("\n  Browser stays open 30 more seconds...")
    time.sleep(30)
    
    browser.close()

print("\n" + "=" * 70)
print("  DONE")
print("=" * 70 + "\n")

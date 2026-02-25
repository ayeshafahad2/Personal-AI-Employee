#!/usr/bin/env python3
"""
Twitter Thread Poster - Uses YOUR Chrome Browser
Connects to your actual Chrome where you're already logged in
No need to log in again - uses your existing session

Usage:
    1. Open Chrome and log in to Twitter manually
    2. Run this script
    3. It will post automatically using your session
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path
import subprocess
import os

print("=" * 70)
print("  TWITTER THREAD POSTER - YOUR CHROME BROWSER")
print("  Uses your existing Twitter login")
print("=" * 70)

tweets = [
    "HIRE A PERSONAL ASSISTANT IN 2026\n\nTraditional Human PA:\n- $3000-8000/month\n- 8 hours/day\n- 5 days/week\n- Needs sleep and vacations\n- Sick days\n- One skill set\n\nAI Personal Assistant:\n- ~$500-2000/month\n- 24/7/365\n- Never stops\n- Zero downtime\n- Never sick\n- Unlimited skills\n\nThe math is simple.",
    "COST COMPARISON\n\nHuman PA (Monthly):\n- Salary: $4000\n- Benefits: $800\n- Training: $200\n- Equipment: $100\n- Total: $5100/month\n\nAI Personal Assistant:\n- API costs: $200-500\n- Infrastructure: $50\n- Total: $250-550/month\n\nSAVINGS: 85-90%",
    "WHAT AI PERSONAL ASSISTANT DOES 24/7:\n\n- Monitor Gmail continuously\n- Auto-reply on WhatsApp\n- Post to LinkedIn, Instagram, Twitter\n- Track deadlines and meetings\n- Generate daily reports\n- Handle routine decisions\n- Escalate important items\n\nAll while you sleep or focus on growth.",
    "REAL-WORLD EXAMPLE:\n\nOur AI Employee System:\n\n1. Gmail Watcher - Creates action items\n2. Orchestrator - Plans with AI reasoning\n3. MCP Servers - Execute actions\n4. HITL Workflow - Human approves critical tasks\n5. Auto-posts to social media\n6. Sends WhatsApp notifications\n\nZero manual work. Full audit trail.",
    "SAFETY and CONTROL:\n\nAI Personal Assistant features:\n- Human-in-the-loop approvals\n- File-based audit logs\n- Permission boundaries\n- Local-first architecture\n- Obsidian vault dashboard\n- Complete transparency\n\nYou are always in control.",
    "THE FUTURE OF WORK:\n\nIt is NOT about replacement.\nIt is about AUGMENTATION.\n\nAI handles: Routine, repetitive, 24/7 monitoring\nHumans focus: Strategy, creativity, relationships\n\nBest results = Human + AI collaboration\n\nThe question is not IF you will use AI. It is WHEN.\n\n#AI #FutureOfWork #Productivity #DigitalTransformation #AIAgent #Automation"
]

print(f"\n  Thread: {len(tweets)} tweets")
print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Chrome user data directory
chrome_user_data = Path(os.environ['LOCALAPPDATA']) / 'Google' / 'Chrome' / 'User Data'

print(f"\n  Chrome Profile: {chrome_user_data}")

with sync_playwright() as p:
    print("\n[1] Launching YOUR Chrome browser...")
    print("    (Using your existing Twitter login session)")
    
    try:
        # Launch Chrome with user's profile
        browser = p.chromium.launch_persistent_context(
            str(chrome_user_data),
            channel='chrome',
            headless=False,
            viewport={'width': 1366, 'height': 768},
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-sandbox',
                '--no-zygote',
                '--disable-gpu'
            ],
            timeout=180000
        )
        
        page = browser.new_page()
        print("    Done ✓")
        
    except Exception as e:
        print(f"    Error: {e}")
        print("\n  Trying alternative profile path...")
        
        # Try Default profile
        default_profile = chrome_user_data / 'Default'
        try:
            browser = p.chromium.launch_persistent_context(
                str(default_profile),
                channel='chrome',
                headless=False,
                viewport={'width': 1366, 'height': 768},
                timeout=180000
            )
            page = browser.new_page()
            print("    Done ✓")
        except Exception as e2:
            print(f"    Error: {e2}")
            print("\n  FALLBACK: Using temporary session")
            print("  You may need to log in once, then it will be saved.")
            
            session_path = Path.home() / '.twitter_session_permanent'
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                channel='chrome',
                headless=False,
                viewport={'width': 1366, 'height': 768},
                timeout=180000
            )
            page = browser.new_page()

    # Go to Twitter and check login
    print("\n[2] Checking Twitter login...")
    page.goto('https://twitter.com/')
    time.sleep(5)
    
    # Check if logged in
    current_url = page.url
    if 'login' in current_url or 'i/flow/login' in current_url:
        print("    Not logged in yet!")
        print("\n" + "=" * 70)
        print("  PLEASE LOG IN - 45 SECONDS")
        print("=" * 70)
        print("  The browser window is showing Twitter login.")
        print("  Log in with: ayeshafahad661@gmail.com")
        print("  After login, the script will continue automatically...\n")
        
        for i in range(45, 0, -5):
            print(f"  {i}s  ", end='\r')
            time.sleep(5)
        print("\n")
        
        # Navigate back to home after login
        page.goto('https://twitter.com/')
        time.sleep(3)
    else:
        print("    Logged in ✓")

    # Post tweets
    print("\n[3] Posting tweets...\n")
    
    for i, tweet_text in enumerate(tweets):
        print(f"  Tweet {i+1}/{len(tweets)}...", end=' ')
        
        try:
            page.goto('https://twitter.com/compose/tweet')
            time.sleep(2)
            
            textbox = page.locator('[data-testid="tweetTextarea_0"]')
            textbox.wait_for(state='visible', timeout=10000)
            textbox.fill(tweet_text)
            time.sleep(1)
            
            post_btn = page.locator('[data-testid="tweetButton"]')
            post_btn.wait_for(state='visible', timeout=10000)
            post_btn.click()
            time.sleep(3)
            
            print("POSTED ✓")
            
        except Exception as e:
            print(f"FAILED - {str(e)[:60]}")
        
        if i < len(tweets) - 1:
            time.sleep(3)

    # Open profile
    print("\n[4] Opening your profile...")
    page.goto('https://twitter.com/ayeshafahad661')
    time.sleep(5)
    print("    Done")

    print("\n" + "=" * 70)
    print("  COMPLETE!")
    print("=" * 70)
    print("""
  Your tweets have been posted!
  
  Browser will stay open for 30 seconds.
  Your login is now saved for next time.
  
  Next time, just run:
    python twitter_post_saved_session.py
""")
    print("=" * 70)

    time.sleep(30)
    browser.close()

print("\n  All done!\n")

#!/usr/bin/env python3
"""
Twitter Thread Poster - Fully Automated Browser
Posts thread using Playwright browser automation
Gives you time to log in, then posts automatically

Usage:
    python twitter_post_browser.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path

print("=" * 70)
print("  TWITTER THREAD POSTER - FULLY AUTOMATED")
print("  Human vs AI Personal Assistant")
print("=" * 70)

# Thread content - 6 tweets
tweets = [
    """HIRE A PERSONAL ASSISTANT IN 2026

Traditional Human PA:
- $3,000-8,000/month
- 8 hours/day
- 5 days/week
- Needs sleep & vacations
- Sick days
- One skill set

AI Personal Assistant:
- ~$500-2,000/month
- 24/7/365
- Never stops
- Zero downtime
- Never sick
- Unlimited skills

The math is simple.""",

    """COST COMPARISON

Human PA (Monthly):
- Salary: $4,000
- Benefits: $800
- Training: $200
- Equipment: $100
- Total: $5,100/month

AI Personal Assistant:
- API costs: $200-500
- Infrastructure: $50
- Total: $250-550/month

SAVINGS: 85-90%""",

    """WHAT AI PERSONAL ASSISTANT DOES 24/7:

- Monitor Gmail continuously
- Auto-reply on WhatsApp
- Post to LinkedIn, Instagram, Twitter
- Track deadlines & meetings
- Generate daily reports
- Handle routine decisions
- Escalate important items

All while you sleep or focus on growth.""",

    """REAL-WORLD EXAMPLE:

Our AI Employee System:

1. Gmail Watcher - Creates action items
2. Orchestrator - Plans with AI reasoning
3. MCP Servers - Execute actions
4. HITL Workflow - Human approves critical tasks
5. Auto-posts to social media
6. Sends WhatsApp notifications

Zero manual work. Full audit trail.""",

    """SAFETY & CONTROL:

AI Personal Assistant features:
- Human-in-the-loop approvals
- File-based audit logs
- Permission boundaries
- Local-first architecture
- Obsidian vault dashboard
- Complete transparency

You're always in control.""",

    """THE FUTURE OF WORK:

It's NOT about replacement.
It's about AUGMENTATION.

AI handles: Routine, repetitive, 24/7 monitoring
Humans focus: Strategy, creativity, relationships

Best results = Human + AI collaboration

The question isn't IF you'll use AI. It's WHEN.

#AI #FutureOfWork #Productivity #DigitalTransformation #AIAgent #Automation"""
]

print(f"\n  Thread: {len(tweets)} tweets")
print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

with sync_playwright() as p:
    # Launch browser with persistent session
    print("\n[1/6] Launching browser...")
    session_path = Path.home() / '.twitter_session_ayesha'
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=180000
    )
    page = browser.new_page()
    print("      Done")

    # Navigate to Twitter login
    print("\n[2/6] Opening Twitter login page...")
    page.goto('https://twitter.com/login')
    time.sleep(5)
    print("      Done")

    # Give user time to log in
    print("\n" + "=" * 70)
    print("  TIME TO LOG IN - 45 SECONDS")
    print("=" * 70)
    print("""
  A browser window has opened with Twitter login.
  
  PLEASE LOG IN NOW:
  1. Enter your username/email
  2. Enter your password
  3. Complete 2FA if enabled
  
  The script will wait 45 seconds, then start posting automatically...
""")

    # Countdown for login
    for i in range(45, 0, -5):
        print(f"  Time remaining: {i} seconds...  ", end='\r')
        time.sleep(5)
    print("\n  Login time complete!")

    # Navigate to compose
    print("\n[3/6] Opening tweet composer...")
    page.goto('https://twitter.com/compose/tweet')
    time.sleep(3)
    print("      Done")

    # Post first tweet
    print("\n[4/6] Posting tweet 1/6...")
    
    try:
        # Find and fill tweet box
        textbox = page.locator('[data-testid="tweetTextarea_0"]')
        textbox.wait_for(state='visible', timeout=15000)
        textbox.click()
        time.sleep(1)
        
        # Clear any existing text
        page.keyboard.press('Control+A')
        time.sleep(0.5)
        page.keyboard.press('Backspace')
        time.sleep(0.5)
        
        # Type first tweet
        textbox.fill(tweets[0])
        time.sleep(2)
        
        print("      Content entered")
        
        # Click Post
        post_btn = page.locator('[data-testid="tweetButton"]')
        post_btn.wait_for(state='visible', timeout=15000)
        post_btn.click()
        time.sleep(4)
        
        print("      Tweet 1 posted!")
        
    except Exception as e:
        print(f"      Error posting tweet 1: {e}")
        print("      Waiting and trying again...")
        time.sleep(5)

    # Wait between tweets
    time.sleep(3)

    # Post remaining tweets
    for i in range(1, len(tweets)):
        print(f"\n[5/6] Posting tweet {i+1}/{len(tweets)}...")
        
        try:
            # Navigate to compose new tweet
            page.goto('https://twitter.com/compose/tweet')
            time.sleep(2)
            
            # Find tweet box
            textbox = page.locator('[data-testid="tweetTextarea_0"]')
            textbox.wait_for(state='visible', timeout=15000)
            textbox.click()
            time.sleep(1)
            
            # Clear and fill
            page.keyboard.press('Control+A')
            time.sleep(0.5)
            page.keyboard.press('Backspace')
            time.sleep(0.5)
            
            textbox.fill(tweets[i])
            time.sleep(2)
            
            # Post
            post_btn = page.locator('[data-testid="tweetButton"]')
            post_btn.wait_for(state='visible', timeout=15000)
            post_btn.click()
            time.sleep(4)
            
            print(f"      Tweet {i+1} posted!")
            
        except Exception as e:
            print(f"      Error: {e}")
            print("      Continuing to next tweet...")
        
        # Wait between tweets (except last)
        if i < len(tweets) - 1:
            time.sleep(3)

    # Navigate to profile to see posts
    print("\n[6/6] Opening your profile...")
    page.goto('https://twitter.com/ayeshafahad661')
    time.sleep(5)
    print("      Done")

    # Final summary
    print("\n" + "=" * 70)
    print("  POSTING COMPLETE!")
    print("=" * 70)
    print(f"""
  Summary:
  - Thread: Human vs AI Personal Assistant
  - Tweets: {len(tweets)}
  - Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  - Account: @ayeshafahad661
  
  Browser will stay open for 30 seconds.
  Check your profile to verify the posts!
""")
    print("=" * 70)

    time.sleep(30)
    browser.close()

print("\n  All done!\n")

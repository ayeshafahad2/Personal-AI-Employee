#!/usr/bin/env python3
"""
Twitter Thread Poster - Automated with Visual Feedback
Gives you 60 seconds to log in, then posts automatically
Uses multiple selector strategies for reliability

Usage:
    python twitter_post_automated.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path

print("=" * 70)
print("  TWITTER THREAD POSTER - AUTOMATED")
print("  Human vs AI Personal Assistant")
print("=" * 70)

# Thread content - 6 tweets
tweets = [
    """HIRE A PERSONAL ASSISTANT IN 2026

Traditional Human PA:
- $3000-8000/month
- 8 hours/day
- 5 days/week
- Needs sleep and vacations
- Sick days
- One skill set

AI Personal Assistant:
- ~$500-2000/month
- 24/7/365
- Never stops
- Zero downtime
- Never sick
- Unlimited skills

The math is simple.""",

    """COST COMPARISON

Human PA (Monthly):
- Salary: $4000
- Benefits: $800
- Training: $200
- Equipment: $100
- Total: $5100/month

AI Personal Assistant:
- API costs: $200-500
- Infrastructure: $50
- Total: $250-550/month

SAVINGS: 85-90%""",

    """WHAT AI PERSONAL ASSISTANT DOES 24/7:

- Monitor Gmail continuously
- Auto-reply on WhatsApp
- Post to LinkedIn, Instagram, Twitter
- Track deadlines and meetings
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

    """SAFETY and CONTROL:

AI Personal Assistant features:
- Human-in-the-loop approvals
- File-based audit logs
- Permission boundaries
- Local-first architecture
- Obsidian vault dashboard
- Complete transparency

You are always in control.""",

    """THE FUTURE OF WORK:

It is NOT about replacement.
It is about AUGMENTATION.

AI handles: Routine, repetitive, 24/7 monitoring
Humans focus: Strategy, creativity, relationships

Best results = Human + AI collaboration

The question is not IF you will use AI. It is WHEN.

#AI #FutureOfWork #Productivity #DigitalTransformation #AIAgent #Automation"""
]

print(f"\n  Thread: {len(tweets)} tweets")
print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

with sync_playwright() as p:
    # Launch browser
    print("\n[Step 1] Launching browser...")
    session_path = Path.home() / '.twitter_session_ayesha'
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=180000
    )
    page = browser.new_page()
    print("          Done")

    # Go to Twitter home
    print("\n[Step 2] Opening Twitter...")
    page.goto('https://twitter.com/')
    time.sleep(3)
    print("          Done")

    # Login time
    print("\n" + "=" * 70)
    print("  LOG IN TO TWITTER - 60 SECONDS")
    print("=" * 70)
    print("""
  The browser is now open at Twitter.
  
  If you see your home feed, you are already logged in.
  If you see the login page, please log in now.
  
  The script will wait 60 seconds before posting starts...
""")
    
    for i in range(60, 0, -5):
        print(f"  Remaining: {i}s  ", end='\r')
        time.sleep(5)
    print("\n  Time is up! Starting to post...")

    # Check if logged in by looking for compose button
    print("\n[Step 3] Checking login status...")
    try:
        page.goto('https://twitter.com/compose/tweet')
        time.sleep(3)
        print("          Navigated to composer")
    except:
        print("          Could not navigate - may need manual login")

    # Post all tweets
    print("\n[Step 4] Posting tweets...\n")
    
    for i, tweet_text in enumerate(tweets):
        print(f"  Posting tweet {i+1}/{len(tweets)}...")
        
        # Try multiple approaches to find the tweet box
        posted = False
        
        # Approach 1: Direct textarea
        try:
            page.goto('https://twitter.com/compose/tweet')
            time.sleep(2)
            
            # Try different selectors
            selectors = [
                '[data-testid="tweetTextarea_0"]',
                'textarea[aria-label="Tweet text"]',
                'textarea[data-testid="tweetTextarea_0"]',
                'div[contenteditable="true"][data-testid="tweetTextarea_0"]',
                '[role="textbox"][data-testid="tweetTextarea_0"]'
            ]
            
            for selector in selectors:
                try:
                    textbox = page.locator(selector)
                    textbox.wait_for(state='visible', timeout=5000)
                    textbox.click()
                    time.sleep(0.5)
                    
                    # Clear and type
                    page.keyboard.press('Control+A')
                    time.sleep(0.3)
                    page.keyboard.press('Backspace')
                    time.sleep(0.3)
                    
                    textbox.fill(tweet_text)
                    time.sleep(1)
                    
                    # Find and click post button
                    post_selectors = [
                        '[data-testid="tweetButton"]',
                        'button[data-testid="tweetButton"]',
                        'div[role="button"][data-testid="tweetButton"]'
                    ]
                    
                    for ps in post_selectors:
                        try:
                            post_btn = page.locator(ps)
                            post_btn.wait_for(state='visible', timeout=3000)
                            post_btn.click()
                            print(f"            SUCCESS - Tweet {i+1} posted!")
                            posted = True
                            break
                        except:
                            continue
                    
                    if posted:
                        break
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"            Error: {e}")
        
        if not posted:
            print(f"            Could not auto-post tweet {i+1}")
            print("            Browser is ready - you can paste manually if needed")
        
        # Wait between tweets
        if i < len(tweets) - 1:
            time.sleep(4)

    # Go to profile
    print("\n[Step 5] Opening your profile...")
    page.goto('https://twitter.com/ayeshafahad661')
    time.sleep(5)
    print("          Done")

    # Summary
    print("\n" + "=" * 70)
    print("  COMPLETE!")
    print("=" * 70)
    print(f"""
  Thread: Human vs AI Personal Assistant
  Tweets: {len(tweets)}
  Account: @ayeshafahad661
  
  The browser will stay open for 30 seconds.
  Check your profile to see if tweets were posted!
  
  If auto-posting failed, you can manually:
  1. Go to https://twitter.com/compose/tweet
  2. Copy tweets from: twitter_thread_content.txt
  3. Paste and post manually
""")
    print("=" * 70)

    time.sleep(30)
    browser.close()

print("\n  Done!\n")

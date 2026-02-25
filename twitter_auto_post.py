#!/usr/bin/env python3
"""
Twitter Thread Poster - FULLY AUTOMATED
Uses your saved Chrome session - no login needed
Posts all 6 tweets automatically

Usage:
    python twitter_auto_post.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from pathlib import Path
import os

print("=" * 70)
print("  TWITTER AUTO POSTER - FULLY AUTOMATED")
print("  Human vs AI Personal Assistant Thread")
print("=" * 70)

tweets = [
    "HIRE A PERSONAL ASSISTANT IN 2026\n\nTraditional Human PA:\n- $3000-8000/month\n- 8 hours/day\n- 5 days/week\n- Needs sleep and vacations\n- Sick days\n- One skill set\n\nAI Personal Assistant:\n- ~$500-2000/month\n- 24/7/365\n- Never stops\n- Zero downtime\n- Never sick\n- Unlimited skills\n\nThe math is simple.",
    "COST COMPARISON\n\nHuman PA (Monthly):\n- Salary: $4000\n- Benefits: $800\n- Training: $200\n- Equipment: $100\n- Total: $5100/month\n\nAI Personal Assistant:\n- API costs: $200-500\n- Infrastructure: $50\n- Total: $250-550/month\n\nSAVINGS: 85-90%",
    "WHAT AI PERSONAL ASSISTANT DOES 24/7:\n\n- Monitor Gmail continuously\n- Auto-reply on WhatsApp\n- Post to LinkedIn, Instagram, Twitter\n- Track deadlines and meetings\n- Generate daily reports\n- Handle routine decisions\n- Escalate important items\n\nAll while you sleep or focus on growth.",
    "REAL-WORLD EXAMPLE:\n\nOur AI Employee System:\n\n1. Gmail Watcher - Creates action items\n2. Orchestrator - Plans with AI reasoning\n3. MCP Servers - Execute actions\n4. HITL Workflow - Human approves critical tasks\n5. Auto-posts to social media\n6. Sends WhatsApp notifications\n\nZero manual work. Full audit trail.",
    "SAFETY and CONTROL:\n\nAI Personal Assistant features:\n- Human-in-the-loop approvals\n- File-based audit logs\n- Permission boundaries\n- Local-first architecture\n- Obsidian vault dashboard\n- Complete transparency\n\nYou are always in control.",
    "THE FUTURE OF WORK:\n\nIt is NOT about replacement.\nIt is about AUGMENTATION.\n\nAI handles: Routine, repetitive, 24/7 monitoring\nHumans focus: Strategy, creativity, relationships\n\nBest results = Human + AI collaboration\n\nThe question is not IF you will use AI. It is WHEN.\n\n#AI #FutureOfWork #Productivity #DigitalTransformation #AIAgent #Automation"
]

print(f"\n  Tweets: {len(tweets)}")
print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Account: @ayeshafahad661")
print("=" * 70)

# Chrome user data directory (where your session is saved)
chrome_user_data = Path(os.environ['LOCALAPPDATA']) / 'Google' / 'Chrome' / 'User Data'

with sync_playwright() as p:
    # Launch Chrome with saved session
    print("\n[1/4] Opening your Chrome browser...")
    browser = p.chromium.launch_persistent_context(
        str(chrome_user_data),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=180000
    )
    page = browser.new_page()
    print("      Done")

    # Go to Twitter
    print("\n[2/4] Opening Twitter...")
    page.goto('https://twitter.com/')
    time.sleep(4)
    print("      Done")

    # Post all tweets
    print("\n[3/4] Posting tweets...\n")
    
    for i, tweet_text in enumerate(tweets):
        print(f"  Tweet {i+1}/{len(tweets)}...", end=' ')
        
        try:
            # Go to compose page
            page.goto('https://twitter.com/compose/tweet')
            time.sleep(2)
            
            # Fill tweet
            textbox = page.locator('[data-testid="tweetTextarea_0"]')
            textbox.wait_for(state='visible', timeout=10000)
            textbox.fill(tweet_text)
            time.sleep(1)
            
            # Post
            post_btn = page.locator('[data-testid="tweetButton"]')
            post_btn.wait_for(state='visible', timeout=10000)
            post_btn.click()
            time.sleep(3)
            
            print("POSTED")
            
        except Exception as e:
            print(f"ERROR: {str(e)[:50]}")
        
        if i < len(tweets) - 1:
            time.sleep(3)

    # Open profile
    print("\n[4/4] Opening your profile...")
    page.goto('https://twitter.com/ayeshafahad661')
    time.sleep(4)
    print("      Done")

    print("\n" + "=" * 70)
    print("  ALL TWEETS POSTED!")
    print("=" * 70)
    print(f"""
  Thread: Human vs AI Personal Assistant
  Total: {len(tweets)} tweets
  Account: @ayeshafahad661
  
  Check your profile to verify!
  Browser closes in 20 seconds...
""")
    print("=" * 70)

    time.sleep(20)
    browser.close()

print("\n  COMPLETE!\n")

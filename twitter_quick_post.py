#!/usr/bin/env python3
"""
Twitter Quick Post - Cost Comparison Tweet
Fast and simple - posts in 10 seconds
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path
import os

print("=" * 60)
print("  TWITTER QUICK POST - Cost Comparison")
print("=" * 60)

# Main tweet - Cost comparison
tweet = """HIRE A PERSONAL ASSISTANT IN 2026

Human PA: $3000-8000/month
AI Assistant: $500-2000/month

Human: 8hrs/day, 5 days/week
AI: 24/7/365, never stops

SAVINGS: 85-90%

The math is simple.

#AI #FutureOfWork #Automation"""

chrome_data = Path(os.environ['LOCALAPPDATA']) / 'Google' / 'Chrome' / 'User Data'

with sync_playwright() as p:
    print("\n[1] Opening Chrome...")
    browser = p.chromium.launch_persistent_context(
        str(chrome_data),
        channel='chrome',
        headless=False,
        viewport={'width': 1280, 'height': 720},
        timeout=60000
    )
    page = browser.new_page()
    print("    Done")

    print("\n[2] Going to Twitter...")
    page.goto('https://twitter.com/compose/tweet')
    time.sleep(3)
    print("    Done")

    print("\n[3] Posting tweet...")
    try:
        textbox = page.locator('[data-testid="tweetTextarea_0"]')
        textbox.fill(tweet)
        time.sleep(1)
        
        post_btn = page.locator('[data-testid="tweetButton"]')
        post_btn.click()
        time.sleep(3)
        
        print("    POSTED!")
    except Exception as e:
        print(f"    Error: {e}")
        print("    Manual post may be needed")

    print("\n[4] Opening profile...")
    page.goto('https://twitter.com/ayeshafahad661')
    time.sleep(3)
    print("    Done")

    print("\n" + "=" * 60)
    print("  DONE! Check your profile for the tweet.")
    print("  Browser closes in 15 seconds...")
    print("=" * 60)

    time.sleep(15)
    browser.close()

print("\n  Complete!\n")

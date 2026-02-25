#!/usr/bin/env python3
"""
Twitter Post - SUPER FAST
No waits, direct posting
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path
import os

print("Posting to Twitter...")

tweet = """HIRE A PERSONAL ASSISTANT IN 2026

Human PA: $3000-8000/month
AI Assistant: $500-2000/month (85-90% savings!)

Human: 8hrs/day, 5 days/week
AI: 24/7/365

The math is simple.

#AI #FutureOfWork #Automation"""

chrome_data = Path(os.environ['LOCALAPPDATA']) / 'Google' / 'Chrome' / 'User Data'

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(str(chrome_data), channel='chrome', headless=False, viewport={'width': 1280, 'height': 720}, timeout=60000)
    page = browser.new_page()
    
    page.goto('https://twitter.com/compose/tweet')
    time.sleep(2)
    
    textbox = page.locator('[data-testid="tweetTextarea_0"]')
    textbox.fill(tweet)
    
    post_btn = page.locator('[data-testid="tweetButton"]')
    post_btn.click()
    time.sleep(2)
    
    page.goto('https://twitter.com/ayeshafahad661')
    
    print("DONE! Tweet posted!")
    time.sleep(10)
    browser.close()

print("Complete!")

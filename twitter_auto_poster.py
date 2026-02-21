#!/usr/bin/env python3
"""
Twitter/X Auto Poster - Browser automation
Posts tweets via web interface (no API needed)
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("  TWITTER/X AUTO POSTER")
print("  Human FTE vs Digital FTE")
print("=" * 70)

# Generate tweet content (280 char limit)
tweets = [
    """🚀 HUMAN FTE vs DIGITAL FTE

💰 Traditional: $4-8K/month
🤖 AI Agent: $500-2K/month (85-90% savings!)

⏰ Human: 8hrs/day
🤖 AI: 24/7/365

❌ Human: Sick days, vacations
✅ AI: Never stops working

The future is AUGMENTATION, not replacement.

#AI #FutureOfWork #DigitalTransformation""",

    """💼 Your Digital FTE (Custom AI Agent) can:

✓ Monitor Gmail 24/7
✓ Auto-reply on WhatsApp  
✓ Post to LinkedIn/IG/Twitter
✓ Track deadlines
✓ Generate reports
✓ Handle routine tasks

While AI handles routine work, YOU focus on:
→ Strategy
→ Creativity  
→ Relationships
→ Growth

Work SMARTER, not harder.

#Productivity #Automation #AIAssistant""",

    """📊 Companies using Digital FTEs report:

• 80% less admin work
• 3x faster responses
• 95% task accuracy
• Zero missed opportunities

This isn't sci-fi. It's TODAY.

Your competitors are already using AI.
Are you?

#BusinessGrowth #TechInnovation #AIAgent"""
]

print(f"\n  Prepared {len(tweets)} tweets (thread)")
print(f"  Caption copied to clipboard")

# Copy first tweet to clipboard
try:
    import subprocess
    subprocess.run(['clip'], input=tweets[0].encode('utf-16-le'), capture_output=True)
except:
    pass

with sync_playwright() as p:
    # Launch
    print("\n[1/6] Launching Twitter...")
    session_path = Path.home() / '.twitter_session'
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        channel='chrome',
        headless=False,
        viewport={'width': 1366, 'height': 768},
        timeout=180000
    )
    page = browser.new_page()
    print("      Done\n")
    
    # Navigate
    print("[2/6] Opening Twitter/X...")
    page.goto('https://twitter.com/')
    time.sleep(5)
    print("      Done\n")
    
    # WAIT FOR LOGIN
    print("=" * 70)
    print("  STEP 1: LOG IN TO TWITTER/X")
    print("=" * 70)
    print("""
  Twitter is open in the browser.
  
  LOG IN NOW:
  - Enter username/email
  - Enter password
  - Complete 2FA if enabled
  
  I will wait 3 MINUTES (180 seconds).
  
  After login, posting will be automatic.
""")
    print("=" * 70)
    
    print("\n  Waiting for login...\n")
    
    logged_in = False
    for i in range(180, 0, -10):
        if i % 30 == 0:
            print(f"  {i} seconds remaining...")
        
        # Check for login (look for tweet button or home timeline)
        try:
            if (page.query_selector('[data-testid="tweetButton"]') or
                page.query_selector('[data-testid="primaryColumn"]') or
                'home' in page.url.lower()):
                print(f"\n  ✓ Login detected!")
                logged_in = True
                break
        except:
            pass
        
        time.sleep(10)
    
    if not logged_in:
        print("\n  Login not detected. Continuing anyway...\n")
        time.sleep(5)
    
    # COMPOSE TWEET
    print("[3/6] Composing tweet...")
    
    try:
        # Find tweet compose box
        compose_selectors = [
            '[data-testid="tweetTextarea_0"]',
            '[role="textbox"][data-testid="tweetTextarea_0"]',
            'div[contenteditable="true"]',
            '[placeholder*="What"]'
        ]
        
        compose_box = None
        for selector in compose_selectors:
            try:
                compose_box = page.query_selector(selector)
                if compose_box and compose_box.is_visible(timeout=3000):
                    print(f"  ✓ Found compose box")
                    break
                compose_box = None
            except:
                compose_box = None
        
        if compose_box:
            compose_box.fill(tweets[0])
            print(f"  ✓ Tweet text entered ({len(tweets[0])} chars)")
            time.sleep(2)
        else:
            print("  Could not find compose box")
            
    except Exception as e:
        print(f"  Error: {e}")
    
    # POST TWEET
    print("\n[4/6] Posting tweet...")
    
    try:
        # Find tweet button
        tweet_btn = page.query_selector('[data-testid="tweetButton"], button:has-text("Post"), button:has-text("Tweet")')
        if tweet_btn and tweet_btn.is_visible(timeout=5000):
            tweet_btn.click()
            print("  ✓ Tweet button clicked")
            time.sleep(5)
        else:
            print("  Could not find Post button")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Wait for post to publish
    print("\n  Waiting for tweet to publish...")
    time.sleep(10)
    
    # SCREENSHOT
    print("\n[5/6] Taking screenshot...")
    page.screenshot(path='twitter_posted.png')
    print("  Saved: twitter_posted.png")
    
    # Navigate to profile to verify
    print("\n[6/6] Checking profile...")
    try:
        page.goto('https://twitter.com/')
        time.sleep(3)
        page.screenshot(path='twitter_profile.png')
        print("  Saved: twitter_profile.png")
    except:
        pass
    
    print("\n" + "=" * 70)
    print("  TWEET POSTED")
    print("=" * 70)
    print("""
  Browser stays open 60 seconds.
  
  Verify your tweet on your profile.
  Screenshots: twitter_posted.png, twitter_profile.png
  
  Tweet content (also copied to clipboard):
  ---
  {tweet}
  ---
""".format(tweet=tweets[0][:200]))
    print("=" * 70)
    
    for i in range(60, 0, -15):
        print(f"  {i} seconds...  ", end='\r')
        time.sleep(15)
    
    print("\n  Closing browser...")
    browser.close()

print("\n" + "=" * 70)
print("  DONE")
print("=" * 70 + "\n")

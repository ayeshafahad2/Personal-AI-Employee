#!/usr/bin/env python3
"""
Twitter Auto Poster - Clean Chrome Profile
Creates a fresh Chrome profile for Twitter automation
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path
import sys

print("=" * 70)
print("  TWITTER AUTO POSTER - CLEAN PROFILE")
print("=" * 70)

# Thread content
tweets = [
    """🤖 CLAUDE CODE IS TAKING OVER

While everyone was watching Qwen, DeepSeek, and other LLMs battle for API dominance, Anthropic's Claude Code quietly became the developer's #1 choice.

Here's why Claude Code is winning the AI coding war 👇

#ClaudeCode #AI #Coding""",

    """1/ REASONING DEPTH

Qwen: Fast responses, surface-level code
DeepSeek: Cheap, good for simple tasks
Claude Code: Thinks like a senior engineer

Claude doesn't just write code—it architects solutions, considers edge cases, and explains trade-offs.

Quality > Speed""",

    """2/ CONTEXT WINDOW DOMINANCE

Claude: 200K tokens (entire codebases)
Qwen: 32K-128K tokens
Others: 8K-32K tokens

You can feed Claude your ENTIRE repository.
It remembers EVERYTHING.

This changes EVERYTHING.

#AI #SoftwareEngineering""",

    """3/ HUMAN-IN-THE-LOOP DESIGN

Claude Code was built for COLLABORATION, not replacement.

- Asks clarifying questions
- Explains its reasoning
- Waits for approval before changes
- Learns your coding style

It's a co-pilot, not an autopilot.

#DeveloperExperience""",

    """4/ SAFETY & RELIABILITY

While other LLMs hallucinate APIs and invent functions, Claude Code:

- Verifies imports exist
- Checks dependencies
- Validates against your codebase
- Catches bugs before you run code

Production-ready code, every time.

#CodeQuality""",

    """5/ THE REALITY CHECK

Qwen: Cheaper per API call
DeepSeek: Budget-friendly alternative
Claude Code: Higher cost, BUT...

Cost per BUG FIXED:
- Qwen: $0.02 x 10 debugs = $0.20
- Claude: $0.10 x 1 debug = $0.10

Claude is actually CHEAPER.

#ROI #Development""",

    """6/ ECOSYSTEM INTEGRATION

Claude Code isn't just a chatbot—it's everywhere:

- VS Code extension
- CLI tool
- MCP servers
- Custom workflows
- API + Desktop app

It fits YOUR workflow, not the other way around.

#DevTools""",

    """7/ THE FUTURE

Qwen & others will compete on PRICE.
Claude Code competes on VALUE.

Developers don't want cheap code.
They want code that WORKS.

The AI coding war isn't about who's fastest.
It's about who's most TRUSTED.

#FutureOfCoding""",

    """FINAL THOUGHTS

I've used Qwen, DeepSeek, Copilot, and Claude Code extensively.

Claude Code isn't perfect, but it's the only AI that:
- Makes me a BETTER developer
- Teaches me new patterns
- Catches my mistakes
- Respects my codebase

That's why it's winning.

#AI #Programming"""
]

# Create fresh profile directory
profile_path = Path("E:\\Hackathon-0\\twitter_profile")
profile_path.mkdir(exist_ok=True)

print(f"\n  Using fresh Chrome profile: {profile_path}")
print("\n  INSTRUCTIONS:")
print("  1. Browser will open Twitter login page")
print("  2. You have 90 seconds to log in manually")
print("  3. Script will auto-detect login and post tweets")
print("\n  Starting in 5 seconds...")
time.sleep(5)

with sync_playwright() as p:
    print("\n[1/5] Launching fresh Chrome profile...")
    
    try:
        browser = p.chromium.launch_persistent_context(
            str(profile_path),
            channel='chrome',
            headless=False,
            viewport={'width': 1280, 'height': 800},
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ],
            ignore_default_args=['--enable-automation'],
            timeout=180000
        )
        print("      [OK]\n")
    except Exception as e:
        print(f"  [ERROR] {e}")
        print("\n  Try this instead:")
        print("  1. Open Chrome normally")
        print("  2. Go to twitter.com and log in")
        print("  3. Run: python twitter_post_helper.py")
        sys.exit(1)
    
    page = browser.new_page()
    
    # Disable automation detection
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US']});
    """)

    # Navigate to Twitter login
    print("[2/5] Opening Twitter login...")
    page.goto('https://twitter.com/login')
    time.sleep(3)
    print("      ✓ Done\n")

    # Wait for user to log in
    print("=" * 70)
    print("  LOG IN TO TWITTER")
    print("=" * 70)
    print("\n  Please log in using your Google account.")
    print("  You have 90 seconds...")
    
    for remaining in range(90, 0, -10):
        print(f"  Time remaining: {remaining}s")
        time.sleep(10)
        
        # Check if logged in by looking for compose button
        try:
            compose_btn = page.query_selector('[data-testid="SideNav_NewTweetBtn"]')
            if compose_btn:
                print("\n  [OK] Login detected!")
                break
        except:
            pass
    
    # Navigate to compose
    print("\n[3/5] Opening compose page...")
    page.goto('https://twitter.com/compose/tweet')
    time.sleep(3)
    print("      [OK]\n")

    # Enter tweets
    print("[4/5] Entering tweets...\n")
    
    time.sleep(2)
    
    # Enter first tweet
    try:
        textareas = page.query_selector_all('textarea[aria-label="Tweet text"]')
        if not textareas:
            textareas = page.query_selector_all('textarea')
        
        if textareas:
            textareas[0].fill('')
            time.sleep(0.5)
            textareas[0].type(tweets[0], delay=20)
            time.sleep(1)
            print("  [OK] Tweet 1/9 entered\n")
        else:
            print("  [ERROR] Could not find tweet input\n")
    except Exception as e:
        print(f"  [ERROR] Tweet 1: {e}\n")

    # Add and fill remaining tweets
    for i in range(1, len(tweets)):
        try:
            # Click "Add another post"
            add_buttons = page.query_selector_all('div[role="button"][aria-label="Add another post"]')
            if add_buttons:
                add_buttons[0].click()
                time.sleep(1)
                
                # Fill new textarea
                textareas = page.query_selector_all('textarea[aria-label="Tweet text"]')
                if len(textareas) > i:
                    textareas[i].fill('')
                    time.sleep(0.3)
                    textareas[i].type(tweets[i], delay=20)
                    time.sleep(0.5)
                    print(f"  [OK] Tweet {i+1}/9 entered")
        except Exception as e:
            print(f"  [ERROR] Tweet {i+1}: {e}")

    print("\n" + "=" * 70)
    print("  [5/5] ALL TWEETS ENTERED!")
    print("=" * 70)
    print("\n  ✓ Your thread is ready in the compose box")
    print("  ✓ Review the content")
    print("  ✓ Click 'Post' button to publish")
    print("\n  Browser stays open for 2 minutes...")
    print("=" * 70)
    
    # Keep browser open
    for remaining in range(120, 0, -10):
        print(f"  Browser closes in {remaining}s...")
        time.sleep(10)
    
    browser.close()

print("\n[OK] Done!")

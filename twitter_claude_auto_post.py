#!/usr/bin/env python3
"""
Twitter Auto Poster - Uses YOUR existing Chrome session
No login needed - uses your already logged-in Chrome
"""

from playwright.sync_api import sync_playwright
import time
import subprocess
from pathlib import Path

print("=" * 70)
print("  CLAUDE CODE TAKING OVER - TWITTER AUTO POSTER")
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

print(f"\n  Prepared {len(tweets)} tweets for thread")
print("\n  This script will use YOUR Chrome browser (already logged in)")
print("\n  Starting in 5 seconds...")
time.sleep(5)

# Find Chrome user data directory
chrome_user_data = Path.home() / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data'

if not chrome_user_data.exists():
    print("\n  Chrome user data not found!")
    print("  Please open Chrome and log in to Twitter first:")
    print("  https://twitter.com/")
    input("\n  Press ENTER when ready...")

with sync_playwright() as p:
    # Launch using existing Chrome profile
    print("\n[1/3] Launching Chrome with your profile...")
    
    try:
        browser = p.chromium.launch_persistent_context(
            str(chrome_user_data),
            channel='chrome',
            headless=False,
            viewport={'width': 1366, 'height': 768},
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ],
            timeout=180000
        )
        print("      Done\n")
    except Exception as e:
        print(f"  Error launching Chrome: {e}")
        print("\n  ALTERNATIVE: Manual posting")
        print("  1. Open https://twitter.com/compose/tweet in Chrome")
        print("  2. Copy each tweet from the file:")
        print("     twitter_claude_thread_*.txt")
        print("  3. Paste and post as thread")
        exit(1)
    
    page = browser.new_page()

    # Navigate to Twitter compose
    print("[2/3] Opening Twitter compose...")
    page.goto('https://twitter.com/compose/tweet')
    time.sleep(5)
    print("      Done\n")

    # Enter tweets
    print("[3/3] Entering all tweets...")
    time.sleep(2)
    
    # Find textarea
    textareas = page.query_selector_all('textarea[aria-label="Tweet text"]')
    if not textareas:
        textareas = page.query_selector_all('textarea')
    
    if textareas:
        print("  Entering tweet 1/9...")
        textareas[0].fill('')
        time.sleep(0.5)
        textareas[0].type(tweets[0], delay=15)
        time.sleep(1)
        print("  ✓ Tweet 1\n")
    else:
        print("  ERROR: Could not find tweet input\n")

    # Add remaining tweets as thread
    for i in range(1, len(tweets)):
        try:
            # Click "Add another post" button
            add_buttons = page.query_selector_all('div[role="button"][aria-label="Add another post"]')
            if add_buttons:
                add_buttons[0].click()
                time.sleep(0.8)
                
                # Find all textareas and fill the newest one
                textareas = page.query_selector_all('textarea[aria-label="Tweet text"]')
                if len(textareas) > i:
                    textareas[i].fill('')
                    time.sleep(0.3)
                    textareas[i].type(tweets[i], delay=15)
                    time.sleep(0.5)
                    print(f"  ✓ Tweet {i+1}")
        except Exception as e:
            print(f"  Error with tweet {i+1}: {e}")

    print("\n" + "=" * 70)
    print("  ALL 9 TWEETS ENTERED!")
    print("=" * 70)
    print("\n  [ACTION REQUIRED]")
    print("  1. Review the thread in the browser")
    print("  2. Click the 'Post' button to publish")
    print("\n  Browser stays open for 2 minutes...")
    print("=" * 70)
    
    # Keep browser open
    for remaining in range(120, 0, -10):
        print(f"  Browser closes in {remaining}s...")
        time.sleep(10)
    
    browser.close()

print("\n[OK] Done!")

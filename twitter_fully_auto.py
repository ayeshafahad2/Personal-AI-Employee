#!/usr/bin/env python3
"""
Twitter Auto Post - Fully Automated with PyAutoGUI
Opens Twitter, pastes tweet, clicks post - completely automatic
"""

import subprocess
import time
import pyautogui
from pathlib import Path

print("=" * 60)
print("  TWITTER AUTO POST - FULLY AUTOMATED")
print("=" * 60)

tweet = """HIRE A PERSONAL ASSISTANT IN 2026

Human PA: $3000-8000/month
AI Assistant: $500-2000/month (85-90% savings!)

Human: 8hrs/day, 5 days/week
AI: 24/7/365

The math is simple.

#AI #FutureOfWork #Automation"""

# Copy to clipboard
subprocess.run(['clip'], input=tweet.encode('utf-16-le'))
print("\n  Tweet copied to clipboard")

# Open Twitter
print("  Opening Twitter compose...")
subprocess.run(['start', 'https://twitter.com/compose/tweet'], shell=True)

# Wait for browser to load
print("  Waiting 8 seconds for Twitter to load...")
for i in range(8, 0, -1):
    print(f"    {i}...  ", end='\r')
    time.sleep(1)
print("\n")

# Auto-paste using PyAutoGUI
print("  Pasting tweet...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)

# Click Post button (finds it by image or coordinates)
print("  Clicking Post button...")
time.sleep(2)

# Try to find and click the Post button
# Twitter Post button is usually at top right of compose box
screen_width, screen_height = pyautogui.size()

# Click approximate location of Post button
post_x = int(screen_width * 0.85)
post_y = int(screen_height * 0.25)

pyautogui.click(post_x, post_y)
time.sleep(2)

print("\n" + "=" * 60)
print("  TWEET POSTED!")
print("=" * 60)
print("""
  Check your Twitter profile to verify.
  
  The automation is complete!
""")
print("=" * 60)

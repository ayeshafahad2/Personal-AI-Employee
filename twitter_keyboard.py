#!/usr/bin/env python3
"""
Twitter Auto Post - Keyboard Automation
Uses keyboard module to paste and post
"""

import subprocess
import time
import keyboard

print("=" * 60)
print("  TWITTER AUTO POST")
print("=" * 60)

tweet = """HIRE A PERSONAL ASSISTANT IN 2026

Human PA: $3000-8000/month
AI Assistant: $500-2000/month (85-90% savings!)

Human: 8hrs/day, 5 days/week
AI: 24/7/365

The math is simple.

#AI #FutureOfWork #Automation"""

subprocess.run(['clip'], input=tweet.encode('utf-16-le'))
print("\n  Tweet copied to clipboard")

print("  Opening Twitter...")
subprocess.run(['start', 'https://twitter.com/compose/tweet'], shell=True)

print("  Waiting 5 seconds...")
time.sleep(5)

print("  Pressing Ctrl+V to paste...")
keyboard.press_and_release('ctrl+v')
time.sleep(2)

print("  Pressing Enter to post...")
keyboard.press_and_release('ctrl+enter')

print("\n  DONE! Tweet posted!")
print("=" * 60)

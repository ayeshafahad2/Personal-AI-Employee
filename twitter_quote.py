#!/usr/bin/env python3
"""
Twitter Motivational Quote - Fully Automated
Posts an inspiring quote automatically
"""

import subprocess
import time
import keyboard

print("=" * 60)
print("  TWITTER MOTIVATIONAL QUOTE")
print("=" * 60)

quote = """The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset #AI"""

subprocess.run(['clip'], input=quote.encode('utf-16-le'))
print("\n  Quote copied to clipboard")

print("  Opening Twitter...")
subprocess.run(['start', 'https://twitter.com/compose/tweet'], shell=True)

print("  Waiting 5 seconds for Twitter to load...")
time.sleep(5)

print("  Pasting quote...")
keyboard.press_and_release('ctrl+v')
time.sleep(1)

print("  Posting...")
keyboard.press_and_release('ctrl+enter')

print("\n" + "=" * 60)
print("  QUOTE POSTED!")
print("=" * 60)
print("""
  Check your profile:
  https://twitter.com/ayeshafahad661
  
  The motivational quote is live!
""")
print("=" * 60)

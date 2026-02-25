#!/usr/bin/env python3
"""
Twitter Auto Post - Uses running Chrome via CDP
Connects to already open Chrome - no profile conflicts
"""

import subprocess
import time
from pathlib import Path
import os

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

# Copy to clipboard
subprocess.run(['clip'], input=tweet.encode('utf-16-le'))
print("\n  Tweet copied to clipboard!")

# Open Twitter
print("  Opening Twitter...")
subprocess.run(['start', 'https://twitter.com/compose/tweet'], shell=True)

print("\n" + "=" * 60)
print("  DONE!")
print("=" * 60)
print("""
  Twitter compose is open.
  Tweet content is in your clipboard.
  
  Just press Ctrl+V to paste and click Post!
  
  This is the fastest and most reliable method.
""")
print("=" * 60)

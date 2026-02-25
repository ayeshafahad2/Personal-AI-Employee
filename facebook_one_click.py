#!/usr/bin/env python3
"""
Facebook One-Click Post
Opens Facebook with pre-filled post - just click Post button
Free, no API setup needed
"""

import subprocess
from urllib.parse import quote

print("=" * 70)
print("  FACEBOOK ONE-CLICK POST")
print("=" * 70)

# Motivational post for Facebook
post = """The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset #Inspiration"""

print("\n  Post to Facebook:")
print("-" * 70)
print(post)
print("-" * 70)

# Facebook doesn't have pre-fill URL like Twitter, so we'll:
# 1. Copy to clipboard
# 2. Open Facebook
# 3. User pastes and posts

# Copy to clipboard
subprocess.run(['clip'], input=post.encode('utf-16-le'))

print("\n  Post copied to clipboard!")
print("  Opening Facebook...")

# Open Facebook
subprocess.Popen(['start', 'https://www.facebook.com/'], shell=True)

print("\n" + "=" * 70)
print("  READY TO POST!")
print("=" * 70)
print("""
  Facebook is opening.
  
  To post:
  1. Click "What's on your mind?" box
  2. Press Ctrl+V to paste (already copied!)
  3. Click "Post"
  
  Takes 5 seconds!
""")
print("=" * 70)
print("\n  Check your profile after posting: https://www.facebook.com/")
print("=" * 70)

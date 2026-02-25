#!/usr/bin/env python3
"""
Facebook ONE-CLICK POST - Guaranteed to Work
Opens Facebook, copies content, you paste and post
100% reliable - no automation issues
"""

import subprocess
import time

post = """The Future of Work is Here!

Human intelligence + AI tools = Unstoppable combination.

While AI handles routine tasks, humans excel at:
- Creative problem-solving
- Strategic thinking
- Building relationships
- Innovation

The question isn't IF you'll use AI.
It's WHEN you'll start.

#FutureOfWork #AI #Innovation #Productivity #DigitalTransformation"""

profile_url = "https://www.facebook.com/profile.php?id=61576154677449"

print("=" * 70)
print("  FACEBOOK ONE-CLICK POST")
print("  Guaranteed to Work!")
print("=" * 70)

print("\n  Content:")
print("-" * 70)
print(post)
print("-" * 70)

# Copy to clipboard
subprocess.run(['clip'], input=post.encode('utf-16-le'))
print("\n  Content copied to clipboard!")

# Open profile
print("  Opening your Facebook profile...")
subprocess.Popen(['start', profile_url], shell=True)

print("\n" + "=" * 70)
print("  READY TO POST!")
print("=" * 70)
print("""
  Facebook is opening. When you see your profile:
  
  1. Click "What's on your mind?" box
  2. Press Ctrl+V to paste (content is ready!)
  3. Click the blue "Post" button
  
  Takes 10 seconds!
""")
print("=" * 70)
print(f"\n  Profile: {profile_url}")
print("=" * 70)

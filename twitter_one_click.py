#!/usr/bin/env python3
"""
Twitter One-Click Post
Opens Twitter with tweet pre-filled - just click Post button
Free, no API credits needed
"""

import subprocess
from urllib.parse import quote

print("=" * 70)
print("  TWITTER ONE-CLICK POST")
print("=" * 70)

# Motivational tweet
tweet = "The best time to plant a tree was 20 years ago. The second best time is NOW. Don't wait for perfect conditions. Start where you are. Use what you have. Do what you can. Your future self will thank you. #Motivation #Success #GrowthMindset"

print("\n  Tweet to post:")
print("-" * 70)
print(tweet)
print("-" * 70)

# Create Twitter intent URL (pre-fills the tweet)
tweet_encoded = quote(tweet)
twitter_url = f"https://twitter.com/intent/tweet?text={tweet_encoded}"

print("\n  Opening Twitter with pre-filled tweet...")
subprocess.Popen(['start', twitter_url], shell=True)

print("\n" + "=" * 70)
print("  DONE!")
print("=" * 70)
print("""
  Twitter is opening with your tweet already written!
  
  Just click the "Post" button to publish.
  
  That's it - one click and you're done!
""")
print("=" * 70)
print("\n  Check profile after posting: https://twitter.com/ayeshafahad661")
print("=" * 70)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post Ramadan Message to LinkedIn - Direct API Call
Simple script to post blessed month message
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Load environment
load_dotenv()

print("=" * 70)
print("  RAMADAN LINKEDIN POST")
print("=" * 70)

# Get credentials
ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

if not ACCESS_TOKEN:
    print("ERROR: LINKEDIN_ACCESS_TOKEN not found in .env")
    exit(1)

print("\nCredentials loaded ✓")

# Post content - Professional Ramadan message
POST_TEXT = """🌙 Embracing the Blessed Month: A Time for Reflection & Renewal

As we welcome the holy month of Ramadan, millions around the world embark on a profound journey of spiritual growth, self-discipline, and community connection.

This sacred month teaches us powerful lessons that extend far beyond fasting:

✨ Mindful Awareness - Conscious eating and drinking reminds us to be intentional in all aspects of life

✨ Self-Discipline - The daily practice of restraint builds mental strength and willpower

✨ Empathy & Gratitude - Experiencing hunger fosters compassion for those less fortunate

✨ Community Bond - Breaking fast together strengthens family and community ties

✨ Digital Detox - A natural opportunity to reduce screen time and focus on what truly matters

In our hyper-connected world, Ramadan offers a unique pause—a chance to reset our priorities, purify our intentions, and reconnect with our core values.

Whether you're observing or simply supporting those who are, may this month bring:
🕊️ Peace to your heart
🤝 Unity to your community
💡 Clarity to your mind
🌟 Blessings to your life

Ramadan Mubarak to all who are celebrating! 🌙

#Ramadan #Ramadan2026 #SpiritualGrowth #Mindfulness #Community #Gratitude #SelfDiscipline #Reflection #BlessedMonth #RamadanKareem #PeaceAndUnity #DigitalWellbeing"""

# API endpoint
url = "https://api.linkedin.com/v2/ugcPosts"

# Headers
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0'
}

# First get person URN
print("\nFetching user profile...")
me_url = "https://api.linkedin.com/v2/me"
me_response = requests.get(me_url, headers=headers, timeout=10)

if me_response.status_code == 403:
    print("\n⚠️  Error: Access token doesn't have required permissions")
    print("\nTo fix this:")
    print("1. Run: python get_linkedin_token.py")
    print("2. Authorize with scopes: r_liteprofile w_member_social")
    print("3. Update .env with new access token")
    print("\nAlternatively, post manually:")
    print("\n" + "=" * 70)
    print("COPY THIS TEXT:")
    print("=" * 70)
    print(POST_TEXT)
    print("=" * 70)
    print("\nThen go to: https://www.linkedin.com/feed/")
    print("Paste and post manually")
    exit(0)

me_response.raise_for_status()
person_id = me_response.json().get('id')
print(f"User ID: {person_id}")

# Create post
payload = {
    "author": f"urn:li:person:{person_id}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": POST_TEXT
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

print("\nPosting to LinkedIn...")
response = requests.post(url, headers=headers, json=payload, timeout=30)

if response.status_code == 201:
    post_id = response.json().get('id', 'Unknown')
    print("\n✅ SUCCESS! Post published!")
    print(f"Post ID: {post_id}")
    print(f"URL: https://www.linkedin.com/feed/update/{post_id}")
    
    # Save to log
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": "LinkedIn",
        "post_id": post_id,
        "content": POST_TEXT,
        "status": "published",
        "topic": "Ramadan"
    }
    
    import json
    log_file = "ramadan_post_log.json"
    with open(log_file, 'w') as f:
        json.dump(log_entry, f, indent=2)
    print(f"\nLog saved to: {log_file}")
    
elif response.status_code == 403:
    print("\n❌ Error 403: Forbidden")
    print("The access token doesn't have permission to post")
    print("\nSolution:")
    print("1. Run: python get_linkedin_token.py")
    print("2. Make sure to authorize 'w_member_social' permission")
    print("3. Update .env with new token")
else:
    print(f"\n❌ Error {response.status_code}")
    print(f"Response: {response.text}")

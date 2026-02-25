#!/usr/bin/env python3
"""
Twitter API Thread Poster - Posts using OAuth 1.0a
Human vs AI Personal Assistant thread
"""

import os
import time
from datetime import datetime
from dotenv import load_dotenv
import requests
from requests_oauthlib import OAuth1

load_dotenv()

# Twitter API credentials
API_KEY = os.getenv('TWITTER_API_KEY', '')
API_SECRET = os.getenv('TWITTER_API_SECRET', '')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')

print("=" * 70)
print("  TWITTER API THREAD POSTER")
print("=" * 70)

# Thread content
tweets = [
    """HIRE A PERSONAL ASSISTANT IN 2026

Traditional Human PA:
- $3,000-8,000/month
- 8 hours/day
- 5 days/week
- Needs sleep & vacations
- Sick days
- One skill set

AI Personal Assistant:
- ~$500-2,000/month
- 24/7/365
- Never stops
- Zero downtime
- Never sick
- Unlimited skills

The math is simple.""",

    """COST COMPARISON

Human PA (Monthly):
- Salary: $4,000
- Benefits: $800
- Training: $200
- Equipment: $100
- Total: $5,100/month

AI Personal Assistant:
- API costs: $200-500
- Infrastructure: $50
- Total: $250-550/month

SAVINGS: 85-90%""",

    """WHAT AI PERSONAL ASSISTANT DOES 24/7:

- Monitor Gmail continuously
- Auto-reply on WhatsApp
- Post to LinkedIn, Instagram, Twitter
- Track deadlines & meetings
- Generate daily reports
- Handle routine decisions
- Escalate important items

All while you sleep or focus on growth.""",

    """REAL-WORLD EXAMPLE:

Our AI Employee System:

1. Gmail Watcher - Creates action items
2. Orchestrator - Plans with AI reasoning
3. MCP Servers - Execute actions
4. HITL Workflow - Human approves critical tasks
5. Auto-posts to social media
6. Sends WhatsApp notifications

Zero manual work. Full audit trail.""",

    """SAFETY & CONTROL:

AI Personal Assistant features:
- Human-in-the-loop approvals
- File-based audit logs
- Permission boundaries
- Local-first architecture
- Obsidian vault dashboard
- Complete transparency

You're always in control.""",

    """THE FUTURE OF WORK:

It's NOT about replacement.
It's about AUGMENTATION.

AI handles: Routine, repetitive, 24/7 monitoring
Humans focus: Strategy, creativity, relationships

Best results = Human + AI collaboration

The question isn't IF you'll use AI. It's WHEN.

#AI #FutureOfWork #Productivity #DigitalTransformation #AIAgent #Automation"""
]

print(f"\n  Thread: {len(tweets)} tweets")
print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Check credentials
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    print("\n  ERROR: Missing Twitter credentials in .env")
    exit(1)

print("\n  Credentials: OK")

# OAuth 1.0a setup
oauth = OAuth1(API_KEY, client_secret=API_SECRET, 
               resource_owner_key=ACCESS_TOKEN, 
               resource_owner_secret=ACCESS_TOKEN_SECRET)

headers = {'Content-Type': 'application/json'}

# Get current user info
print("\n[1/4] Getting user info...")
response = requests.get('https://api.twitter.com/1.1/account/verify_credentials.json', auth=oauth)
if response.status_code == 200:
    user = response.json()
    screen_name = user['screen_name']
    print(f"  Logged in as: @{screen_name}")
else:
    print(f"  Error: {response.status_code} - {response.text}")
    exit(1)

# Post tweet function
def post_tweet(text, reply_to=None):
    """Post a tweet using Twitter API v2 with OAuth 1.0a"""
    url = "https://api.twitter.com/2/tweets"
    
    payload = {"text": text}
    if reply_to:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to}
    
    response = requests.post(url, auth=oauth, headers=headers, json=payload)
    return response

# Post the thread
print(f"\n[2/4] Posting thread...")
tweet_ids = []

for i, tweet_text in enumerate(tweets):
    reply_to = tweet_ids[-1] if tweet_ids else None
    
    print(f"\n  Posting tweet {i+1}/{len(tweets)}...")
    
    response = post_tweet(tweet_text, reply_to)
    
    if response.status_code == 201:
        result = response.json()
        tweet_id = result['data']['id']
        tweet_ids.append(tweet_id)
        print(f"  Success! Tweet ID: {tweet_id}")
        
        # Small delay between tweets
        if i < len(tweets) - 1:
            time.sleep(1)
    else:
        print(f"  Error: {response.status_code}")
        print(f"  Response: {response.text}")
        break

# Summary
print("\n" + "=" * 70)
print("  POSTING SUMMARY")
print("=" * 70)

if tweet_ids:
    print(f"\n  Successfully posted {len(tweet_ids)} tweets!")
    print(f"\n  Thread URL:")
    print(f"  https://twitter.com/{screen_name}/status/{tweet_ids[0]}")
    print("\n  Tweet IDs:")
    for i, tid in enumerate(tweet_ids, 1):
        print(f"    {i}. {tid}")
    
    # Log to vault
    from pathlib import Path
    vault_path = Path('AI_Employee_Vault/Logs')
    vault_path.mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        'date': datetime.now().isoformat(),
        'type': 'twitter_thread',
        'topic': 'Human vs AI Personal Assistant',
        'tweets': len(tweet_ids),
        'thread_url': f"https://twitter.com/{screen_name}/status/{tweet_ids[0]}",
        'tweet_ids': tweet_ids
    }
    
    log_file = vault_path / f"twitter_{datetime.now().strftime('%Y-%m-%d')}.json"
    import json
    with open(log_file, 'w') as f:
        json.dump(log_entry, f, indent=2)
    
    print(f"\n  Logged to: {log_file}")
    
else:
    print("\n  No tweets posted.")

print("\n" + "=" * 70)

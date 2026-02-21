#!/usr/bin/env python3
"""
Direct LinkedIn Post - Bypasses the publisher class
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get credentials
access_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
client_id = os.getenv('LINKEDIN_CLIENT_ID', '77q075v0bg3v7e')
client_secret = os.getenv('LINKEDIN_CLIENT_SECRET', 'WPL_AP1.YOUR_LINKEDIN_SECRET_HERE')

print("=" * 70)
print("  LINKEDIN DIRECT POST")
print("=" * 70)

if not access_token or access_token == 'your_linkedin_access_token_here':
    print("\n[ERROR] No access token found!")
    print("Please complete OAuth first.")
    exit(1)

print(f"\nToken: {access_token[:30]}...")

# Post content
post_text = """
The Rise of AI Personal Assistants

AI personal assistants are transforming how we work in 2026:

✓ 24/7 availability - never sleeps
✓ Instant processing - thousands of tasks per second  
✓ Data-driven decisions - insights at scale
✓ Perfect consistency - 99.9% accuracy
✓ Cost-effective - fraction of human assistant cost
✓ Seamless integration - connects all your tools
✓ Infinite scalability - handle 10x work instantly

The future belongs to those who leverage AI to amplify their capabilities.

The question isn't "Will AI replace my assistant?"
The question is "How quickly can I integrate AI?"

#AI #Productivity #FutureOfWork #Automation #DigitalTransformation
"""

# First, get user info
print("\nGetting user info...")
headers = {
    'Authorization': f'Bearer {access_token}',
    'X-Restli-Protocol-Version': '2.0.0'
}

response = requests.get(
    'https://api.linkedin.com/v2/me',
    headers=headers,
    timeout=30
)

if response.status_code == 200:
    user_data = response.json()
    person_urn = user_data.get('id', '')
    print(f"User ID: {person_urn}")
    
    # Create post
    print("\nCreating post...")
    
    post_url = 'https://api.linkedin.com/v2/ugcPosts'
    
    payload = {
        "author": f"urn:li:person:{person_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text.strip()
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    post_response = requests.post(
        post_url,
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if post_response.status_code == 201:
        result = post_response.json()
        post_id = result.get('id', '')
        post_urn = result.get('urn', '')
        
        print("\n" + "=" * 70)
        print("  SUCCESS! POST PUBLISHED")
        print("=" * 70)
        print(f"\n  Post ID: {post_id}")
        print(f"  Post URN: {post_urn}")
        print(f"\n  View at: https://www.linkedin.com/feed/update/{post_urn}")
        print("=" * 70)
    else:
        print(f"\n[ERROR] {post_response.status_code}")
        print(f"Response: {post_response.text}")
        
        if post_response.status_code == 401:
            print("\nThe access token may still be activating.")
            print("Wait 5-10 minutes and try again.")
        elif post_response.status_code == 403:
            print("\nPermission denied. Check that your app has 'w_member_social' scope.")
            
else:
    print(f"\n[ERROR] {response.status_code}")
    print(f"Response: {response.text}")
    print("\nThe access token may need time to activate.")
    print("Wait 5-10 minutes, then try again.")

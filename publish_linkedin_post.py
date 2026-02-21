#!/usr/bin/env python3
"""
Simple LinkedIn Post Publisher - No emojis for Windows compatibility
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Get credentials
access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
client_id = os.getenv('LINKEDIN_CLIENT_ID')
client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')

if not access_token:
    print("ERROR: No LinkedIn access token found in .env")
    exit(1)

print("=" * 60)
print("LINKEDIN POST PUBLISHER")
print("=" * 60)

# Step 1: Get person URN
print("\nStep 1: Getting your LinkedIn profile info...")
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0'
}

try:
    response = requests.get(
        "https://api.linkedin.com/v2/me",
        headers=headers,
        timeout=30
    )
    
    if response.status_code == 200:
        person_data = response.json()
        person_urn = person_data.get('id', '')
        print(f"SUCCESS: Found profile ID: {person_urn}")
    else:
        print(f"ERROR: Failed to get profile. Status: {response.status_code}")
        print(f"Response: {response.text}")
        print("\nThis may be due to:")
        print("1. Token not yet activated (wait 5-10 minutes)")
        print("2. Missing permissions in LinkedIn app")
        print("3. Invalid token")
        exit(1)
        
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

# Step 2: Read post content
print("\nStep 2: Reading post content...")
post_file = "linkedin_post_best_personal_ai_employee_20260213_000304.txt"

try:
    with open(post_file, 'r', encoding='utf-8') as f:
        post_content = f.read().strip()
    print(f"SUCCESS: Read post from {post_file}")
    print(f"Post length: {len(post_content)} characters")
except FileNotFoundError:
    print(f"ERROR: Post file not found: {post_file}")
    exit(1)

# Step 3: Publish post
print("\nStep 3: Publishing to LinkedIn...")

payload = {
    "author": f"urn:li:person:{person_urn}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": post_content
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

try:
    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 201:
        result = response.json()
        post_id = result.get('id', 'Unknown')
        post_urn = result.get('urn', '')
        
        print("\n" + "=" * 60)
        print("SUCCESS! POST PUBLISHED TO LINKEDIN")
        print("=" * 60)
        print(f"Post ID: {post_id}")
        print(f"Post URN: {post_urn}")
        if post_urn:
            post_url = f"https://www.linkedin.com/feed/update/{post_urn}"
            print(f"Post URL: {post_url}")
        print("=" * 60)
    else:
        print(f"ERROR: Failed to publish. Status: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"ERROR: {e}")

print("\nDone.")

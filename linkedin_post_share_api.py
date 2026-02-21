#!/usr/bin/env python3
"""
LinkedIn Post Publisher - Using Share API (alternative approach)
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')

if not access_token:
    print("ERROR: No access token found")
    exit(1)

print("=" * 70)
print("LINKEDIN POST PUBLISHER - Share API")
print("=" * 70)

# Read post content
post_file = "linkedin_post_best_personal_ai_employee_20260213_000304.txt"

try:
    with open(post_file, 'r', encoding='utf-8') as f:
        post_content = f.read().strip()
    print(f"\nPost loaded: {len(post_content)} characters")
except FileNotFoundError:
    print(f"ERROR: Post file not found: {post_file}")
    exit(1)

# Try different API endpoints
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0'
}

# Method 1: Try person endpoint with different version
print("\nMethod 1: Trying /me endpoint...")
response = requests.get(
    "https://api.linkedin.com/v2/me?projection=(id,firstName,lastName)",
    headers=headers,
    timeout=30
)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    person_data = response.json()
    person_urn = person_data.get('id', '')
    print(f"Profile ID: {person_urn}")
    
    # Try posting with UGC Posts API
    print("\nPublishing via UGC Posts API...")
    
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
    
    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    print(f"Publish Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        post_id = result.get('id', '')
        post_urn = result.get('urn', '')
        print(f"\nSUCCESS! Post ID: {post_id}")
        if post_urn:
            print(f"Post URL: https://www.linkedin.com/feed/update/{post_urn}")
    else:
        print(f"Error: {response.text}")
        
elif response.status_code == 403:
    print("403 Forbidden - App permissions issue")
    print("\nThis means the LinkedIn app needs approval for w_member_social scope.")
    print("\nTo fix this:")
    print("1. Go to https://www.linkedin.com/developers/apps/")
    print("2. Select your app")
    print("3. Go to Settings tab")
    print("4. Add your LinkedIn account as a Test User")
    print("5. Wait 5 minutes, then re-authorize")
    print("\nOR submit your app for LinkedIn review (takes 1-3 business days)")
else:
    print(f"Error: {response.status_code}")
    print(f"Response: {response.text}")

print("\nDone.")

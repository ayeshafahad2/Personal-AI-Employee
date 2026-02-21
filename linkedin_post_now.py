#!/usr/bin/env python3
"""
LinkedIn Post Publisher - Direct API call
"""

import os
import webbrowser
import urllib.parse
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Get credentials from .env
CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID', '77q075v0bg3v7e')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:3000/callback')

print("=" * 70)
print("LINKEDIN POST PUBLISHER")
print("=" * 70)

# Step 1: Build authorization URL
auth_url = (
    f"https://www.linkedin.com/oauth/v2/authorization?"
    f"response_type=code&"
    f"client_id={CLIENT_ID}&"
    f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}&"
    f"scope={urllib.parse.quote('openid profile w_member_social email')}&"
    f"state=linkedin_post_auth"
)

print("\nStep 1: Authorize the application")
print("-" * 70)
print("\nOpening LinkedIn authorization page...")
print(f"URL: {auth_url}")

webbrowser.open(auth_url)

print("\nPlease authorize the app in your browser.")
print("After authorization, copy the 'code' parameter from the redirect URL.")
print("\nThe URL will look like: http://localhost:3000/callback?code=ABC123...")

auth_code = input("\nPaste the authorization code here: ").strip()

if not auth_code:
    print("ERROR: No code provided")
    exit(1)

print(f"\nCode received: {auth_code[:20]}...")

# Step 2: Exchange code for access token
print("\nStep 2: Exchanging code for access token...")
print("-" * 70)

token_url = "https://www.linkedin.com/oauth/v2/accessToken"

data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': REDIRECT_URI,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}

try:
    response = requests.post(token_url, data=data, timeout=30)
    response.raise_for_status()
    
    result = response.json()
    access_token = result.get('access_token', '')
    refresh_token = result.get('refresh_token', '')
    expires_in = result.get('expires_in', 0)
    
    if not access_token:
        print(f"ERROR: No access token in response")
        print(f"Response: {result}")
        exit(1)
    
    print(f"SUCCESS! Access token received")
    print(f"Expires in: {expires_in} seconds ({expires_in/3600:.1f} hours)")
    
    # Update .env file
    print("\nUpdating .env file...")
    env_file = '.env'
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Replace the access token
    import re
    content = re.sub(
        r'LINKEDIN_ACCESS_TOKEN=.*',
        f'LINKEDIN_ACCESS_TOKEN={access_token}',
        content
    )
    
    if 'your_linkedin_refresh_token_here' in content:
        content = content.replace('your_linkedin_refresh_token_here', refresh_token)
    else:
        content = re.sub(
            r'LINKEDIN_REFRESH_TOKEN=.*',
            f'LINKEDIN_REFRESH_TOKEN={refresh_token}',
            content
        )
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(".env file updated with new tokens!")
    
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

# Step 3: Get person URN
print("\nStep 3: Getting your LinkedIn profile info...")
print("-" * 70)

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

# Step 4: Read post content
print("\nStep 4: Reading post content...")
print("-" * 70)

post_file = "linkedin_post_best_personal_ai_employee_20260213_000304.txt"

try:
    with open(post_file, 'r', encoding='utf-8') as f:
        post_content = f.read().strip()
    print(f"SUCCESS: Read post from {post_file}")
    print(f"Post length: {len(post_content)} characters")
except FileNotFoundError:
    print(f"ERROR: Post file not found: {post_file}")
    exit(1)

# Step 5: Publish post
print("\nStep 5: Publishing to LinkedIn...")
print("-" * 70)

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
        
        print("\n" + "=" * 70)
        print("SUCCESS! POST PUBLISHED TO LINKEDIN")
        print("=" * 70)
        print(f"Post ID: {post_id}")
        print(f"Post URN: {post_urn}")
        if post_urn:
            post_url = f"https://www.linkedin.com/feed/update/{post_urn}"
            print(f"Post URL: {post_url}")
            print(f"\nView your post: {post_url}")
        print("=" * 70)
    else:
        print(f"ERROR: Failed to publish. Status: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"ERROR: {e}")

print("\nDone.")

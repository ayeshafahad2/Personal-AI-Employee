#!/usr/bin/env python3
"""
Quick LinkedIn Token Generator

This will open your browser to authorize the app and get your access token.
"""

import webbrowser
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("  LINKEDIN ACCESS TOKEN GENERATOR")
print("=" * 70)

# Get credentials from .env
client_id = os.getenv('LINKEDIN_CLIENT_ID', '7763qv2uyw7eao')
redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI', 'https://localhost')

# Build authorization URL
auth_url = (
    f"https://www.linkedin.com/oauth/v2/authorization?"
    f"response_type=code&"
    f"client_id={client_id}&"
    f"redirect_uri={redirect_uri}&"
    f"scope={urllib.parse.quote('r_liteprofile w_member_social')}&"
    f"state=linkedin_auth"
)

print("\nStep 1: Authorize the application")
print("-" * 70)
print("\nClick this URL (or it will open in your browser):")
print(auth_url)

# Open browser automatically
print("\nOpening browser...")
webbrowser.open(auth_url)

print("\n" + "=" * 70)
print("Step 2: Get Authorization Code")
print("-" * 70)
print("""
1. Sign in to LinkedIn if prompted
2. Click 'Allow' to authorize the application
3. You'll be redirected to a URL like:
   https://localhost?code=AQEDAbc123xyz...&state=linkedin_auth

4. Copy the 'code' parameter value (everything after 'code=' and before '&')
""")

auth_code = input("Paste the authorization code here: ").strip()

if not auth_code:
    print("ERROR: No code provided")
    exit(1)

print("\n" + "=" * 70)
print("Step 3: Exchange Code for Access Token")
print("-" * 70)

# Exchange code for token
import requests

client_secret = os.getenv('LINKEDIN_CLIENT_SECRET', 'WPL_AP1.YOUR_LINKEDIN_SECRET_HERE')

token_url = "https://www.linkedin.com/oauth/v2/accessToken"

data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret
}

try:
    response = requests.post(token_url, data=data, timeout=30)
    response.raise_for_status()
    
    result = response.json()
    
    access_token = result.get('access_token', '')
    refresh_token = result.get('refresh_token', '')
    expires_in = result.get('expires_in', 0)
    
    if access_token:
        print("\n✅ SUCCESS! Your LinkedIn credentials:\n")
        print(f"  Access Token:  {access_token}")
        print(f"  Refresh Token: {refresh_token}")
        print(f"  Expires In:    {expires_in} seconds ({expires_in/3600:.1f} hours)")
        
        # Update .env file
        print("\n" + "=" * 70)
        print("Step 4: Update .env file")
        print("-" * 70)
        
        env_file = '.env'
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace placeholder tokens
        if 'your_linkedin_access_token_here' in content:
            content = content.replace('your_linkedin_access_token_here', access_token)
        if 'your_linkedin_refresh_token_here' in content:
            content = content.replace('your_linkedin_refresh_token_here', refresh_token)
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print(f"\n✅ .env file updated with your tokens!")
        
        print("\n" + "=" * 70)
        print("Step 5: Test LinkedIn Posting")
        print("-" * 70)
        print("\nRun this command to test:")
        print("  python auto_post_manager.py --test")
        print("\nOr post a demo message:")
        print("  python auto_post_manager.py")
        
    else:
        print("❌ ERROR: No access token received")
        print(f"Response: {result}")
        
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP Error: {e}")
    try:
        error = e.response.json()
        print(f"Details: {error}")
    except:
        print(f"Response: {e.response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "=" * 70)

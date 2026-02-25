#!/usr/bin/env python3
"""
Gmail OAuth - Complete Setup
Run this after authorizing in browser
"""

import os
import sys
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('GMAIL_CLIENT_ID', '')
CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET', '')

print("=" * 70)
print("  GMAIL OAUTH - COMPLETE SETUP")
print("=" * 70)

if not CLIENT_ID or not CLIENT_SECRET:
    print("\n  ERROR: Gmail credentials not in .env")
    sys.exit(1)

print(f"\n  Client ID: {CLIENT_ID[:30]}...")
print(f"  Client Secret: {CLIENT_SECRET[:20]}...")

print("\n" + "=" * 70)
print("  INSTRUCTIONS")
print("=" * 70)
print("""
  1. Gmail OAuth page should be open in Chrome
  2. Click "Allow" or "Continue" to grant permissions
  3. You'll be redirected to a URL like:
     http://localhost/?code=ABC123...
  4. That URL won't load (that's OK!)
  5. COPY the entire URL from address bar
  6. Paste it below
""")

print("\n  Waiting for authorization...")
print("  (Browser should be open now)")

# Get callback URL
callback_url = input("\n  Paste the callback URL here: ").strip()

if not callback_url or 'code=' not in callback_url:
    print("\n  ERROR: No code in URL. Please paste full callback URL.")
    sys.exit(1)

# Extract code
parsed = urllib.parse.urlparse(callback_url)
params = urllib.parse.parse_qs(parsed.query)
auth_code = params.get('code', [None])[0]

if not auth_code:
    print("\n  ERROR: No authorization code found.")
    sys.exit(1)

print(f"\n  ✅ Got code: {auth_code[:30]}...")

# Exchange for token
print("\n" + "=" * 70)
print("  GETTING GMAIL TOKEN...")
print("=" * 70)

import requests

token_url = "https://oauth2.googleapis.com/token"
data = {
    'code': auth_code,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': 'http://localhost',
    'grant_type': 'authorization_code',
    'scope': 'https://www.googleapis.com/auth/gmail.send'
}

try:
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token', '')
        refresh_token = token_data.get('refresh_token', '')
        expires_in = token_data.get('expires_in', 0)
        
        print(f"\n  ✅ SUCCESS!")
        print(f"\n  Access Token: {access_token[:50]}...")
        print(f"  Expires: {expires_in} seconds")
        
        # Save token to file
        import json
        token_info = {
            'token': access_token,
            'refresh_token': refresh_token,
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scopes': ['https://www.googleapis.com/auth/gmail.send']
        }
        
        with open('token.json', 'w') as f:
            json.dump(token_info, f, indent=2)
        
        print(f"\n  ✅ Token saved to token.json!")
        print("\n  🎉 Gmail is now configured!")
        print("  Restart dashboard: python dashboard_server.py")
        
    else:
        print(f"\n  ❌ ERROR: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        
except Exception as e:
    print(f"\n  ❌ ERROR: {e}")

print("\n" + "=" * 70)

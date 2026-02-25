#!/usr/bin/env python3
"""
LinkedIn OAuth - Simple Version
Run this, then open browser, then wait for callback
"""

import os
import sys
import urllib.parse
import webbrowser
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID', '')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET', '')
REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:3000/callback')

print("=" * 70)
print("  LINKEDIN OAUTH - SIMPLE VERSION")
print("=" * 70)

if not CLIENT_ID or not CLIENT_SECRET:
    print("\n  ERROR: Credentials not in .env")
    sys.exit(1)

print(f"\n  Client ID: {CLIENT_ID}")
print(f"  Redirect: {REDIRECT_URI}")

# Build auth URL
auth_url = (
    "https://www.linkedin.com/oauth/v2/authorization?"
    f"response_type=code&"
    f"client_id={CLIENT_ID}&"
    f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}&"
    f"scope={urllib.parse.quote('openid profile email w_member_social')}"
)

print("\n" + "=" * 70)
print("  INSTRUCTIONS")
print("=" * 70)
print("""
  1. Copy the URL below
  2. Paste it in your browser (Chrome)
  3. Click "Allow" on LinkedIn
  4. You'll be redirected to a URL like:
     http://localhost:3000/callback?code=ABC123...
  5. COPY that entire URL
  6. Paste it below when prompted
""")

print("\n  AUTHORIZATION URL:")
print("  " + "=" * 60)
print(f"  {auth_url}")
print("  " + "=" * 60)

# Try to open browser
try:
    webbrowser.open(auth_url)
    print("\n  ✅ Browser opened! If not, copy URL above.")
except:
    print("\n  ⚠️  Browser didn't open. Copy URL above manually.")

print("\n" + "=" * 70)

# Get callback URL
callback_url = input("\n  Paste the callback URL here (or 'q' to quit): ").strip()

if callback_url.lower() == 'q':
    print("\n  Cancelled.")
    sys.exit(0)

if not callback_url or 'code=' not in callback_url:
    print("\n  ERROR: No code in URL. Please paste the full callback URL.")
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
print("  GETTING ACCESS TOKEN...")
print("=" * 70)

import requests

token_url = "https://www.linkedin.com/oauth/v2/accessToken"
data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': REDIRECT_URI,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
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
        
        # Update .env
        update = input("\n  Update .env with token? (y/n): ").strip().lower()
        
        if update == 'y':
            import re
            with open('.env', 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = re.sub(
                r'^LINKEDIN_ACCESS_TOKEN=.*$',
                f'LINKEDIN_ACCESS_TOKEN={access_token}',
                content,
                flags=re.MULTILINE
            )
            
            if refresh_token:
                content = re.sub(
                    r'^LINKEDIN_REFRESH_TOKEN=.*$',
                    f'LINKEDIN_REFRESH_TOKEN={refresh_token}',
                    content,
                    flags=re.MULTILINE
                )
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("\n  ✅ .env updated!")
            print("\n  🎉 LinkedIn is now configured!")
            print("  Restart dashboard: python dashboard_server.py")
        else:
            print(f"\n  Add manually to .env:")
            print(f"  LINKEDIN_ACCESS_TOKEN={access_token}")
    else:
        print(f"\n  ❌ ERROR: {response.status_code}")
        print(f"  Response: {response.text}")
        print("\n  Common issues:")
        print("  1. Redirect URI doesn't match LinkedIn app")
        print("  2. Authorization code expired (use it within 5 minutes)")
        print("  3. Invalid client credentials")
        
except Exception as e:
    print(f"\n  ❌ ERROR: {e}")

print("\n" + "=" * 70)

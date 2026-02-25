#!/usr/bin/env python3
"""
Twitter OAuth 1.0a Token Getter - Desktop App Version
Get user access tokens for posting tweets via API
Uses PIN-based OAuth (oob) for desktop applications

Usage:
    python get_twitter_token.py
"""

import os
import sys
from dotenv import load_dotenv
import webbrowser

load_dotenv()

# Twitter API credentials
API_KEY = os.getenv('TWITTER_API_KEY', '')
API_SECRET = os.getenv('TWITTER_API_SECRET', '')

if not API_KEY or not API_SECRET:
    print("ERROR: TWITTER_API_KEY or TWITTER_API_SECRET not set in .env")
    sys.exit(1)

print("=" * 70)
print("  TWITTER OAUTH 1.0a - GET ACCESS TOKEN (Desktop/PIN)")
print("=" * 70)

try:
    from requests_oauthlib import OAuth1Session
except ImportError:
    print("\n  Installing requests-oauthlib...")
    os.system('pip install requests-oauthlib')
    from requests_oauthlib import OAuth1Session

# Use 'oob' for desktop/PIN-based OAuth
callback_uri = 'oob'

print(f"\n  API Key: {API_KEY[:10]}...")
print(f"  API Secret: {API_SECRET[:10]}...")
print(f"  Type: Desktop App (PIN-based)")

print("\n" + "=" * 70)
print("  STEP 1: OPEN AUTHORIZATION URL")
print("=" * 70)

try:
    twitter = OAuth1Session(API_KEY, client_secret=API_SECRET, callback_uri=callback_uri)
    
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token"
    twitter.fetch_request_token(request_token_url)
    
    # Get authorization URL
    authorization_url = twitter.authorization_url(
        "https://api.twitter.com/oauth/authorize"
    )
    
    print("\n  Opening authorization URL in browser...")
    
    try:
        webbrowser.open(authorization_url)
    except:
        pass
    
except Exception as e:
    print(f"\n  Error: {e}")
    sys.exit(1)

print(f"""
  INSTRUCTIONS:
  
  1. A browser window should open with Twitter authorization page
  2. If not, copy and paste this URL into your browser:
  
     {authorization_url}
  
  3. Log in to Twitter if needed
  4. Click 'Authorize app'
  5. Twitter will show you a PIN code
  6. Copy that PIN and paste it below
  
""")

print("=" * 70)
print("  STEP 2: ENTER PIN")
print("=" * 70)

pin = input("\n  Enter the PIN from Twitter: ").strip()

if not pin:
    print("\n  No PIN provided. Exiting.")
    sys.exit(1)

print("\n" + "=" * 70)
print("  STEP 3: GET ACCESS TOKEN")
print("=" * 70)

try:
    # Exchange PIN for access token
    access_token_url = f"https://api.twitter.com/oauth/access_token?oauth_verifier={pin}"
    access_token_response = twitter.fetch_token(access_token_url)
    
    access_token = access_token_response['oauth_token']
    access_token_secret = access_token_response['oauth_token_secret']
    user_id = access_token_response.get('user_id', 'unknown')
    screen_name = access_token_response.get('screen_name', 'unknown')
    
    print(f"\n  SUCCESS!")
    print(f"\n  User: @{screen_name} (ID: {user_id})")
    print(f"\n  Access Token: {access_token}")
    print(f"  Access Token Secret: {access_token_secret}")
    
    # Save to .env
    print("\n" + "=" * 70)
    print("  STEP 4: SAVE TO .ENV")
    print("=" * 70)
    
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    # Read existing .env
    env_content = ""
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Update or add tokens
    lines = env_content.split('\n')
    new_lines = []
    token_added = False
    secret_added = False
    
    for line in lines:
        if line.startswith('TWITTER_ACCESS_TOKEN='):
            new_lines.append(f'TWITTER_ACCESS_TOKEN={access_token}')
            token_added = True
        elif line.startswith('TWITTER_ACCESS_TOKEN_SECRET='):
            new_lines.append(f'TWITTER_ACCESS_TOKEN_SECRET={access_token_secret}')
            secret_added = True
        else:
            new_lines.append(line)
    
    if not token_added:
        new_lines.append(f'TWITTER_ACCESS_TOKEN={access_token}')
    if not secret_added:
        new_lines.append(f'TWITTER_ACCESS_TOKEN_SECRET={access_token_secret}')
    
    # Write updated .env
    with open(env_file, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print(f"\n  Saved to: {env_file}")
    print(f"\n  Now run: python post_twitter_api.py")
    print(f"\n  Or: python post_twitter_thread.py")
    
except Exception as e:
    print(f"\n  Error: {e}")
    print("\n  Troubleshooting:")
    print("  - Make sure you entered the correct PIN")
    print("  - PIN expires quickly, try again if it took too long")
    print("  - Check that your Twitter app has 'Read and Write' permissions")

print("\n" + "=" * 70)

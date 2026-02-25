#!/usr/bin/env python3
"""
Twitter OAuth 1.0a Token Getter - Complete with PIN
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials
API_KEY = os.getenv('TWITTER_API_KEY', '')
API_SECRET = os.getenv('TWITTER_API_SECRET', '')

# PIN from user
PIN = sys.argv[1] if len(sys.argv) > 1 else None

if not API_KEY or not API_SECRET:
    print("ERROR: TWITTER_API_KEY or TWITTER_API_SECRET not set in .env")
    sys.exit(1)

if not PIN:
    print("ERROR: PIN not provided. Usage: python complete_twitter_oauth.py <PIN>")
    sys.exit(1)

print("=" * 70)
print("  TWITTER OAUTH - EXCHANGING PIN FOR ACCESS TOKEN")
print("=" * 70)

try:
    from requests_oauthlib import OAuth1Session
except ImportError:
    print("Installing requests-oauthlib...")
    os.system('pip install requests-oauthlib')
    from requests_oauthlib import OAuth1Session

callback_uri = 'oob'

print(f"\n  API Key: {API_KEY[:10]}...")
print(f"  PIN: {PIN}")

# Create OAuth session
twitter = OAuth1Session(API_KEY, client_secret=API_SECRET, callback_uri=callback_uri)

# Exchange PIN for access token
print("\n  Exchanging PIN for access token...")

try:
    access_token_url = f"https://api.twitter.com/oauth/access_token?oauth_verifier={PIN}"
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
    print("  SAVING TO .ENV")
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
    print(f"\n  Credentials configured successfully!")
    
except Exception as e:
    print(f"\n  Error: {e}")
    print("\n  Possible issues:")
    print("  - PIN may have expired (they expire quickly)")
    print("  - PIN was entered incorrectly")
    print("  - Try the OAuth flow again")
    sys.exit(1)

print("\n" + "=" * 70)
print("  NEXT STEP: POST THE THREAD")
print("=" * 70)
print("\n  Run: python post_twitter_api.py")
print("\n" + "=" * 70)

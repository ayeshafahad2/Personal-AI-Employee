#!/usr/bin/env python3
"""
Twitter OAuth 1.0a - Complete Flow with PIN
Usage: 
  Step 1: python twitter_oauth_complete.py (get URL)
  Step 2: Open URL, authorize, get PIN
  Step 3: python twitter_oauth_complete.py <PIN> (get tokens)
"""

import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TWITTER_API_KEY', '')
API_SECRET = os.getenv('TWITTER_API_SECRET', '')

if not API_KEY or not API_SECRET:
    print("ERROR: TWITTER_API_KEY or TWITTER_API_SECRET not set in .env")
    sys.exit(1)

print("=" * 70)
print("  TWITTER OAUTH 1.0a - COMPLETE FLOW")
print("=" * 70)

try:
    from requests_oauthlib import OAuth1Session
    from oauthlib.oauth1 import SIGNATURE_HMAC
except ImportError:
    print("Installing requests-oauthlib...")
    os.system('pip install requests-oauthlib')
    from requests_oauthlib import OAuth1Session

PIN = sys.argv[1] if len(sys.argv) > 1 else None
callback_uri = 'oob'
temp_file = os.path.join(os.path.dirname(__file__), '.twitter_oauth_temp.json')

if not PIN:
    # Step 1: Get authorization URL
    print("\n  Generating authorization URL...")
    
    twitter = OAuth1Session(API_KEY, client_secret=API_SECRET, callback_uri=callback_uri)
    request_token_url = "https://api.twitter.com/oauth/request_token"
    twitter.fetch_request_token(request_token_url)
    authorization_url = twitter.authorization_url("https://api.twitter.com/oauth/authorize")
    
    # Save request token for step 2
    with open(temp_file, 'w') as f:
        json.dump({
            'resource_owner_key': twitter._client.resource_owner_key,
            'resource_owner_secret': twitter._client.resource_owner_secret
        }, f)
    
    print(f"""
  Open this URL in your browser:
  
  {authorization_url}
  
  INSTRUCTIONS:
  1. Log in to Twitter
  2. Click 'Authorize app'  
  3. Copy the PIN shown
  4. Run: python twitter_oauth_complete.py <YOUR_PIN>
""")
    
else:
    # Step 2: Exchange PIN for access token
    print(f"\n  PIN: {PIN}")
    
    if not os.path.exists(temp_file):
        print("\n  ERROR: No pending OAuth request.")
        print("  Run without PIN first: python twitter_oauth_complete.py")
        sys.exit(1)
    
    with open(temp_file, 'r') as f:
        temp_data = json.load(f)
    
    twitter = OAuth1Session(
        API_KEY,
        client_secret=API_SECRET,
        resource_owner_key=temp_data['resource_owner_key'],
        resource_owner_secret=temp_data['resource_owner_secret'],
        callback_uri=callback_uri
    )
    
    print("  Exchanging PIN for access token...")
    
    try:
        access_token_url = f"https://api.twitter.com/oauth/access_token?oauth_verifier={PIN}"
        access_token_response = twitter.post(access_token_url)
        
        if access_token_response.status_code != 200:
            print(f"\n  ERROR: {access_token_response.status_code}")
            print(f"  Response: {access_token_response.text}")
            print("\n  PIN may have expired. Try again.")
            sys.exit(1)
        
        from urllib.parse import parse_qs
        parsed = parse_qs(access_token_response.text)
        
        access_token = parsed.get('oauth_token', [''])[0]
        access_token_secret = parsed.get('oauth_token_secret', [''])[0]
        user_id = parsed.get('user_id', ['unknown'])[0]
        screen_name = parsed.get('screen_name', ['unknown'])[0]
        
        if not access_token:
            print(f"\n  ERROR: No access token in response")
            print(f"  Response: {access_token_response.text}")
            sys.exit(1)
        
        print(f"\n  SUCCESS!")
        print(f"\n  User: @{screen_name} (ID: {user_id})")
        print(f"  Access Token: {access_token[:20]}...")
        print(f"  Access Token Secret: {access_token_secret[:20]}...")
        
        # Save to .env
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        env_content = ""
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                env_content = f.read()
        
        lines = env_content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('TWITTER_ACCESS_TOKEN='):
                new_lines.append(f'TWITTER_ACCESS_TOKEN={access_token}')
            elif line.startswith('TWITTER_ACCESS_TOKEN_SECRET='):
                new_lines.append(f'TWITTER_ACCESS_TOKEN_SECRET={access_token_secret}')
            else:
                new_lines.append(line)
        
        if 'TWITTER_ACCESS_TOKEN=' not in env_content:
            new_lines.append(f'TWITTER_ACCESS_TOKEN={access_token}')
        if 'TWITTER_ACCESS_TOKEN_SECRET=' not in env_content:
            new_lines.append(f'TWITTER_ACCESS_TOKEN_SECRET={access_token_secret}')
        
        with open(env_file, 'w') as f:
            f.write('\n'.join(new_lines))
        
        os.remove(temp_file)
        
        print(f"\n  Saved to .env")
        print("\n  NOW RUN: python post_twitter_api.py")
        
    except Exception as e:
        print(f"\n  ERROR: {e}")
        print("\n  PIN may have expired. Try again.")

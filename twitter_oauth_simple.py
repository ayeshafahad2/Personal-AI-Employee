#!/usr/bin/env python3
"""
Twitter OAuth 1.0a - PIN Flow using requests-oauthlib correctly
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
print("  TWITTER OAUTH 1.0a - PIN FLOW")
print("=" * 70)

try:
    from requests_oauthlib import OAuth1
    import requests
except ImportError:
    print("Installing requests-oauthlib...")
    os.system('pip install requests-oauthlib')
    from requests_oauthlib import OAuth1
    import requests

PIN = sys.argv[1] if len(sys.argv) > 1 else None
temp_file = os.path.join(os.path.dirname(__file__), '.twitter_oauth_temp.json')

if not PIN:
    # Step 1: Get request token
    print("\n  Getting request token...")
    
    try:
        oauth = OAuth1(API_KEY, client_secret=API_SECRET, callback_uri='oob')
        
        # Get request token
        response = requests.post(
            'https://api.twitter.com/oauth/request_token',
            auth=oauth
        )
        
        if response.status_code != 200:
            print(f"\n  ERROR: {response.status_code}")
            print(f"  Response: {response.text}")
            sys.exit(1)
        
        from urllib.parse import parse_qs
        result = parse_qs(response.text)
        
        request_token = result.get('oauth_token', [''])[0]
        request_token_secret = result.get('oauth_token_secret', [''])[0]
        
        if not request_token:
            print(f"\n  ERROR: Could not get request token")
            sys.exit(1)
        
        # Save for step 2
        with open(temp_file, 'w') as f:
            json.dump({
                'oauth_token': request_token,
                'oauth_token_secret': request_token_secret
            }, f)
        
        authorization_url = f"https://api.twitter.com/oauth/authorize?oauth_token={request_token}"
        
        print(f"""
  Open this URL in your browser:
  
  {authorization_url}
  
  INSTRUCTIONS:
  1. Log in to Twitter
  2. Click 'Authorize app'  
  3. Copy the PIN shown
  4. Run: python twitter_oauth_simple.py <YOUR_PIN>
""")
        
    except Exception as e:
        print(f"\n  ERROR: {e}")
        sys.exit(1)

else:
    # Step 2: Exchange PIN for access token
    print(f"\n  PIN: {PIN}")
    
    if not os.path.exists(temp_file):
        print("\n  ERROR: No pending OAuth request.")
        print("  Run without PIN first.")
        sys.exit(1)
    
    with open(temp_file, 'r') as f:
        temp_data = json.load(f)
    
    print("  Exchanging PIN for access token...")
    
    try:
        oauth = OAuth1(
            API_KEY,
            client_secret=API_SECRET,
            resource_owner_key=temp_data['oauth_token'],
            resource_owner_secret=temp_data['oauth_token_secret'],
            verifier=PIN
        )
        
        response = requests.post(
            'https://api.twitter.com/oauth/access_token',
            auth=oauth
        )
        
        if response.status_code != 200:
            print(f"\n  ERROR: {response.status_code}")
            print(f"  Response: {response.text}")
            print("\n  PIN may have expired. Try again.")
            sys.exit(1)
        
        from urllib.parse import parse_qs
        result = parse_qs(response.text)
        
        access_token = result.get('oauth_token', [''])[0]
        access_token_secret = result.get('oauth_token_secret', [''])[0]
        user_id = result.get('user_id', ['unknown'])[0]
        screen_name = result.get('screen_name', ['unknown'])[0]
        
        if not access_token:
            print(f"\n  ERROR: No access token in response")
            print(f"  Response: {result}")
            sys.exit(1)
        
        print(f"\n  SUCCESS!")
        print(f"\n  User: @{screen_name} (ID: {user_id})")
        print(f"  Access Token: {access_token[:30]}...")
        print(f"  Access Token Secret: {access_token_secret[:30]}...")
        
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

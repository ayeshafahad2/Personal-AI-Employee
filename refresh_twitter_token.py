#!/usr/bin/env python3
"""
Twitter Bearer Token Refresh - Get Fresh Token
This script gets a new bearer token using your API key and secret

Usage:
    python refresh_twitter_token.py
"""

import os
import sys
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("  TWITTER BEARER TOKEN REFRESH")
print("=" * 70)

# Get credentials
api_key = os.getenv('TWITTER_API_KEY', '')
api_secret = os.getenv('TWITTER_API_SECRET', '')

if not api_key or not api_secret:
    print("\n  ERROR: TWITTER_API_KEY or TWITTER_API_SECRET not set in .env")
    print("  Please add them to your .env file first.")
    sys.exit(1)

print(f"\n  API Key: {api_key[:15]}...")
print(f"  API Secret: {api_secret[:15]}...")

# Encode credentials
key_secret = f"{api_key}:{api_secret}".encode('ascii')
b64_encoded_key = base64.b64encode(key_secret).decode('ascii')

# Get bearer token
token_url = "https://api.twitter.com/oauth2/token"
headers = {
    "Authorization": f"Basic {b64_encoded_key}",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}
data = {"grant_type": "client_credentials"}

print("\n  Requesting new bearer token...")

try:
    response = requests.post(token_url, headers=headers, data=data, timeout=30)
    response.raise_for_status()
    
    token_data = response.json()
    new_bearer_token = token_data.get('access_token', '')
    
    if new_bearer_token:
        print("\n  [SUCCESS] New bearer token obtained.")
        print(f"\n  Token: {new_bearer_token[:50]}...")
        
        # Ask to update .env
        update = input("\n  Update .env file with new token? (y/n): ").strip().lower()
        
        if update == 'y':
            # Read current .env
            env_file = '.env'
            env_content = ""
            
            with open(env_file, 'r', encoding='utf-8') as f:
                env_content = f.read()
            
            # Replace old token with new
            import re
            old_token_pattern = r'TWITTER_BEARER_TOKEN=.*'
            new_line = f'TWITTER_BEARER_TOKEN={new_bearer_token}'
            
            if re.search(old_token_pattern, env_content):
                env_content = re.sub(old_token_pattern, new_line, env_content)
            else:
                env_content += f'\n{new_line}\n'
            
            # Write updated .env
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            
            print("\n  [OK] .env file updated!")
            print("\n  [INFO] Restart dashboard server to use new token.")
        else:
            print("\n  [INFO] Token not saved. Add it manually to .env:")
            print(f"  TWITTER_BEARER_TOKEN={new_bearer_token}")
    else:
        print("\n  [ERROR] No token in response")
        
except requests.exceptions.RequestException as e:
    print(f"\n  [ERROR] {e}")
    print("\n  Possible issues:")
    print("  1. Invalid API Key/Secret")
    print("  2. Twitter API downtime")
    print("  3. Network connection issue")
except Exception as e:
    print(f"\n  [ERROR] {e}")

print("\n" + "=" * 70)

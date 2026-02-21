#!/usr/bin/env python3
"""
Open LinkedIn in Google Chrome
"""

import webbrowser
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("  OPENING LINKEDIN IN CHROME")
print("=" * 70)

# Get credentials
client_id = os.getenv('LINKEDIN_CLIENT_ID', '7763qv2uyw7eao')

# Build auth URL
auth_url = (
    f"https://www.linkedin.com/oauth/v2/authorization?"
    f"response_type=code&"
    f"client_id={client_id}&"
    f"redirect_uri=https://localhost&"
    f"scope={urllib.parse.quote('r_liteprofile w_member_social')}&"
    f"state=linkedin_auth"
)

print("\nAuthorization URL:")
print(f"{auth_url[:80]}...")

# Try to open in Chrome
chrome_paths = [
    r'C:/Program Files/Google/Chrome/Application/chrome.exe',
    r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
]

chrome_found = False
for chrome_path in chrome_paths:
    if os.path.exists(chrome_path):
        print(f"\nFound Chrome at: {chrome_path}")
        try:
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
            webbrowser.get('chrome').open(auth_url)
            print("LinkedIn opened in Chrome!")
            chrome_found = True
            break
        except Exception as e:
            print(f"Error opening Chrome: {e}")

if not chrome_found:
    print("\nChrome not found, opening in default browser...")
    webbrowser.open(auth_url)
    print("Opened in default browser.")

print("\n" + "=" * 70)
print("  INSTRUCTIONS")
print("=" * 70)
print("""
1. Sign in to LinkedIn in Chrome
2. Click 'Allow' to authorize
3. After redirect, look at the address bar
4. Copy the code from the URL (between 'code=' and '&')

Example:
https://localhost?code=XXXXXX&state=linkedin_auth
                    ^^^^^^
                    Copy this
""")
print("=" * 70)

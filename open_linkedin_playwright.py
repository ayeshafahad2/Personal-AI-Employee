#!/usr/bin/env python3
"""
Open LinkedIn Authorization using Playwright
"""

from playwright.sync_api import sync_playwright
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("  LINKEDIN AUTHORIZATION - PLAYWRIGHT")
print("=" * 70)

# Get credentials
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

print("\nOpening LinkedIn in browser...")
print(f"URL: {auth_url[:100]}...")

# Launch browser
with sync_playwright() as p:
    # Launch visible browser
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Navigate to LinkedIn auth
    print("\nNavigating to LinkedIn authorization page...")
    page.goto(auth_url)
    
    print("\n" + "=" * 70)
    print("  BROWSER OPENED")
    print("=" * 70)
    print("""
  Next Steps:
  
  1. Sign in to LinkedIn (if not already signed in)
  2. Click 'Allow' to authorize the application
  3. After redirect, copy the code from the URL
  
  The browser will stay open for you to complete authorization.
  
  After you get the code, paste it here.
  """)
    print("=" * 70)
    
    # Wait for user to complete authorization
    # Keep browser open for 5 minutes
    try:
        print("\nWaiting for authorization (5 minutes max)...")
        print("Complete the authorization in the browser window.")
        
        # Wait for redirect or user input
        page.wait_for_timeout(300000)  # 5 minutes
        
    except Exception as e:
        print(f"Browser closed or error: {e}")
    
    browser.close()

print("\nBrowser closed.")
print("\nDid you get the authorization code?")
print("If yes, paste it and I'll exchange it for an access token.")

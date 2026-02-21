#!/usr/bin/env python3
"""
Open LinkedIn Authorization using Playwright (Non-blocking)
"""

from playwright.sync_api import sync_playwright
import urllib.parse
import os
from dotenv import load_dotenv
import time

load_dotenv()

print("=" * 70)
print("  OPENING LINKEDIN AUTHORIZATION")
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

print("\nLaunching browser...")

# Launch browser
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Navigate to LinkedIn auth
    print("Navigating to LinkedIn...")
    page.goto(auth_url, wait_until='domcontentloaded')
    
    print("\n" + "=" * 70)
    print("  LINKEDIN OPENED IN BROWSER")
    print("=" * 70)
    print("""
  INSTRUCTIONS:
  
  1. Sign in to LinkedIn (if prompted)
  2. Click 'Allow' to authorize
  3. After redirect, look at the URL in address bar
  4. Copy the code (after 'code=' and before '&')
  
  Example URL:
  https://localhost?code=AQEDAXXXXX-yyy&state=linkedin_auth
                    ^^^^^^^^^^^^^^^
                    Copy this part
  
  5. Paste the code here when ready
  """)
    print("=" * 70)
    
    # Give user time to see instructions
    time.sleep(2)
    
    # Keep browser open but return control to user
    # Browser will stay open in background
    print("\nBrowser window is open - complete authorization there.")
    print("The browser will stay open while you authorize.")

# Browser context closes but window may stay open depending on OS
print("\nWaiting for your authorization code...")

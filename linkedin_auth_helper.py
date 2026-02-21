#!/usr/bin/env python3
"""
Helper script to generate LinkedIn access token
"""
import webbrowser
import urllib.parse
from pathlib import Path
import os

def generate_linkedin_auth_url():
    """
    Generates the LinkedIn OAuth 2.0 authorization URL
    """
    client_id = os.getenv('LINKEDIN_CLIENT_ID', '7763qv2uyw7eao')
    redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost')
    
    # Define the required scopes
    scopes = [
        'r_liteprofile',    # Basic profile information
        'w_member_social',  # Post updates
    ]
    
    scope_str = ' '.join(scopes)
    
    # Construct the authorization URL
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri=https://localhost&"  # Using https for LinkedIn OAuth
        f"scope={urllib.parse.quote(scope_str)}&"
        f"state=linkedin_auth_state"
    )
    
    return auth_url

def main():
    print("LinkedIn Access Token Generator")
    print("=" * 40)
    print()
    
    print("Step 1: Get Authorization Code")
    print("-" * 30)
    auth_url = generate_linkedin_auth_url()
    print(f"Visit this URL to authorize the application:")
    print(auth_url)
    print()
    
    print("After authorizing, you'll be redirected to your redirect URI")
    print("with an authorization code in the URL. Copy the 'code' parameter.")
    print()
    
    open_browser = input("Would you like to open the authorization URL in your browser? (y/n): ")
    if open_browser.lower() == 'y':
        webbrowser.open(auth_url)
    
    print()
    print("Step 2: Exchange Authorization Code for Access Token")
    print("-" * 50)
    print("Once you have the authorization code, exchange it for an access token.")
    print("You can do this using a tool like curl or Postman, or by visiting:")
    print()
    print("https://www.linkedin.com/developers/tools/oauth")
    print()
    
    print("The token exchange request looks like this:")
    print("POST https://www.linkedin.com/oauth/v2/accessToken")
    print("Content-Type: application/x-www-form-urlencoded")
    print()
    print("Body parameters:")
    print("- grant_type: authorization_code")
    print(f"- code: [YOUR_AUTHORIZATION_CODE]")
    print(f"- redirect_uri: {os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost')}")
    print(f"- client_id: {os.getenv('LINKEDIN_CLIENT_ID', '7763qv2uyw7eao')}")
    print(f"- client_secret: [YOUR_CLIENT_SECRET]")
    print()
    
    print("Step 3: Update Your Environment")
    print("-" * 30)
    print("After getting your access token, update your .env file:")
    print()
    print("# LinkedIn API Credentials")
    print(f"LINKEDIN_CLIENT_ID={os.getenv('LINKEDIN_CLIENT_ID', '7763qv2uyw7eao')}")
    print(f"LINKEDIN_CLIENT_SECRET={os.getenv('LINKEDIN_CLIENT_SECRET', 'WPL_AP1.YOUR_LINKEDIN_SECRET_HERE')}")
    print("LINKEDIN_ACCESS_TOKEN=[YOUR_ACTUAL_ACCESS_TOKEN]")
    print("LINKEDIN_REFRESH_TOKEN=[YOUR_REFRESH_TOKEN_IF_PROVIDED]")
    print(f"LINKEDIN_REDIRECT_URI={os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost')}")
    print()
    
    print("Step 4: Test the Integration")
    print("-" * 25)
    print("Run the following command to test:")
    print("python test_linkedin_watcher.py")

if __name__ == "__main__":
    main()
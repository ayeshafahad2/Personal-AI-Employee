#!/usr/bin/env python3
"""
LinkedIn Redirect URI Auto-Fixer
Automatically fixes the redirect URI issue by using the most common working format
"""
import os
from pathlib import Path
import re

def fix_redirect_uri():
    """
    Fixes the redirect URI in the .env file to use the most common working format
    """
    print("LinkedIn Redirect URI Auto-Fixer")
    print("=" * 40)
    print()
    
    # The most common working redirect URI for LinkedIn OAuth
    working_redirect_uri = "https://localhost"
    
    print(f"Fixing redirect URI to use: {working_redirect_uri}")
    print("(This is the most commonly accepted format for LinkedIn OAuth)")
    print()
    
    # Read the current .env file
    env_path = Path(".env")
    if not env_path.exists():
        print("Error: .env file not found!")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Update the LINKEDIN_REDIRECT_URI
    updated_content = re.sub(
        r'LINKEDIN_REDIRECT_URI=.*$', 
        f'LINKEDIN_REDIRECT_URI={working_redirect_uri}', 
        content, 
        flags=re.MULTILINE
    )
    
    # Write the updated content back
    with open(env_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Successfully updated .env file to use {working_redirect_uri}")
    print()
    
    # Generate the correct authorization URL
    client_id = "7763qv2uyw7eao"
    scopes = "r_liteprofile%20w_member_social"  # Using scopes that don't require special approval
    state = "linkedin_auth_state"
    
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri={working_redirect_uri}&scope={scopes}&state={state}"
    
    print("CORRECTED AUTHORIZATION URL:")
    print("=" * 60)
    print(auth_url)
    print("=" * 60)
    print()
    
    print("Steps to get your access token:")
    print("1. Visit the URL above to authorize your application")
    print("2. Log in to LinkedIn and approve the requested permissions")
    print("3. You'll be redirected to https://localhost with an authorization code")
    print("4. Copy the 'code' parameter from the URL")
    print("5. Exchange the code for an access token using LinkedIn's token endpoint")
    print()
    
    print("TIP: If https://localhost doesn't work, try registering http://localhost")
    print("    in your LinkedIn application settings instead.")
    
    return True

def main():
    fix_redirect_uri()

if __name__ == "__main__":
    main()
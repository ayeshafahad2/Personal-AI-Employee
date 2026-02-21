#!/usr/bin/env python3
"""
LinkedIn Redirect URI Resolver
Helps you create the correct authorization URL with the exact redirect URI registered with your application
"""
import os
from pathlib import Path
import urllib.parse

def create_correct_authorization_url():
    """
    Creates the correct LinkedIn authorization URL with the exact redirect URI
    """
    print("LinkedIn Redirect URI Resolver")
    print("=" * 40)
    print()
    
    print("To fix the redirect URI error, you need to use the exact redirect URI")
    print("that is registered with your LinkedIn application.")
    print()
    
    print("Please visit https://www.linkedin.com/developers/ to check your")
    print("application's registered redirect URIs under the 'Auth' tab.")
    print()
    
    print("Common redirect URI formats include:")
    print("1. https://localhost")
    print("2. https://localhost:3000/callback")
    print("3. http://localhost:3000/callback")
    print("4. https://yourdomain.com/callback")
    print("5. http://localhost:8080/callback")
    print()
    
    registered_uri = input("Enter the EXACT redirect URI registered with your LinkedIn application: ").strip()
    
    if not registered_uri:
        print("No redirect URI entered. Using https://localhost as default.")
        registered_uri = "https://localhost"
    
    # Create the authorization URL with the exact registered URI
    client_id = "7763qv2uyw7eao"
    scopes = "r_liteprofile%20w_member_social"  # Using scopes that don't require special approval
    state = "linkedin_auth_state"
    
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri={urllib.parse.quote(registered_uri)}&scope={scopes}&state={state}"
    
    print()
    print("✅ CORRECTED AUTHORIZATION URL:")
    print("=" * 60)
    print(auth_url)
    print("=" * 60)
    print()
    
    print("Steps to get your access token:")
    print("1. Visit the URL above to authorize your application")
    print("2. Log in to LinkedIn and approve the requested permissions")
    print("3. You'll be redirected to your registered URI with an authorization code")
    print("4. Copy the 'code' parameter from the URL")
    print("5. Exchange the code for an access token using LinkedIn's token endpoint")
    print()
    
    # Also update the .env file with the correct redirect URI
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Update the LINKEDIN_REDIRECT_URI
        import re
        updated_content = re.sub(
            r'LINKEDIN_REDIRECT_URI=.*$', 
            f'LINKEDIN_REDIRECT_URI={registered_uri}', 
            content, 
            flags=re.MULTILINE
        )
        
        # Write the updated content back
        with open(env_path, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated .env file with the correct redirect URI: {registered_uri}")
    
    return auth_url

def main():
    create_correct_authorization_url()

if __name__ == "__main__":
    main()
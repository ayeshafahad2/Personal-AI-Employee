#!/usr/bin/env python3
"""
LinkedIn Redirect URI Configurator
Updates the .env file to use the correct redirect URI for LinkedIn API
"""
import os
from pathlib import Path
import re

def configure_default_redirect_uri():
    """
    Updates the .env file to use https://localhost as the redirect URI
    """
    print("LinkedIn Redirect URI Configurator")
    print("=" * 40)
    print()
    
    print("Configuring .env file to use: https://localhost")
    print("(This is the most commonly used redirect URI for LinkedIn OAuth)")
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
        'LINKEDIN_REDIRECT_URI=https://localhost', 
        content, 
        flags=re.MULTILINE
    )
    
    # Write the updated content back
    with open(env_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Successfully updated .env file to use https://localhost")
    print("\nYou can now use this redirect URI when getting your LinkedIn access token.")
    print("\nTo get your access token:")
    print("1. Visit: https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=7763qv2uyw7eao&redirect_uri=https://localhost&scope=r_liteprofile%20r_emailaddress%20w_member_social%20rw_ads%20r_organization_social&state=linkedin_auth_state")
    print("2. Follow the instructions to get your authorization code")
    print("3. Exchange the code for an access token")
    print("4. Update your .env file with the access token")
    print("5. Run: python post_to_linkedin_auto.py")
    
    return True

def main():
    configure_default_redirect_uri()

if __name__ == "__main__":
    main()
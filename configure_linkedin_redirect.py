#!/usr/bin/env python3
"""
LinkedIn Redirect URI Configurator
Helps you select and configure the correct redirect URI for LinkedIn API
"""
import os
from pathlib import Path

def configure_redirect_uri():
    """
    Helps configure the correct redirect URI in the .env file
    """
    print("LinkedIn Redirect URI Configurator")
    print("=" * 40)
    print()
    
    print("You have two redirect URIs registered with your LinkedIn application:")
    print("1. https://localhost")
    print("2. https://localhost:3000/callback")
    print()
    
    choice = input("Which redirect URI would you like to use? (1/2): ").strip()
    
    if choice == "1":
        selected_uri = "https://localhost"
    elif choice == "2":
        selected_uri = "https://localhost:3000/callback"
    else:
        print("Invalid choice. Using https://localhost as default.")
        selected_uri = "https://localhost"
    
    print(f"\nUpdating .env file to use: {selected_uri}")
    
    # Read the current .env file
    env_path = Path(".env")
    if not env_path.exists():
        print("Error: .env file not found!")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Update the LINKEDIN_REDIRECT_URI
    import re
    updated_content = re.sub(
        r'LINKEDIN_REDIRECT_URI=.*$', 
        f'LINKEDIN_REDIRECT_URI={selected_uri}', 
        content, 
        flags=re.MULTILINE
    )
    
    # Write the updated content back
    with open(env_path, 'w') as f:
        f.write(updated_content)
    
    print(f"\n✅ Successfully updated .env file to use {selected_uri}")
    print("\nYou can now use this redirect URI when getting your LinkedIn access token.")
    
    return True

def main():
    configure_redirect_uri()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
LinkedIn Post Publisher - Complete Process
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.linkedin_watcher import LinkedInWatcher

def publish_post_with_token_check():
    """
    Publish the post with token validation
    """
    print("=" * 80)
    print("LINKEDIN POST PUBLISHER - COMPLETE PROCESS")
    print("=" * 80)
    print()
    
    # Check if we have an access token
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ Error: .env file not found!")
        return False
    
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    # Check if access token is still the placeholder
    if "your_linkedin_access_token_here" in env_content:
        print("No valid LinkedIn access token found in .env file!")
        print()
        print("To publish your post, you need to:")
        print("1. Get your LinkedIn access token using the authorization URL:")
        print("   https://www.linkedin.com/oauth/v2/authorization?response_type=code&")
        print("   client_id=7763qv2uyw7eao&redirect_uri=https://localhost&")
        print("   scope=r_liteprofile%20w_member_social&state=linkedin_auth_state")
        print()
        print("2. Exchange the authorization code for an access token")
        print("3. Update your .env file with the access token")
        print("4. Replace 'your_linkedin_access_token_here' with your actual token")
        print()
        print("After updating your .env file, run this script again.")
        return False
    
    print("Valid LinkedIn access token found!")
    print()
    
    # Get the vault path
    vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'
    vault_path.mkdir(parents=True, exist_ok=True)
    
    # Create the LinkedIn watcher instance
    watcher = LinkedInWatcher(str(vault_path))
    
    # Read the post content
    post_file = Path("linkedin_post_best_personal_ai_employee_20260213_000304.txt")
    if not post_file.exists():
        print("❌ Error: Post file not found!")
        return False
    
    with open(post_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📝 Post content to be published:")
    print("-" * 80)
    print(content[:500] + "..." if len(content) > 500 else content)
    print("-" * 80)
    print()
    
    # Attempt to post
    print("📤 Attempting to publish post to LinkedIn...")
    result = watcher.post_content(content)
    
    if result:
        print(f"Successfully published post to LinkedIn!")
        print(f"Post ID: {result.get('id', 'Unknown')}")
        print()
        print("Your LinkedIn post about Personal AI Employees has been published successfully!")
        print("Check your LinkedIn profile to see the post.")
        return True
    else:
        print("Failed to publish post to LinkedIn.")
        print("This could be due to an invalid access token or insufficient permissions.")
        print("Please verify your access token and try again.")
        return False

def main():
    success = publish_post_with_token_check()
    
    if not success:
        print()
        print("To get your access token:")
        print("1. Visit: https://www.linkedin.com/oauth/v2/authorization?response_type=code&")
        print("   client_id=7763qv2uyw7eao&redirect_uri=https://localhost&")
        print("   scope=r_liteprofile%20w_member_social&state=linkedin_auth_state")
        print("2. Authorize the application")
        print("3. Copy the 'code' parameter from the redirect URL")
        print("4. Exchange the code for an access token using LinkedIn's API")
        print("5. Update your .env file with the access token")
        print("6. Run this script again")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
LinkedIn Poster - Posts content to LinkedIn using the API
"""
import os
import sys
from pathlib import Path
import time

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.linkedin_watcher import LinkedInWatcher

def post_to_linkedin(text_content, vault_path=None):
    """
    Posts content to LinkedIn using the LinkedInWatcher
    """
    if vault_path is None:
        vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'
        vault_path.mkdir(parents=True, exist_ok=True)
    
    # Create the LinkedIn watcher instance
    watcher = LinkedInWatcher(str(vault_path))
    
    # Check if we have an access token
    if not watcher.access_token or watcher.access_token == "your_linkedin_access_token_here":
        print("Error: No valid LinkedIn access token found!")
        print("\nTo post to LinkedIn, you need to:")
        print("1. Get your LinkedIn access token (follow instructions in LINKEDIN_WATCHER_README.md)")
        print("2. Update the LINKEDIN_ACCESS_TOKEN in your .env file with your actual token")
        print("3. Run this script again")
        return False
    
    print("LinkedIn access token found. Attempting to post...")
    
    # Post the content
    result = watcher.post_content(text_content)
    
    if result:
        print(f"Successfully posted to LinkedIn!")
        print(f"Post ID: {result.get('id', 'Unknown')}")
        print(f"Response: {result}")
        return True
    else:
        print("Failed to post to LinkedIn. Check the logs for details.")
        return False

def main():
    print("LinkedIn Poster - Automated Posting")
    print("=" * 50)
    
    # Get the LinkedIn post content from the long post file
    long_post_path = Path("linkedin_post_personal_ai_employee_20260212_215403.txt")
    
    # Check if the file exists
    if not long_post_path.exists():
        print("❌ LinkedIn post file not found!")
        print("Please run the post generation scripts first.")
        return
    
    # Read the content
    with open(long_post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\nLinkedIn post content to be published:")
    print("-" * 50)
    print(content)
    print("-" * 50)
    
    print("\nAttempting to post to LinkedIn...")
    success = post_to_linkedin(content)
    
    if success:
        print("\nYour LinkedIn post has been published successfully!")
        print("Check your LinkedIn profile to see the post.")
    else:
        print("\nFailed to publish your LinkedIn post.")
        print("This is likely because you don't have a valid access token yet.")
        print("Follow these steps to get one:")
        print("1. Run: python linkedin_auth_helper.py")
        print("2. Follow the instructions to get your access token")
        print("3. Update your .env file with the token")
        print("4. Run this script again")

if __name__ == "__main__":
    main()
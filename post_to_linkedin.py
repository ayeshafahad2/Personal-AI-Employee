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
        print("❌ Error: No valid LinkedIn access token found!")
        print("\nTo post to LinkedIn, you need to:")
        print("1. Get your LinkedIn access token (follow instructions in LINKEDIN_WATCHER_README.md)")
        print("2. Update the LINKEDIN_ACCESS_TOKEN in your .env file")
        print("3. Run this script again")
        return False
    
    print("✅ LinkedIn access token found. Attempting to post...")
    
    # Post the content
    result = watcher.post_content(text_content)
    
    if result:
        print(f"✅ Successfully posted to LinkedIn!")
        print(f"Post ID: {result.get('id', 'Unknown')}")
        print(f"Response: {result}")
        return True
    else:
        print("❌ Failed to post to LinkedIn. Check the logs for details.")
        return False

def main():
    print("LinkedIn Poster")
    print("=" * 50)
    
    # Get the LinkedIn post content
    long_post_path = Path("linkedin_post_personal_ai_employee_20260212_215403.txt")
    short_post_path = Path("linkedin_post_personal_ai_employee_short_20260212_215457.txt")
    
    # Check if the files exist
    if not long_post_path.exists() and not short_post_path.exists():
        print("❌ LinkedIn post files not found!")
        print("Please run the post generation scripts first.")
        return
    
    print("\nAvailable LinkedIn posts:")
    if long_post_path.exists():
        print(f"1. Long post: {long_post_path.name}")
    if short_post_path.exists():
        print(f"2. Short post: {short_post_path.name}")
    
    # Ask user which post to use
    choice = input("\nWhich post would you like to publish? (1/2): ").strip()
    
    if choice == "1" and long_post_path.exists():
        with open(long_post_path, 'r', encoding='utf-8') as f:
            content = f.read()
    elif choice == "2" and short_post_path.exists():
        with open(short_post_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print("Invalid choice or file doesn't exist.")
        return
    
    print(f"\nSelected post content preview:")
    print("-" * 50)
    print(content[:500] + "..." if len(content) > 500 else content)
    print("-" * 50)
    
    confirm = input(f"\nDo you want to post this content to LinkedIn? (y/n): ").strip().lower()
    
    if confirm == 'y':
        success = post_to_linkedin(content)
        if success:
            print("\n🎉 Your LinkedIn post has been published successfully!")
        else:
            print("\n💥 Failed to publish your LinkedIn post.")
    else:
        print("\nPost publication cancelled.")

if __name__ == "__main__":
    main()
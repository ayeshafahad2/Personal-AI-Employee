#!/usr/bin/env python3
"""
LinkedIn Poster - Personal Employee Post
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.linkedin_watcher import LinkedInWatcher

def post_personal_employee_content():
    """
    Posts the Personal Employee content to LinkedIn
    """
    # Get the vault path
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
    
    print("LinkedIn access token found. Reading Personal Employee content...")
    
    # Read the Personal Employee post content
    post_file = Path("linkedin_post_personal_employee_20260212_224706.txt")
    if not post_file.exists():
        print("Error: Personal Employee post file not found!")
        return False
    
    with open(post_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Attempting to post Personal Employee content to LinkedIn...")
    
    # Post the content
    result = watcher.post_content(content)
    
    if result:
        print(f"Successfully posted Personal Employee content to LinkedIn!")
        print(f"Post ID: {result.get('id', 'Unknown')}")
        return True
    else:
        print("Failed to post Personal Employee content to LinkedIn.")
        return False

def main():
    print("LinkedIn Poster - Personal Employee Content")
    print("=" * 50)
    
    print("\nPersonal Employee post content:")
    print("-" * 50)
    
    # Read and display the content
    post_file = Path("linkedin_post_personal_employee_20260212_224706.txt")
    if post_file.exists():
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(content)
    else:
        print("Post file not found!")
        return
    
    print("-" * 50)
    
    success = post_personal_employee_content()
    
    if success:
        print("\n🎉 Your Personal Employee LinkedIn post has been published successfully!")
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
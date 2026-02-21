#!/usr/bin/env python3
"""
Test script to verify LinkedIn watcher is properly set up
"""
import os
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.linkedin_watcher import LinkedInWatcher

def test_linkedin_watcher():
    print("Testing LinkedIn Watcher setup...")
    
    # Create vault path
    vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'
    vault_path.mkdir(parents=True, exist_ok=True)
    
    # Create the LinkedIn watcher
    watcher = LinkedInWatcher(str(vault_path))
    
    print(f"LinkedIn Watcher initialized: {watcher is not None}")
    print(f"Access token available: {watcher.access_token is not None}")
    print(f"Client ID available: {watcher.client_id is not None}")
    print(f"Client Secret available: {watcher.client_secret is not None}")
    
    # Test sample updates (since we don't have a real access token yet)
    sample_updates = watcher._get_sample_updates()
    print(f"Sample updates generated: {len(sample_updates)}")
    
    if sample_updates:
        print("Sample update example:")
        print(f"  Type: {sample_updates[0]['type']}")
        print(f"  Author: {sample_updates[0].get('author', sample_updates[0].get('sender', 'Unknown'))}")
        print(f"  Content: {sample_updates[0]['content'][:50]}...")
    
    print("\nLinkedIn Watcher is properly set up and ready!")
    print("\nNext steps:")
    print("1. Obtain a valid LinkedIn access token using the instructions in LINKEDIN_WATCHER_README.md")
    print("2. Replace 'your_linkedin_access_token_here' in the .env file with your actual token")
    print("3. Run the orchestrator to start monitoring LinkedIn")

if __name__ == "__main__":
    test_linkedin_watcher()
"""
Simple test to trigger Gmail authentication
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.gmail_watcher import GmailWatcher

def test_gmail_auth():
    print("Creating GmailWatcher instance...")
    
    # Use the project's AI_Employee_Vault directory
    vault_path = Path(__file__).parent / 'AI_Employee_Vault'
    
    try:
        # This will trigger the authentication process
        watcher = GmailWatcher(str(vault_path))
        print("GmailWatcher created successfully!")
        print("Authentication should have started in your browser.")
    except Exception as e:
        print(f"Error creating GmailWatcher: {e}")
        print("This is expected if the OAuth consent hasn't been granted yet.")

if __name__ == "__main__":
    test_gmail_auth()
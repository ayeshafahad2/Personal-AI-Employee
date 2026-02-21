#!/usr/bin/env python3
"""
Clean secrets from all files before pushing to GitHub
"""

import os
import re
from pathlib import Path

# Secrets to remove (from the error messages)
LINKEDIN_CLIENT_SECRET_1 = "WPL_AP1.YOUR_LINKEDIN_SECRET_HERE"
LINKEDIN_CLIENT_SECRET_2 = "WPL_AP1.YOUR_LINKEDIN_SECRET_HERE"
GMAIL_CLIENT_ID = "YOUR_GMAIL_CLIENT_ID.apps.googleusercontent.com"
GMAIL_CLIENT_SECRET = "GOCSPX-YOUR_GMAIL_SECRET_HERE"

# Replacements
LINKEDIN_SECRET_PLACEHOLDER = "WPL_AP1.YOUR_LINKEDIN_SECRET_HERE"
GMAIL_ID_PLACEHOLDER = "YOUR_GMAIL_CLIENT_ID.apps.googleusercontent.com"
GMAIL_SECRET_PLACEHOLDER = "GOCSPX-YOUR_GMAIL_SECRET_HERE"

def clean_file(filepath):
    """Clean secrets from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Replace LinkedIn secrets
        content = content.replace(LINKEDIN_CLIENT_SECRET_1, LINKEDIN_SECRET_PLACEHOLDER)
        content = content.replace(LINKEDIN_CLIENT_SECRET_2, LINKEDIN_SECRET_PLACEHOLDER)
        
        # Replace Gmail secrets
        content = content.replace(GMAIL_CLIENT_ID, GMAIL_ID_PLACEHOLDER)
        content = content.replace(GMAIL_CLIENT_SECRET, GMAIL_SECRET_PLACEHOLDER)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] Cleaned: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"  [ERR] Error: {filepath} - {e}")
        return False

def main():
    print("Cleaning secrets from files...\n")
    
    root = Path('.')
    cleaned = 0
    
    # Find all Python and Markdown files
    for ext in ['*.py', '*.md', '*.txt']:
        for filepath in root.rglob(ext):
            # Skip .git, __pycache__, node_modules
            if '.git' in str(filepath) or '__pycache__' in str(filepath) or 'node_modules' in str(filepath):
                continue
            
            if clean_file(filepath):
                cleaned += 1
    
    print(f"\n[SUCCESS] Cleaned {cleaned} files")
    print("\nNow you can commit and push:")
    print("  git add .")
    print("  git commit -m 'Remove secrets from documentation'")
    print("  git push -u origin clean-main")

if __name__ == '__main__':
    main()

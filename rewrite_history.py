#!/usr/bin/env python3
"""
Rewrite git history to remove secrets
"""
import subprocess
import os

# Secrets to replace
replacements = [
    ('WPL_AP1.YOUR_LINKEDIN_SECRET_HERE', 'WPL_AP1.YOUR_LINKEDIN_SECRET_HERE'),
    ('WPL_AP1.YOUR_LINKEDIN_SECRET_HERE', 'WPL_AP1.YOUR_LINKEDIN_SECRET_HERE'),
    ('YOUR_GMAIL_CLIENT_ID.apps.googleusercontent.com', 'YOUR_GMAIL_CLIENT_ID.apps.googleusercontent.com'),
    ('GOCSPX-YOUR_GMAIL_SECRET_HERE', 'GOCSPX-YOUR_GMAIL_SECRET_HERE'),
]

print("Step 1: Create a backup branch")
subprocess.run(['git', 'branch', '-M', 'main-backup'], check=False)

print("Step 2: Reset to initial commit")
result = subprocess.run(['git', 'rev-list', '--max-parents=0', 'HEAD'], capture_output=True, text=True)
initial_commit = result.stdout.strip()
print(f"Initial commit: {initial_commit}")

print("Step 3: Create new orphan branch")
subprocess.run(['git', 'checkout', '--orphan', 'main-clean'], check=True)

print("Step 4: Remove all files from staging")
subprocess.run(['git', 'rm', '-rf', '.'], check=False)

print("Step 5: Checkout files from backup (without history)")
subprocess.run(['git', 'checkout', 'main-backup', '--', '.'], check=True)

print("Step 6: Clean secrets from all files")
import os
from pathlib import Path

for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith(('.py', '.md', '.txt', '.json')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                original = content
                for old, new in replacements:
                    content = content.replace(old, new)
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  Cleaned: {filepath}")
            except Exception as e:
                print(f"  Error: {filepath} - {e}")

print("Step 7: Add all files")
subprocess.run(['git', 'add', '-A'], check=True)

print("Step 8: Create clean commit")
subprocess.run(['git', 'commit', '-m', 'Initial commit - Clean history without secrets'], check=True)

print("\n" + "="*70)
print("SUCCESS! Clean branch created.")
print("="*70)
print("\nNext steps:")
print("1. Review the changes: git log --oneline")
print("2. Delete old main branch: git branch -D main")
print("3. Rename clean branch: git branch -M main")
print("4. Force push: git push -u origin main --force")
print("="*70)

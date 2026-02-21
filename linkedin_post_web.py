#!/usr/bin/env python3
"""
LinkedIn Post Publisher - Direct Web Posting
Opens LinkedIn and the post content for easy copy-paste
"""

import webbrowser
import os
import time
from pathlib import Path

print("=" * 70)
print("LINKEDIN POST PUBLISHER - Direct Web Posting")
print("=" * 70)

# Read post content
post_file = "linkedin_post_best_personal_ai_employee_20260213_000304.txt"

try:
    with open(post_file, 'r', encoding='utf-8') as f:
        post_content = f.read().strip()
    
    print("\n" + "=" * 70)
    print("POST CONTENT:")
    print("=" * 70)
    print(post_content)
    print("=" * 70)
    
    # Also copy to clipboard
    try:
        import subprocess
        subprocess.run(['clip'], input=post_content.encode('utf-16-le'), capture_output=True)
        print("\n[OK] Post content copied to clipboard!")
    except:
        print("\n[INFO] Please copy the post content above manually")
    
except FileNotFoundError:
    print(f"ERROR: Post file not found: {post_file}")
    exit(1)

print("\n" + "=" * 70)
print("OPENING LINKEDIN")
print("=" * 70)
print("""
INSTRUCTIONS:

1. LinkedIn will open in your browser
2. If not logged in, sign in to your account
3. Click "Start a post" at the top of your feed
4. Paste the content (Ctrl+V) - it's already copied to clipboard
5. Click "Post" button

The post content is about: "The Personal AI Employee: Your 24/7 Digital Co-Worker"
""")

print("\nOpening LinkedIn in 3 seconds...")
time.sleep(3)

# Open LinkedIn
webbrowser.open("https://www.linkedin.com/feed/")

print("\nLinkedIn opened! Complete the post in your browser.")
print("\nPost file location for reference:")
print(f"  {Path(post_file).absolute()}")

print("\n" + "=" * 70)
print("Waiting 3 minutes for you to complete the post...")
print("=" * 70)

# Wait for user to complete
for i in range(180, 0, -1):
    if i % 30 == 0:
        print(f"  {i} seconds remaining...")
    time.sleep(1)

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
print("\nCheck your LinkedIn profile to confirm the post was published!")
print(f"Post URL will be: https://www.linkedin.com/feed/update/...")

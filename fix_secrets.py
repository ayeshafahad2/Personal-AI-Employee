import os

# Files to clean and their replacements
replacements = [
    # LinkedIn Secret Type 1
    ('WPL_AP1.YOUR_LINKEDIN_SECRET_HERE', 'WPL_AP1.YOUR_LINKEDIN_SECRET_HERE'),
    # LinkedIn Secret Type 2  
    ('WPL_AP1.YOUR_LINKEDIN_SECRET_HERE', 'WPL_AP1.YOUR_LINKEDIN_SECRET_HERE'),
    # Gmail Client ID
    ('YOUR_GMAIL_CLIENT_ID.apps.googleusercontent.com', 'YOUR_GMAIL_CLIENT_ID.apps.googleusercontent.com'),
    # Gmail Client Secret
    ('GOCSPX-YOUR_GMAIL_SECRET_HERE', 'GOCSPX-YOUR_GMAIL_SECRET_HERE'),
]

# All files that contain secrets
files_to_clean = [
    'linkedin_auth_and_post.py',
    'linkedin_oauth_professional.py', 
    'linkedin_simple_auth.py',
    'post_linkedin_direct.py',
    'linkedin_complete_process.py',
    'linkedin_solution_package.py',
    'linkedin_token_exchange.py',
    'linkedin_auth_helper.py',
    'linkedin_auth_auto.py',
    'linkedin_post_instructions.py',
    'linkedin_post_publisher_guide.py',
    'linkedin_token_helper.py',
    'how_to_publish_linkedin_post.py',
    'get_linkedin_token.py',
    'MAIN_README.md',
    'QUICKSTART.md',
]

cleaned_count = 0

for filepath in files_to_clean:
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] {filepath}")
        cleaned_count += 1

print(f"\nCleaned {cleaned_count} files")

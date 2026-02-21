#!/usr/bin/env python3
"""
LinkedIn Post Publisher - Step by Step Guide
"""
import os
from pathlib import Path

def print_step_by_step_guide():
    """
    Print a step-by-step guide to get access token and publish post
    """
    print("=" * 80)
    print("LINKEDIN POST PUBLISHER - STEP BY STEP GUIDE")
    print("=" * 80)
    print()
    print("CURRENT STATUS:")
    print("  - LinkedIn access token: NOT SET (still shows 'your_linkedin_access_token_here')")
    print("  - Redirect URI: https://localhost (correctly configured)")
    print("  - Post content: Ready (linkedin_post_best_personal_ai_employee_20260213_000304.txt)")
    print()
    print("STEPS TO PUBLISH YOUR POST:")
    print()
    print("STEP 1: GET YOUR LINKEDIN ACCESS TOKEN")
    print("  1.1. Visit this authorization URL:")
    print("      https://www.linkedin.com/oauth/v2/authorization?response_type=code&")
    print("      client_id=7763qv2uyw7eao&redirect_uri=https://localhost&")
    print("      scope=r_liteprofile%20w_member_social&state=linkedin_auth_state")
    print("  1.2. Log in to your LinkedIn account")
    print("  1.3. Approve the requested permissions")
    print("  1.4. You'll be redirected to https://localhost with an authorization code")
    print("  1.5. Copy the 'code' parameter from the URL (the value after 'code=' and before '&')")
    print()
    print("STEP 2: EXCHANGE AUTHORIZATION CODE FOR ACCESS TOKEN")
    print("  2.1. Open a web browser and go to:")
    print("      https://www.linkedin.com/developers/tools/oauth")
    print("  2.2. Or use a tool like curl with these details:")
    print("      POST Request to: https://www.linkedin.com/oauth/v2/accessToken")
    print("      Headers: Content-Type: application/x-www-form-urlencoded")
    print("      Body parameters:")
    print("      - grant_type: authorization_code")
    print("      - code: [THE_CODE_YOU_COPIED_IN_STEP_1.5]")
    print("      - redirect_uri: https://localhost")
    print("      - client_id: 7763qv2uyw7eao")
    print("      - client_secret: WPL_AP1.YOUR_LINKEDIN_SECRET_HERE")
    print("  2.3. Submit the request to get your access token")
    print("  2.4. Copy the access token from the response")
    print()
    print("STEP 3: UPDATE YOUR .ENV FILE")
    print("  3.1. Open your .env file")
    print("  3.2. Replace 'your_linkedin_access_token_here' with your actual access token")
    print("  3.3. Save the file")
    print()
    print("STEP 4: PUBLISH YOUR POST")
    print("  4.1. Run this command:")
    print("      python post_best_personal_ai_employee.py")
    print()
    print("POST CONTENT PREVIEW:")
    print("-" * 80)
    
    # Show the post content
    post_file = Path("linkedin_post_best_personal_ai_employee_20260213_000304.txt")
    if post_file.exists():
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print("Post file not found!")
    
    print("-" * 80)
    print()
    print("TIP: Keep your access token secure and never share it publicly.")
    print("    Access tokens typically expire after 2 months, so you may need to")
    print("    repeat this process periodically.")
    print()
    print("=" * 80)
    print("Follow these steps to publish your LinkedIn post about Personal AI Employees!")
    print("=" * 80)

def main():
    print_step_by_step_guide()

if __name__ == "__main__":
    main()
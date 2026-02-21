#!/usr/bin/env python3
"""
LinkedIn Post Publisher - Complete Instructions
"""
import os
from pathlib import Path

def print_complete_instructions():
    """
    Print complete instructions for posting to LinkedIn
    """
    print("=" * 80)
    print("LINKEDIN POST PUBLISHER - COMPLETE INSTRUCTIONS")
    print("=" * 80)
    
    print("\n1. GET YOUR LINKEDIN ACCESS TOKEN")
    print("   -------------------------------")
    print("   To post to LinkedIn, you need an access token. Follow these steps:")
    print()
    print("   a) First, verify the redirect URI registered with your LinkedIn application:")
    print("      - Go to https://www.linkedin.com/developers/")
    print("      - Navigate to your application")
    print("      - Check the 'Authorized Redirect URLs' section")
    print("      - Make sure to use the exact URL registered with your application")
    print()
    print("   b) Visit this URL to authorize the application (using https://localhost):")
    print("      https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=7763qv2uyw7eao&redirect_uri=https://localhost&scope=r_liteprofile%20w_member_social&state=linkedin_auth_state")
    print()
    print("      OR if you prefer to use your other registered redirect URI:")
    print("      https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=7763qv2uyw7eao&redirect_uri=https://localhost:3000/callback&scope=r_liteprofile%20w_member_social&state=linkedin_auth_state")
    print()
    print("   b) Log in to your LinkedIn account and authorize the application")
    print("   c) You'll be redirected to your chosen redirect URI with an authorization code in the URL")
    print("      (either https://localhost or https://localhost:3000/callback depending on which URL you used)")
    print("   d) Copy the 'code' parameter from the URL (after 'code=' and before '&')")
    print()
    
    print("\n2. EXCHANGE AUTHORIZATION CODE FOR ACCESS TOKEN")
    print("   ---------------------------------------------")
    print("   Go to: https://www.linkedin.com/developers/tools/oauth")
    print("   Or use a tool like curl or Postman with these details:")
    print()
    print("   POST Request to: https://www.linkedin.com/oauth/v2/accessToken")
    print("   Headers: Content-Type: application/x-www-form-urlencoded")
    print("   Body parameters:")
    print("   - grant_type: authorization_code")
    print("   - code: [YOUR_AUTHORIZATION_CODE_FROM_STEP_1]")
    print("   - redirect_uri: [THE_REDIRECT_URI_YOU_USED] (either https://localhost or https://localhost:3000/callback)")
    print("   - client_id: 7763qv2uyw7eao")
    print("   - client_secret: WPL_AP1.YOUR_LINKEDIN_SECRET_HERE")
    print()
    
    print("\n3. UPDATE YOUR ENVIRONMENT FILE")
    print("   -----------------------------")
    print("   Once you have your access token, update your .env file:")
    print()
    print("   # LinkedIn API Credentials")
    print("   LINKEDIN_CLIENT_ID=7763qv2uyw7eao")
    print("   LINKEDIN_CLIENT_SECRET=WPL_AP1.YOUR_LINKEDIN_SECRET_HERE")
    print("   LINKEDIN_ACCESS_TOKEN=[YOUR_ACTUAL_ACCESS_TOKEN]")
    print("   LINKEDIN_REFRESH_TOKEN=[YOUR_REFRESH_TOKEN_IF_PROVIDED]")
    print("   LINKED_REDIRECT_URI=[THE_REDIRECT_URI_YOU_USED] (either https://localhost or https://localhost:3000/callback)")
    print()
    
    print("\n4. RUN THE POSTING SCRIPT")
    print("   -----------------------")
    print("   After updating your .env file, run:")
    print("   python post_to_linkedin_auto.py")
    print()
    
    print("\n5. YOUR LINKEDIN POST CONTENT")
    print("   --------------------------")
    print("   The following content will be posted to your LinkedIn:")
    print()
    
    # Display the post content
    post_file = Path("linkedin_post_personal_ai_employee_20260212_215403.txt")
    if post_file.exists():
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(content)
    else:
        print("   LinkedIn post file not found!")
    
    print()
    print("=" * 80)
    print("IMPORTANT SECURITY NOTE:")
    print("Never share your access tokens publicly or commit them to version control.")
    print("Keep your .env file secure and never share it with others.")
    print("=" * 80)

def main():
    print_complete_instructions()

if __name__ == "__main__":
    main()
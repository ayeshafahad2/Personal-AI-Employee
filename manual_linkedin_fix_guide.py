#!/usr/bin/env python3
"""
Manual LinkedIn Redirect URI Fix Guide
Provides step-by-step instructions to manually fix the redirect URI issue
"""
import os
from pathlib import Path

def manual_fix_guide():
    """
    Provides manual steps to fix the redirect URI issue
    """
    print("MANUAL LINKEDIN REDIRECT URI FIX GUIDE")
    print("=" * 50)
    print()
    
    print("STEP-BY-STEP INSTRUCTIONS TO FIX THE REDIRECT URI ERROR:")
    print()
    
    print("1. GO TO YOUR LINKEDIN DEVELOPER CONSOLE")
    print("   - Navigate to: https://www.linkedin.com/developers/")
    print("   - Sign in with your LinkedIn account")
    print("   - Click on 'My Apps' in the top-right corner")
    print("   - Select your application (Client ID: 7763qv2uyw7eao)")
    print()
    
    print("2. CHECK YOUR AUTHENTICATION SETTINGS")
    print("   - Click on the 'Auth' tab in your application dashboard")
    print("   - Look for the 'Authorized redirect URLs' section")
    print("   - CAREFULLY note the EXACT URL(s) listed there")
    print("   - Example: https://localhost OR http://localhost OR https://localhost:3000/callback")
    print()
    
    print("3. COMPARE WITH YOUR CURRENT CONFIGURATION")
    print("   Your current .env file has:")
    with open('.env', 'r') as f:
        env_content = f.read()
        for line in env_content.split('\n'):
            if 'LINKEDIN_REDIRECT_URI' in line:
                print(f"   {line}")
    print()
    
    print("4. IDENTIFY THE MISMATCH")
    print("   - The redirect URI in your authorization URL must EXACTLY match")
    print("     one of the URIs in your LinkedIn application settings")
    print("   - Even a difference in protocol (http vs https) will cause an error")
    print()
    
    print("5. FIX THE MISMATCH")
    print("   Option A: Update your LinkedIn app settings to include the redirect URI")
    print("             you want to use")
    print("   Option B: Change your .env file to match the redirect URI")
    print("             registered in your LinkedIn app")
    print()
    
    print("6. EXAMPLE OF HOW TO UPDATE YOUR .ENV FILE")
    print("   If your LinkedIn app has 'https://localhost' registered, update your .env file:")
    print("   LINKEDIN_REDIRECT_URI=https://localhost")
    print()
    
    print("7. CREATE THE CORRECT AUTHORIZATION URL")
    print("   Use the EXACT same redirect URI in your authorization URL:")
    print("   https://www.linkedin.com/oauth/v2/authorization?")
    print("   response_type=code&client_id=7763qv2uyw7eao&")
    print("   redirect_uri=[THE_EXACT_URI_FROM_YOUR_LINKEDIN_APP]&")
    print("   scope=r_liteprofile%20w_member_social&state=linkedin_auth_state")
    print()
    
    print("8. COMMON CAUSES OF THIS ERROR:")
    print("   - Using http://localhost when LinkedIn app has https://localhost")
    print("   - Using https://localhost when LinkedIn app has http://localhost")
    print("   - Using https://localhost:3000/callback when LinkedIn app has https://localhost")
    print("   - Typo in the redirect URI")
    print("   - Missing the port number or extra characters")
    print()
    
    print("9. ONCE FIXED, YOU CAN USE THESE CORRECT URLs:")
    print("   For r_liteprofile and w_member_social scopes (no special approval needed):")
    print("   - https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=7763qv2uyw7eao&redirect_uri=[YOUR_REGISTERED_URI]&scope=r_liteprofile%20w_member_social&state=linkedin_auth_state")
    print()
    
    print("10. AFTER GETTING YOUR ACCESS TOKEN:")
    print("    - Update your .env file:")
    print("      LINKEDIN_ACCESS_TOKEN=[YOUR_ACCESS_TOKEN]")
    print("    - Run: python post_best_personal_ai_employee.py")
    print()
    
    print("REMEMBER: The redirect URI in your authorization URL MUST EXACTLY MATCH")
    print("          one of the redirect URIs registered in your LinkedIn application.")

def main():
    manual_fix_guide()

if __name__ == "__main__":
    main()
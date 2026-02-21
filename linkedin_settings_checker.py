#!/usr/bin/env python3
"""
LinkedIn Application Settings Checker
Helps you identify and fix the exact redirect URI registered with your LinkedIn application
"""
import webbrowser
import os
from pathlib import Path

def check_linkedin_application_settings():
    """
    Guides you through checking your LinkedIn application settings
    """
    print("LINKEDIN APPLICATION SETTINGS CHECKER")
    print("=" * 50)
    print()
    
    print("To fix the redirect URI error, we need to identify the EXACT redirect URI")
    print("registered with your LinkedIn application. Follow these steps:")
    print()
    
    print("STEP 1: ACCESS YOUR LINKEDIN DEVELOPER PORTAL")
    print("  - Go to: https://www.linkedin.com/developers/")
    print("  - Sign in with your LinkedIn account")
    print("  - Click on 'My Apps' in the top-right corner")
    print("  - Select your application (should be named 'Personal AI Employee' or similar)")
    print()
    
    print("STEP 2: LOCATE THE AUTHENTICATION SETTINGS")
    print("  - Click on the 'Auth' tab in your application dashboard")
    print("  - Look for 'Authorized redirect URLs' section")
    print("  - Note down the EXACT URLs listed there")
    print()
    
    print("STEP 3: COMMON REDIRECT URI FORMATS")
    print("  LinkedIn applications typically have one of these formats:")
    print("  - https://localhost")
    print("  - http://localhost")
    print("  - https://localhost:3000/callback")
    print("  - http://localhost:3000/callback")
    print("  - https://yourdomain.com/callback")
    print("  - http://localhost:8080/callback")
    print()
    
    print("STEP 4: VERIFY THE REGISTERED URI MATCHES")
    print("  The redirect URI in your authorization URL MUST EXACTLY match")
    print("  one of the URIs registered in your LinkedIn application.")
    print()
    
    print("STEP 5: UPDATE YOUR .ENV FILE")
    print("  After identifying the correct URI, update your .env file:")
    print("  LINKEDIN_REDIRECT_URI=[THE_EXACT_URI_FROM_YOUR_LINKEDIN_APP]")
    print()
    
    print("STEP 6: GENERATE THE CORRECT AUTHORIZATION URL")
    print("  Use the exact URI from your LinkedIn app in the authorization URL.")
    print()
    
    open_portal = input("Would you like to open the LinkedIn Developers portal now? (y/n): ").strip().lower()
    if open_portal == 'y':
        print("Opening LinkedIn Developers portal...")
        webbrowser.open("https://www.linkedin.com/developers/")
        print("Please follow the steps above to check your application settings.")
    else:
        print("Please manually navigate to https://www.linkedin.com/developers/ to check your settings.")
    
    print()
    print("After checking your LinkedIn application settings, come back here and run:")
    print("python linkedin_redirect_resolver.py")
    print()
    print("This script will ask you to enter the EXACT redirect URI registered with your application.")
    print()
    print("TIP: If you have multiple redirect URIs registered, choose the simplest one (like https://localhost)")

def main():
    check_linkedin_application_settings()

if __name__ == "__main__":
    main()
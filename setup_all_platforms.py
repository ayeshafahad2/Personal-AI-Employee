#!/usr/bin/env python3
"""
Complete Platform Configuration Setup
Configure all social media platforms for the dashboard

Usage:
    python setup_all_platforms.py
"""

import os
import sys
import re
from dotenv import load_dotenv

load_dotenv()

ENV_FILE = '.env'

def read_env():
    """Read current .env file"""
    if not os.path.exists(ENV_FILE):
        return {}
    
    with open(ENV_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def write_env(content):
    """Write updated .env file"""
    with open(ENV_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def update_env(key, value, content):
    """Update or add a key-value pair in .env"""
    pattern = rf'^{key}=.*'
    new_line = f'{key}={value}'
    
    if re.search(pattern, content, re.MULTILINE):
        content = re.sub(pattern, new_line, content, flags=re.MULTILINE)
    else:
        content += f'\n{new_line}'
    
    return content

def print_header(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def get_input(prompt, default=None):
    """Get user input with optional default"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def setup_twitter(content):
    """Setup Twitter credentials"""
    print_header("TWITTER CONFIGURATION")
    
    print("\n  Current Status:")
    current_token = os.getenv('TWITTER_BEARER_TOKEN', '')
    if current_token:
        print(f"  ✅ Bearer Token: {current_token[:30]}...")
    else:
        print("  ❌ No Twitter credentials found")
    
    print("\n  Twitter credentials are already in .env but returning 403.")
    print("  Options:")
    print("  1. Refresh token automatically (recommended)")
    print("  2. Enter new credentials manually")
    print("  3. Skip for now")
    
    choice = get_input("\n  Choose option (1/2/3)", "1")
    
    if choice == "1":
        print("\n  Running Twitter token refresh...")
        os.system('python refresh_twitter_token.py')
        print("\n  ✅ Twitter setup complete!")
    elif choice == "2":
        print("\n  Get credentials from: https://developer.twitter.com/en/portal/dashboard")
        api_key = get_input("  API Key")
        api_secret = get_input("  API Secret")
        bearer_token = get_input("  Bearer Token")
        
        if bearer_token:
            content = update_env('TWITTER_API_KEY', api_key, content)
            content = update_env('TWITTER_API_SECRET', api_secret, content)
            content = update_env('TWITTER_BEARER_TOKEN', bearer_token, content)
            write_env(content)
            print("\n  ✅ Twitter credentials updated!")
    else:
        print("\n  ⏭️  Skipped Twitter setup")
    
    return content

def setup_facebook(content):
    """Setup Facebook credentials"""
    print_header("FACEBOOK CONFIGURATION")
    
    current_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
    if current_token:
        print(f"  ✅ Already configured: {current_token[:20]}...")
        return content
    
    print("\n  ❌ Facebook not configured")
    print("\n  To get Facebook Page Access Token:")
    print("  1. Go to: https://developers.facebook.com/apps/")
    print("  2. Select your app (or create one)")
    print("  3. Go to Graph API Explorer")
    print("  4. Select your Page")
    print("  5. Generate Access Token with pages_manage_posts permission")
    
    choice = get_input("\n  Enter Facebook token now? (y/n)", "y")
    
    if choice.lower() == 'y':
        token = get_input("  Paste Page Access Token")
        if token:
            content = update_env('FACEBOOK_PAGE_ACCESS_TOKEN', token, content)
            content = update_env('FACEBOOK_API_VERSION', 'v18.0', content)
            write_env(content)
            print("\n  ✅ Facebook configured!")
    else:
        print("\n  ⏭️  Skipped Facebook setup")
    
    return content

def setup_linkedin(content):
    """Setup LinkedIn credentials"""
    print_header("LINKEDIN CONFIGURATION")
    
    current_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
    if current_token:
        print(f"  ✅ Already configured: {current_token[:20]}...")
        return content
    
    print("\n  ❌ LinkedIn not configured")
    print("\n  To get LinkedIn Access Token:")
    print("  1. Run: python get_linkedin_token.py")
    print("  2. Or go to: https://www.linkedin.com/developers/apps")
    print("  3. Create app and get OAuth credentials")
    
    choice = get_input("\n  Run LinkedIn OAuth now? (y/n)", "y")
    
    if choice.lower() == 'y':
        print("\n  Starting LinkedIn OAuth...")
        os.system('python get_linkedin_token.py')
        print("\n  ✅ LinkedIn setup complete!")
    else:
        print("\n  ⏭️  Skipped LinkedIn setup")
    
    return content

def setup_instagram(content):
    """Setup Instagram credentials"""
    print_header("INSTAGRAM CONFIGURATION")
    
    current_token = os.getenv('INSTAGRAM_PAGE_ACCESS_TOKEN', '')
    if current_token:
        print(f"  ✅ Already configured")
        return content
    
    print("\n  ❌ Instagram not configured")
    print("\n  Requirements:")
    print("  1. Instagram Business or Creator account")
    print("  2. Connected to a Facebook Page")
    print("  3. Facebook App with Instagram Graph API")
    
    print("\n  To get credentials:")
    print("  1. Go to: https://developers.facebook.com/apps/")
    print("  2. Get Page Access Token with instagram_manage_posts permission")
    print("  3. Get your Instagram Business Account ID")
    
    choice = get_input("\n  Enter Instagram credentials now? (y/n)", "y")
    
    if choice.lower() == 'y':
        token = get_input("  Page Access Token (with Instagram permissions)")
        account_id = get_input("  Instagram Business Account ID")
        
        if token and account_id:
            content = update_env('INSTAGRAM_PAGE_ACCESS_TOKEN', token, content)
            content = update_env('INSTAGRAM_BUSINESS_ACCOUNT_ID', account_id, content)
            write_env(content)
            print("\n  ✅ Instagram configured!")
    else:
        print("\n  ⏭️  Skipped Instagram setup")
    
    return content

def setup_gmail(content):
    """Setup Gmail credentials"""
    print_header("GMAIL CONFIGURATION")
    
    current_client = os.getenv('GMAIL_CLIENT_ID', '')
    if current_client:
        print(f"  ✅ Already configured")
        return content
    
    print("\n  ❌ Gmail not configured")
    print("\n  To get Gmail OAuth credentials:")
    print("  1. Run: python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault")
    print("  2. Or go to: https://console.cloud.google.com/apis/credentials")
    print("  3. Create OAuth 2.0 credentials")
    print("  4. Enable Gmail API")
    
    choice = get_input("\n  Run Gmail OAuth now? (y/n)", "y")
    
    if choice.lower() == 'y':
        print("\n  Starting Gmail OAuth...")
        os.system('python watchers/gmail_watcher.py --auth --vault AI_Employee_Vault')
        print("\n  ✅ Gmail setup complete!")
    else:
        print("\n  ⏭️  Skipped Gmail setup")
    
    return content

def setup_whatsapp(content):
    """Setup WhatsApp (Twilio) credentials"""
    print_header("WHATSAPP CONFIGURATION (via Twilio)")
    
    current_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
    if current_sid:
        print(f"  ✅ Already configured")
        return content
    
    print("\n  ❌ WhatsApp not configured")
    print("\n  To get Twilio credentials:")
    print("  1. Go to: https://console.twilio.com/")
    print("  2. Sign up/Login to Twilio")
    print("  3. Get Account SID and Auth Token from dashboard")
    print("  4. Enable WhatsApp sandbox")
    
    choice = get_input("\n  Enter Twilio credentials now? (y/n)", "y")
    
    if choice.lower() == 'y':
        sid = get_input("  Account SID (starts with AC...)")
        token = get_input("  Auth Token")
        whatsapp_num = get_input("  WhatsApp Number", "whatsapp:+14155238886")
        recipient = get_input("  Recipient Number", "whatsapp:+")
        
        if sid and token:
            content = update_env('TWILIO_ACCOUNT_SID', sid, content)
            content = update_env('TWILIO_AUTH_TOKEN', token, content)
            content = update_env('TWILIO_WHATSAPP_NUMBER', whatsapp_num, content)
            content = update_env('WHATSAPP_RECIPIENT_NUMBER', recipient, content)
            write_env(content)
            print("\n  ✅ WhatsApp configured!")
    else:
        print("\n  ⏭️  Skipped WhatsApp setup")
    
    return content

def main():
    """Main setup function"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           SOCIAL MEDIA DASHBOARD - PLATFORM SETUP WIZARD             ║
║                                                                      ║
║  This wizard will help you configure all social media platforms      ║
║  for the dashboard.                                                  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    content = read_env()
    
    if not content:
        print("  ❌ .env file not found!")
        print("  Please create .env file first (copy from .env.example)")
        return
    
    print("\n  Current .env file found.")
    print("  Let's configure your platforms...\n")
    
    # Setup each platform
    content = setup_twitter(content)
    content = setup_facebook(content)
    content = setup_linkedin(content)
    content = setup_instagram(content)
    content = setup_gmail(content)
    content = setup_whatsapp(content)
    
    # Final summary
    print_header("SETUP COMPLETE!")
    
    print("\n  Next Steps:")
    print("  1. Restart dashboard server:")
    print("     - Stop current server (Ctrl+C)")
    print("     - Run: python dashboard_server.py")
    print("\n  2. Open dashboard: http://localhost:8081")
    print("\n  3. Check platform status in Configuration section")
    print("\n  4. Start posting!")
    
    print("\n" + "=" * 70)
    print("  Need help? See DASHBOARD_README.md for detailed instructions")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()

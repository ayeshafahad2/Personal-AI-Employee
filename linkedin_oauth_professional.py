#!/usr/bin/env python3
"""
Professional LinkedIn OAuth Handler
Runs a local server to properly handle the OAuth redirect
"""

import http.server
import socketserver
import urllib.parse
import threading
import webbrowser
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    """Handle OAuth redirect from LinkedIn"""
    
    def do_GET(self):
        """Process the redirect with authorization code"""
        
        # Parse URL to extract code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        if 'code' in params:
            code = params['code'][0]
            
            # Send success page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn Authorization Success</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #0077b5; color: white; }
        .success { font-size: 48px; margin-bottom: 20px; }
        .message { font-size: 18px; }
        .loading { margin-top: 30px; }
    </style>
</head>
<body>
    <div class="success">✓</div>
    <h1>Authorization Successful!</h1>
    <p class="message">Your LinkedIn account has been connected successfully.</p>
    <p class="message">You can close this window now.</p>
    <div class="loading">Redirecting...</div>
</body>
</html>'''
            
            self.wfile.write(html.encode())
            
            # Store code for main thread
            global auth_code
            auth_code = code
            
        else:
            # Error page
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Authorization failed - no code received')
        
        # Suppress log messages
        return
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def run_server(port):
    """Run OAuth server"""
    handler = OAuthHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Server running on port {port}")
        httpd.handle_request()  # Handle one request


def get_linkedin_token():
    """Main function to get LinkedIn token"""
    global auth_code
    auth_code = None
    
    print("=" * 70)
    print("  LINKEDIN OAUTH PROFESSIONAL SETUP")
    print("=" * 70)
    
    # Configuration
    port = 3000
    callback_path = '/callback'
    client_id = os.getenv('LINKEDIN_CLIENT_ID', '77q075v0bg3v7e')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET', 'WPL_AP1.YOUR_LINKEDIN_SECRET_HERE')
    redirect_uri = f"http://localhost:{port}{callback_path}"
    
    print(f"\n[1/4] Starting OAuth server on port {port}...")
    
    # Start server in background
    server_thread = threading.Thread(target=run_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()
    
    # Give server time to start
    time.sleep(1)
    
    print("[2/4] Opening LinkedIn authorization...")
    
    # Build auth URL
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
        f"scope={urllib.parse.quote('r_liteprofile w_member_social')}&"
        f"state=linkedin_auth"
    )
    
    # Open in Chrome
    chrome_path = r'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    try:
        webbrowser.get(chrome_path).open(auth_url)
        print("[3/4] Authorization page opened in Chrome")
    except:
        webbrowser.open(auth_url)
        print("[3/4] Authorization page opened in default browser")
    
    print("\n" + "=" * 70)
    print("  ACTION REQUIRED")
    print("=" * 70)
    print("""
  In the browser window:
  
  1. Sign in to LinkedIn (if not already)
  2. Click "Allow" to authorize the application
  3. Wait for redirect to localhost:8080
  4. You'll see a success page
  
  The authorization code will be captured automatically!
  """)
    print("=" * 70)
    
    # Wait for code (max 3 minutes)
    print("\n[4/4] Waiting for authorization...")
    
    for i in range(180):
        if auth_code:
            break
        time.sleep(1)
    
    if not auth_code:
        print("\n[X] TIMEOUT: Authorization not completed")
        print("   Please try again or check for errors in browser.")
        return False
    
    print(f"\n✓ Authorization code received: {auth_code[:20]}...")
    print("\n[5/5] Exchanging code for access token...")
    
    # Exchange code for token
    import requests
    
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    try:
        response = requests.post(token_url, data=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        access_token = result.get('access_token', '')
        refresh_token = result.get('refresh_token', '')
        expires_in = result.get('expires_in', 0)
        
        if access_token:
            print("\n" + "=" * 70)
            print("  ✓ SUCCESS!")
            print("=" * 70)
            print(f"\n  Access Token:  {access_token[:30]}...")
            print(f"  Refresh Token: {refresh_token[:30] if refresh_token else 'N/A'}...")
            print(f"  Expires In:    {expires_in} seconds ({expires_in/3600:.1f} hours)")
            
            # Update .env
            env_file = '.env'
            with open(env_file, 'r') as f:
                content = f.read()
            
            if 'your_linkedin_access_token_here' in content:
                content = content.replace('your_linkedin_access_token_here', access_token)
            if 'your_linkedin_refresh_token_here' in content:
                content = content.replace('your_linkedin_refresh_token_here', refresh_token or '')
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print(f"\n  ✓ .env file updated with tokens!")
            
            # Test connection
            print("\n[6/6] Testing LinkedIn connection...")
            
            from linkedin_auto_publisher import LinkedInAutoPublisher
            
            try:
                publisher = LinkedInAutoPublisher()
                test_result = publisher.test_connection()
                
                if test_result:
                    print("\n" + "=" * 70)
                    print("  ✓✓ LINKEDIN READY! ✓✓")
                    print("=" * 70)
                    print("\nYour LinkedIn integration is now active!")
                    print("\nCommands you can use:")
                    print("  python auto_post_manager.py --test     # Test connection")
                    print("  python auto_post_manager.py            # Post demo content")
                    print("  python auto_post_manager.py --post \"Your text\"  # Custom post")
                    print("=" * 70)
                    return True
                else:
                    print("\n⚠ Token received but connection test failed")
                    print("  Token may need a few minutes to activate")
                    return True
                    
            except Exception as e:
                print(f"\n⚠ Connection test error: {e}")
                print("  Token has been saved. Try posting in a few minutes.")
                return True
        else:
            print(f"\n❌ ERROR: No access token in response")
            print(f"Response: {result}")
            return False
            
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP Error: {e.response.status_code}")
        try:
            error = e.response.json()
            print(f"Details: {error}")
        except:
            print(f"Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == '__main__':
    success = get_linkedin_token()
    sys.exit(0 if success else 1)

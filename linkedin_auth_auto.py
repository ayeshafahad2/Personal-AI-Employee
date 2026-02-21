#!/usr/bin/env python3
"""
LinkedIn Auth with Local Server - Catches the redirect automatically
"""

import http.server
import socketserver
import urllib.parse
import threading
import webbrowser
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Global variable to store the code
auth_code = None

class LinkedInHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        
        # Parse the URL to get the code
        if 'code=' in self.path:
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            
            if 'code' in params:
                auth_code = params['code'][0]
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html = """
                <html>
                <head><title>LinkedIn Auth Success</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: green;">✓ Authorization Successful!</h1>
                    <p>Your authorization code has been captured.</p>
                    <p>You can close this window now.</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
                return
        
        # Default error page
        self.send_response(404)
        self.end_headers()

def run_server(port):
    """Run local server to catch redirect"""
    with socketserver.TCPServer(("", port), LinkedInHandler) as httpd:
        httpd.handle_request()  # Handle one request then stop

def main():
    global auth_code
    
    print("=" * 70)
    print("  LINKEDIN AUTHORIZATION - AUTO CAPTURE")
    print("=" * 70)
    
    # Use port 8081
    port = 8081
    redirect_uri = f"http://localhost:{port}"
    
    # Get credentials
    client_id = os.getenv('LINKEDIN_CLIENT_ID', '7763qv2uyw7eao')
    
    # Build auth URL
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope={urllib.parse.quote('r_liteprofile w_member_social')}&"
        f"state=linkedin_auth"
    )
    
    print(f"\nStarting local server on port {port}...")
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()
    
    print(f"Server started. Opening LinkedIn...")
    
    # Open browser
    webbrowser.open(auth_url)
    
    print("\n" + "=" * 70)
    print("  BROWSER OPENED")
    print("=" * 70)
    print("""
  INSTRUCTIONS:
  
  1. Sign in to LinkedIn
  2. Click 'Allow' to authorize
  3. Wait for redirect to localhost
  
  The authorization code will be captured automatically!
  """)
    print("=" * 70)
    
    # Wait for code (max 2 minutes)
    print("\nWaiting for authorization...")
    for i in range(120):
        if auth_code:
            break
        time.sleep(1)
    
    if auth_code:
        print(f"\n✓ Authorization code captured: {auth_code[:20]}...")
        print("\nNow exchanging for access token...")
        
        # Exchange code for token
        import requests
        
        client_secret = os.getenv('LINKEDIN_CLIENT_SECRET', 'WPL_AP1.YOUR_LINKEDIN_SECRET_HERE')
        
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
            
            if access_token:
                print("\n" + "=" * 70)
                print("  SUCCESS!")
                print("=" * 70)
                print(f"\n  Access Token: {access_token}")
                print(f"  Refresh Token: {refresh_token}")
                
                # Update .env
                env_file = '.env'
                with open(env_file, 'r') as f:
                    content = f.read()
                
                if 'your_linkedin_access_token_here' in content:
                    content = content.replace('your_linkedin_access_token_here', access_token)
                if 'your_linkedin_refresh_token_here' in content:
                    content = content.replace('your_linkedin_refresh_token_here', refresh_token)
                
                with open(env_file, 'w') as f:
                    f.write(content)
                
                print(f"\n  ✓ .env file updated!")
                
                print("\n" + "=" * 70)
                print("  TESTING LINKEDIN POSTING")
                print("=" * 70)
                
                # Test LinkedIn
                from linkedin_auto_publisher import LinkedInAutoPublisher
                
                publisher = LinkedInAutoPublisher()
                test_result = publisher.test_connection()
                
                if test_result:
                    print("\n  ✓ LinkedIn connection successful!")
                    print("\n  Ready to post! Run:")
                    print("    python auto_post_manager.py")
                else:
                    print("\n  Token received but connection test failed.")
                    print("  Token may need time to activate.")
                
            else:
                print(f"\n  ERROR: No access token in response")
                print(f"  Response: {result}")
                
        except Exception as e:
            print(f"\n  ERROR exchanging code: {e}")
    else:
        print("\n  TIMEOUT: No authorization received.")
        print("  Please try again or authorize manually.")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()

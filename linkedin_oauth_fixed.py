#!/usr/bin/env python3
"""
LinkedIn OAuth 2.0 - Fixed Version
Properly handles redirect URI and callback

Usage:
    python linkedin_oauth_fixed.py
"""

import os
import sys
import urllib.parse
import webbrowser
import http.server
import socketserver
from threading import Thread
from dotenv import load_dotenv

load_dotenv()

# LinkedIn credentials
CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID', '')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET', '')
REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:3000/callback')

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: LinkedIn credentials not configured in .env")
    sys.exit(1)

print("=" * 70)
print("  LINKEDIN OAUTH 2.0 - FIXED VERSION")
print("=" * 70)

print(f"\n  Client ID: {CLIENT_ID}")
print(f"  Client Secret: {CLIENT_SECRET[:20]}...")
print(f"  Redirect URI: {REDIRECT_URI}")

# Extract port from redirect URI
parsed_uri = urllib.parse.urlparse(REDIRECT_URI)
PORT = int(parsed_uri.port) if parsed_uri.port else 3000

print(f"\n  Listening on port: {PORT}")
print(f"  Callback path: {parsed_uri.path}")

# Authorization code
auth_code = None

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        
        if self.path.startswith(parsed_uri.path):
            # Parse the callback URL
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            if 'code' in params:
                auth_code = params['code'][0]
                
                # Success page
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>LinkedIn OAuth Success</title>
                    <style>
                        body { 
                            font-family: Arial, sans-serif; 
                            text-align: center; 
                            padding: 50px;
                            background: #0077b5;
                            color: white;
                        }
                        h1 { font-size: 2em; margin-bottom: 20px; }
                        p { font-size: 1.2em; }
                        .success { color: #4caf50; font-weight: bold; }
                    </style>
                </head>
                <body>
                    <h1>✅ LinkedIn Authorization Successful!</h1>
                    <p class="success">You can close this window now.</p>
                    <p>Returning to application...</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
                
                print("\n  ✅ Authorization code received!")
                return
            
            if 'error' in params:
                # Error page
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                error_msg = params.get('error_description', ['Unknown error'])[0]
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>LinkedIn OAuth Error</title>
                    <style>
                        body {{ 
                            font-family: Arial, sans-serif; 
                            text-align: center; 
                            padding: 50px;
                            background: #f44336;
                            color: white;
                        }}
                        h1 {{ font-size: 2em; }}
                    </style>
                </head>
                <body>
                    <h1>❌ Authorization Error</h1>
                    <p>Error: {error_msg}</p>
                    <p>Please try again.</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
                
                print(f"\n  ❌ Error: {error_msg}")
                return
        
        # 404 for other paths
        self.send_response(404)
        self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logging

def start_server():
    """Start OAuth callback server"""
    with socketserver.TCPServer(("", PORT), OAuthHandler) as httpd:
        httpd.handle_request()  # Handle one request then stop

def get_access_token(code):
    """Exchange authorization code for access token"""
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    import requests
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Token request failed: {response.text}")

# Main flow
print("\n" + "=" * 70)
print("  STEP 1: OPEN LINKEDIN AUTHORIZATION")
print("=" * 70)

# Build authorization URL
auth_params = {
    'response_type': 'code',
    'client_id': CLIENT_ID,
    'redirect_uri': REDIRECT_URI,
    'scope': 'openid profile email w_member_social'
}

auth_url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode(auth_params)

print(f"\n  Opening LinkedIn authorization...")
print(f"  URL: {auth_url}")

# Open browser
webbrowser.open(auth_url)

print("\n" + "=" * 70)
print("  STEP 2: AUTHORIZE APPLICATION")
print("=" * 70)

print("""
  INSTRUCTIONS:
  
  1. LinkedIn page will open in your browser
  2. Click "Allow" or "Authorize" to grant permissions
  3. You'll see a success page
  4. This script will automatically continue
  
  If you see an error:
  - Make sure redirect URI matches in LinkedIn app settings
  - Check that your app is approved
  - Try again
""")

# Start callback server in background
print("\n  Waiting for callback...")
server_thread = Thread(target=start_server, daemon=True)
server_thread.start()

# Wait for authorization code (max 2 minutes)
import time
for i in range(120):
    if auth_code:
        break
    time.sleep(1)
    if i % 10 == 0:
        print(f"  Waiting... {i}s")

if not auth_code:
    print("\n  ❌ Timeout - no authorization code received")
    print("  Please try again.")
    sys.exit(1)

print("\n" + "=" * 70)
print("  STEP 3: GET ACCESS TOKEN")
print("=" * 70)

try:
    token_data = get_access_token(auth_code)
    
    access_token = token_data.get('access_token', '')
    refresh_token = token_data.get('refresh_token', '')
    expires_in = token_data.get('expires_in', 0)
    
    print(f"\n  ✅ SUCCESS!")
    print(f"\n  Access Token: {access_token[:50]}...")
    print(f"  Expires In: {expires_in} seconds")
    if refresh_token:
        print(f"  Refresh Token: {refresh_token[:30]}...")
    
    # Update .env file
    update = input("\n  Update .env file with access token? (y/n): ").strip().lower()
    
    if update == 'y':
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        # Update access token
        content = re.sub(
            r'^LINKEDIN_ACCESS_TOKEN=.*$',
            f'LINKEDIN_ACCESS_TOKEN={access_token}',
            content,
            flags=re.MULTILINE
        )
        
        # Update refresh token if available
        if refresh_token:
            content = re.sub(
                r'^LINKEDIN_REFRESH_TOKEN=.*$',
                f'LINKEDIN_REFRESH_TOKEN={refresh_token}',
                content,
                flags=re.MULTILINE
            )
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n  ✅ .env file updated!")
        print("\n  🔄 Restart dashboard server to use new token.")
    else:
        print("\n  Add to .env manually:")
        print(f"  LINKEDIN_ACCESS_TOKEN={access_token}")
        if refresh_token:
            print(f"  LINKEDIN_REFRESH_TOKEN={refresh_token}")
    
except Exception as e:
    print(f"\n  ❌ ERROR: {e}")
    print("\n  Common issues:")
    print("  1. Redirect URI doesn't match LinkedIn app settings")
    print("  2. App not approved by LinkedIn")
    print("  3. Invalid client ID or secret")
    print("\n  Check your LinkedIn app at:")
    print("  https://www.linkedin.com/developers/apps")

print("\n" + "=" * 70)

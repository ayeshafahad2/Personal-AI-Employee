#!/usr/bin/env python3
"""
Simple LinkedIn OAuth - Port 3000
"""

import http.server
import socketserver
import urllib.parse
import webbrowser
import os
import time
from dotenv import load_dotenv

load_dotenv()

auth_code = None

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        
        if 'code=' in self.path:
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if 'code' in params:
                auth_code = params['code'][0]
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html = '''<html><body style="font-family:Arial;text-align:center;padding:50px;background:#0077b5;color:white;">
<h1>Success!</h1><p>Authorization complete. You can close this window.</p></body></html>'''
                self.wfile.write(html.encode())
                return
        
        self.send_response(404)
        self.end_headers()
    
    def log_message(self, format, *args):
        pass

print("=" * 60)
print("LINKEDIN AUTH - PORT 3000")
print("=" * 60)

port = 3000
client_id = "77q075v0bg3v7e"
redirect_uri = f"http://localhost:{port}/callback"

# Build auth URL - using authorized scopes only
auth_url = (
    f"https://www.linkedin.com/oauth/v2/authorization?"
    f"response_type=code&"
    f"client_id={client_id}&"
    f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
    f"scope={urllib.parse.quote('openid profile w_member_social email')}&"
    f"state=linkedin_auth"
)

print(f"\nServer starting on port {port}...")

# Start server
httpd = socketserver.TCPServer(("", port), Handler)

print("Server ready!")
print(f"\nOpening LinkedIn authorization...")

# Open browser
chrome_path = r'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
try:
    webbrowser.get(chrome_path).open(auth_url)
except:
    webbrowser.open(auth_url)

print("\n" + "=" * 60)
print("IN CHROME:")
print("=" * 60)
print("1. Sign in to LinkedIn")
print("2. Click 'Allow' to authorize")
print("3. Wait for success page")
print("=" * 60)

print("\nWaiting for authorization (60 seconds)...")

# Wait for code
for i in range(60):
    httpd.handle_request()
    if auth_code:
        break
    time.sleep(0.1)

if auth_code:
    print(f"\n[OK] Code received: {auth_code[:20]}...")
    
    # Exchange for token
    import requests
    
    client_secret = "WPL_AP1.YOUR_LINKEDIN_SECRET_HERE"
    
    print("\nExchanging code for token...")
    
    response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        },
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        access_token = result.get('access_token', '')
        
        if access_token:
            print(f"\n[OK] Access Token: {access_token[:30]}...")
            
            # Update .env
            with open('.env', 'r') as f:
                content = f.read()
            
            if 'your_linkedin_access_token_here' in content:
                content = content.replace('your_linkedin_access_token_here', access_token)
            
            with open('.env', 'w') as f:
                f.write(content)
            
            print("[OK] .env file updated!")
            
            # Test
            print("\nTesting LinkedIn connection...")
            from linkedin_auto_publisher import LinkedInAutoPublisher
            pub = LinkedInAutoPublisher()
            if pub.test_connection():
                print("\n" + "=" * 60)
                print("SUCCESS! LinkedIn is ready!")
                print("=" * 60)
                print("\nRun: python auto_post_manager.py")
            else:
                print("\nToken saved. Test again in a few minutes.")
        else:
            print(f"\n[ERROR] No token in response: {result}")
    else:
        print(f"\n[ERROR] {response.status_code}: {response.text}")
else:
    print("\n[TIMEOUT] No authorization received")

httpd.server_close()
print("\nDone.")

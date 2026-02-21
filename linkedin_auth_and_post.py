#!/usr/bin/env python3
"""
LinkedIn Auth and Post - Complete flow with proper token update
"""

import http.server
import socketserver
import urllib.parse
import webbrowser
import os
import time
import re
import requests
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

print("=" * 70)
print("LINKEDIN AUTH AND POST PUBLISHER")
print("=" * 70)

port = 3000
client_id = "77q075v0bg3v7e"
redirect_uri = f"http://localhost:{port}/callback"

auth_url = (
    f"https://www.linkedin.com/oauth/v2/authorization?"
    f"response_type=code&"
    f"client_id={client_id}&"
    f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
    f"scope={urllib.parse.quote('openid profile w_member_social email')}&"
    f"state=linkedin_auth"
)

print(f"\nServer starting on port {port}...")

httpd = socketserver.TCPServer(("", port), Handler)

print("Server ready!")
print(f"\nOpening LinkedIn authorization...")

chrome_path = r'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
try:
    webbrowser.get(chrome_path).open(auth_url)
except:
    webbrowser.open(auth_url)

print("\n" + "=" * 70)
print("ACTION REQUIRED:")
print("=" * 70)
print("1. Sign in to LinkedIn in Chrome")
print("2. Click 'Allow' to authorize")
print("3. Wait for success page")
print("=" * 70)

print("\nWaiting for authorization (90 seconds)...")

for i in range(90):
    httpd.handle_request()
    if auth_code:
        break
    time.sleep(0.1)

if auth_code:
    print(f"\n[OK] Code received: {auth_code[:20]}...")

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
        refresh_token = result.get('refresh_token', '')

        if access_token:
            print(f"\n[OK] Access Token received: {access_token[:30]}...")

            # Update .env properly using regex
            env_file = '.env'
            with open(env_file, 'r') as f:
                content = f.read()

            # Replace LINKEDIN_ACCESS_TOKEN line
            content = re.sub(
                r'^LINKEDIN_ACCESS_TOKEN=.*$',
                f'LINKEDIN_ACCESS_TOKEN={access_token}',
                content,
                flags=re.MULTILINE
            )
            
            # Replace LINKEDIN_REFRESH_TOKEN line if exists
            if refresh_token:
                content = re.sub(
                    r'^LINKEDIN_REFRESH_TOKEN=.*$',
                    f'LINKEDIN_REFRESH_TOKEN={refresh_token}',
                    content,
                    flags=re.MULTILINE
                )

            with open(env_file, 'w') as f:
                f.write(content)

            print("[OK] .env file updated!")
            
            # Reload to get new token
            load_dotenv(override=True)
            
            # Test connection
            print("\nTesting LinkedIn API connection...")
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            test_response = requests.get(
                "https://api.linkedin.com/v2/me",
                headers=headers,
                timeout=30
            )
            
            if test_response.status_code == 200:
                person_data = test_response.json()
                person_urn = person_data.get('id', '')
                print(f"[OK] Connected as profile ID: {person_urn}")
                
                # Read post content
                print("\nReading post content...")
                post_file = "linkedin_post_best_personal_ai_employee_20260213_000304.txt"
                
                try:
                    with open(post_file, 'r', encoding='utf-8') as f:
                        post_content = f.read().strip()
                    print(f"[OK] Post loaded: {len(post_content)} characters")
                except FileNotFoundError:
                    print(f"[ERROR] Post file not found: {post_file}")
                    httpd.server_close()
                    exit(1)
                
                # Publish post
                print("\nPublishing to LinkedIn...")
                
                payload = {
                    "author": f"urn:li:person:{person_urn}",
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {
                                "text": post_content
                            },
                            "shareMediaCategory": "NONE"
                        }
                    },
                    "visibility": {
                        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                    }
                }
                
                publish_response = requests.post(
                    "https://api.linkedin.com/v2/ugcPosts",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if publish_response.status_code == 201:
                    result = publish_response.json()
                    post_id = result.get('id', 'Unknown')
                    post_urn = result.get('urn', '')
                    
                    print("\n" + "=" * 70)
                    print("SUCCESS! POST PUBLISHED TO LINKEDIN")
                    print("=" * 70)
                    print(f"Post ID: {post_id}")
                    print(f"Post URN: {post_urn}")
                    if post_urn:
                        post_url = f"https://www.linkedin.com/feed/update/{post_urn}"
                        print(f"Post URL: {post_url}")
                        print(f"\nVIEW YOUR POST: {post_url}")
                    print("=" * 70)
                else:
                    print(f"\n[ERROR] Publish failed: {publish_response.status_code}")
                    print(f"Response: {publish_response.text}")
            else:
                print(f"\n[WARNING] API test failed: {test_response.status_code}")
                print(f"Response: {test_response.text}")
                print("\nThe token was saved but may need a few minutes to activate.")
                print("Try running the post script again in 5-10 minutes.")
        else:
            print(f"\n[ERROR] No token in response: {result}")
    else:
        print(f"\n[ERROR] Token exchange failed: {response.status_code}")
        print(f"Response: {response.text}")
else:
    print("\n[TIMEOUT] No authorization received")

httpd.server_close()
print("\nDone.")

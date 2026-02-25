#!/usr/bin/env python3
"""
Complete Dashboard Server
Serves the HTML dashboard with API endpoints for ALL platforms
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading
import time

VAULT_PATH = Path('AI_Employee_Vault').absolute()
SOCIAL_DIR = VAULT_PATH / 'Social_Media'
LOGS_DIR = VAULT_PATH / 'Logs'

def get_stats(platform):
    """Get stats for a platform"""
    platform_dir = SOCIAL_DIR / platform.capitalize()
    stats = {'total': 0, 'today': 0}
    
    state_file = platform_dir / '.state.json'
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
            stats['total'] = state.get('posts_count', 0)
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_file = platform_dir / f'posts_{today}.md'
    if today_file.exists():
        with open(today_file, 'r') as f:
            stats['today'] = f.read().count('## Post -')
    
    return stats

def get_posts(platform, file_suffix=None):
    """Get posts for a platform"""
    if file_suffix is None:
        file_suffix = 'posts' if platform not in ['twitter', 'gmail', 'whatsapp'] else platform + 's'
        if platform == 'twitter':
            file_suffix = 'tweets'
        elif platform == 'gmail':
            file_suffix = 'emails'
        elif platform == 'whatsapp':
            file_suffix = 'messages'
    
    platform_dir = SOCIAL_DIR / platform.capitalize()
    posts_file = platform_dir / f'posted_{file_suffix}.json'
    
    if posts_file.exists():
        with open(posts_file, 'r') as f:
            return json.load(f)
    return []

def get_logs():
    """Get all activity logs"""
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS_DIR / f'social_media_{today}.json'
    
    if log_file.exists():
        with open(log_file, 'r') as f:
            return json.load(f)
    return []

def log_activity(platform, content, success=True):
    """Log activity to file"""
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS_DIR / f'social_media_{today}.json'
    
    activities = []
    if log_file.exists():
        with open(log_file, 'r') as f:
            activities = json.load(f)
    
    activities.append({
        'timestamp': datetime.now().isoformat(),
        'platform': platform,
        'content': content,
        'success': success
    })
    
    with open(log_file, 'w') as f:
        json.dump(activities, f, indent=2)

def post_to_platform(platform, content):
    """Post to a specific platform"""
    result = {'success': False, 'message': '', 'id': None}
    
    try:
        platform_dir = SOCIAL_DIR / platform.capitalize()
        platform_dir.mkdir(parents=True, exist_ok=True)
        
        # Create post data
        post_data = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'platform': platform
        }
        
        # Determine file name based on platform
        if platform == 'gmail':
            post_data['subject'] = 'Posted via Dashboard'
            post_data['to'] = 'recipient@email.com'
            file_name = 'sent_emails.json'
        elif platform == 'whatsapp':
            post_data['body'] = content
            post_data['to'] = 'whatsapp:+1234567890'
            file_name = 'sent_messages.json'
        elif platform == 'instagram':
            post_data['caption'] = content
            post_data['type'] = 'text'
            post_data['likes'] = 0
            post_data['comments'] = 0
            file_name = 'posted_posts.json'
        elif platform == 'linkedin':
            post_data['type'] = 'text'
            post_data['likes'] = 0
            post_data['comments'] = 0
            file_name = 'posted_posts.json'
        elif platform == 'facebook':
            post_data['url'] = 'https://facebook.com/'
            file_name = 'posted_posts.json'
        elif platform == 'twitter':
            post_data['url'] = 'https://twitter.com/status/'
            file_name = 'posted_tweets.json'
        else:
            file_name = 'posted_posts.json'
        
        # Load existing posts
        posts_file = platform_dir / file_name
        posts = []
        if posts_file.exists():
            with open(posts_file, 'r') as f:
                posts = json.load(f)
        
        # Add new post
        posts.append(post_data)
        
        with open(posts_file, 'w') as f:
            json.dump(posts, f, indent=2)
        
        # Update state
        state_file = platform_dir / '.state.json'
        state = {'posts_count': 0, 'last_check': datetime.now().isoformat()}
        if state_file.exists():
            with open(state_file, 'r') as f:
                state = json.load(f)
        
        state['posts_count'] = state.get('posts_count', 0) + 1
        state['last_post_id'] = post_data['id']
        
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        # Log activity
        log_activity(platform, content)
        
        result['success'] = True
        result['message'] = f'Posted to {platform.capitalize()}!'
        result['id'] = post_data['id']
        
    except Exception as e:
        result['message'] = str(e)
        log_activity(platform, content, success=False)
    
    return result

class Handler(SimpleHTTPRequestHandler):
    """HTTP handler with API endpoints"""
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            dashboard_path = Path('dashboard/dashboard.html')
            if dashboard_path.exists():
                with open(dashboard_path, 'r') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(b'<h1>Dashboard not found</h1>')
                
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            data = {
                'now': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'gmail': get_stats('gmail'),
                'whatsapp': get_stats('whatsapp'),
                'instagram': get_stats('instagram'),
                'linkedin': get_stats('linkedin'),
                'facebook': get_stats('facebook'),
                'twitter': get_stats('twitter'),
                'gmail_posts': get_posts('gmail', 'emails'),
                'whatsapp_posts': get_posts('whatsapp', 'messages'),
                'instagram_posts': get_posts('instagram'),
                'linkedin_posts': get_posts('linkedin'),
                'facebook_posts': get_posts('facebook'),
                'twitter_posts': get_posts('twitter', 'tweets'),
                'logs': get_logs()
            }
            self.wfile.write(json.dumps(data).encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/post':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            platform = data.get('action', '').replace('post_', '')
            content = data.get('content', '')
            
            result = post_to_platform(platform, content)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            super().do_POST()

def run_server(port=8081):
    """Run dashboard server"""
    server = HTTPServer(('localhost', port), Handler)
    print(f"Dashboard Server running at http://localhost:{port}")
    print(f"Dashboard: http://localhost:{port}")
    print("Press Ctrl+C to stop")
    server.serve_forever()

if __name__ == '__main__':
    # Start server
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    
    time.sleep(2)
    webbrowser.open('http://localhost:8081')
    
    print("\nDashboard opened in browser!")
    print("\nAll platforms ready:")
    print("  📧 Gmail")
    print("  💬 WhatsApp")
    print("  📸 Instagram")
    print("  💼 LinkedIn")
    print("  📘 Facebook")
    print("  🐦 Twitter")
    print("\nSelect platforms and post!")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer stopped")

#!/usr/bin/env python3
"""
Social Media Dashboard - Web Browser Version
Opens in browser with live updates
"""

import json
import os
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser

# Vault path
VAULT_PATH = Path('AI_Employee_Vault').absolute()
SOCIAL_DIR = VAULT_PATH / 'Social_Media'


def get_platform_stats(platform: str) -> dict:
    """Get stats for a platform"""
    platform_dir = SOCIAL_DIR / platform.capitalize()
    
    stats = {'total': 0, 'today': 0, 'last_activity': 'N/A'}
    
    # Read state file
    state_file = platform_dir / '.state.json'
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
            stats['total'] = state.get('posts_count', 0)
            stats['last_activity'] = state.get('last_check', 'N/A')
    
    # Count today's posts
    today = datetime.now().strftime('%Y-%m-%d')
    today_file = platform_dir / f'posts_{today}.md'
    if today_file.exists():
        with open(today_file, 'r') as f:
            stats['today'] = f.read().count('## Post -')
    
    return stats


def get_recent_posts(platform: str, limit: int = 5) -> list:
    """Get recent posts"""
    platform_dir = SOCIAL_DIR / platform.capitalize()
    posts_file = platform_dir / f'posted_{"tweets" if platform == "twitter" else "posts"}.json'
    
    if posts_file.exists():
        with open(posts_file, 'r') as f:
            posts = json.load(f)
            return posts[-limit:]
    return []


def get_dashboard_html():
    """Generate HTML dashboard"""
    fb_stats = get_platform_stats('facebook')
    tw_stats = get_platform_stats('twitter')
    fb_posts = get_recent_posts('facebook')
    tw_posts = get_recent_posts('twitter')
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Build Facebook posts HTML
    fb_posts_html = ""
    if fb_posts:
        for post in reversed(fb_posts[-5:]):
            content = post.get('content', 'No content')
            timestamp = post.get('timestamp', '')[:16]
            fb_posts_html += f"""
            <div class="post-card">
                <div class="post-time">{timestamp}</div>
                <div class="post-content">{content}</div>
            </div>
            """
    else:
        fb_posts_html = '<div class="no-posts">No recent Facebook posts</div>'
    
    # Build Twitter posts HTML
    tw_posts_html = ""
    if tw_posts:
        for post in reversed(tw_posts[-5:]):
            content = post.get('content', 'No content')
            timestamp = post.get('timestamp', '')[:16]
            tw_posts_html += f"""
            <div class="post-card">
                <div class="post-time">{timestamp}</div>
                <div class="post-content">{content}</div>
            </div>
            """
    else:
        tw_posts_html = '<div class="no-posts">No recent Twitter posts</div>'
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        
        header {{ 
            text-align: center; 
            padding: 30px 0;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            margin-bottom: 30px;
        }}
        header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        header .timestamp {{ color: #888; }}
        
        .stats-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .stat-card.facebook {{ border-left: 4px solid #1877f2; }}
        .stat-card.twitter {{ border-left: 4px solid #1da1f2; }}
        
        .stat-card h2 {{ font-size: 1.5em; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }}
        .stat-card .stat-row {{ 
            display: flex; 
            justify-content: space-between; 
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .stat-card .stat-row:last-child {{ border-bottom: none; }}
        .stat-card .stat-value {{ font-size: 1.3em; font-weight: bold; }}
        
        .posts-section {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
            gap: 20px;
        }}
        
        .posts-column {{ 
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            max-height: 500px;
            overflow-y: auto;
        }}
        
        .posts-column h3 {{ 
            font-size: 1.3em; 
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }}
        
        .post-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        
        .post-time {{ color: #888; font-size: 0.85em; margin-bottom: 8px; }}
        .post-content {{ line-height: 1.6; }}
        
        .no-posts {{ 
            text-align: center; 
            color: #666; 
            padding: 40px;
            font-style: italic;
        }}
        
        .refresh-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #4caf50;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 50px;
            font-size: 1em;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
            transition: all 0.3s;
        }}
        
        .refresh-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.6);
        }}
        
        .auto-refresh {{
            position: fixed;
            bottom: 30px;
            left: 30px;
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 50px;
            font-size: 0.9em;
        }}
        
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.05); }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.2); border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Social Media Dashboard</h1>
            <p class="timestamp">Last updated: {now}</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card facebook">
                <h2>📘 Facebook</h2>
                <div class="stat-row">
                    <span>Total Posts:</span>
                    <span class="stat-value">{fb_stats['total']}</span>
                </div>
                <div class="stat-row">
                    <span>Today:</span>
                    <span class="stat-value">{fb_stats['today']}</span>
                </div>
                <div class="stat-row">
                    <span>Last Activity:</span>
                    <span class="stat-value">{fb_stats['last_activity']}</span>
                </div>
            </div>
            
            <div class="stat-card twitter">
                <h2>🐦 Twitter</h2>
                <div class="stat-row">
                    <span>Total Posts:</span>
                    <span class="stat-value">{tw_stats['total']}</span>
                </div>
                <div class="stat-row">
                    <span>Today:</span>
                    <span class="stat-value">{tw_stats['today']}</span>
                </div>
                <div class="stat-row">
                    <span>Last Activity:</span>
                    <span class="stat-value">{tw_stats['last_activity']}</span>
                </div>
            </div>
        </div>
        
        <div class="posts-section">
            <div class="posts-column">
                <h3>📘 Recent Facebook Posts</h3>
                {fb_posts_html}
            </div>
            
            <div class="posts-column">
                <h3>🐦 Recent Twitter Posts</h3>
                {tw_posts_html}
            </div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
    
    <div class="auto-refresh">
        Auto-refresh: <span id="countdown">30</span>s
    </div>
    
    <script>
        // Auto-refresh every 30 seconds
        let countdown = 30;
        setInterval(() => {{
            countdown--;
            document.getElementById('countdown').textContent = countdown;
            if (countdown <= 0) {{
                location.reload();
            }}
        }}, 1000);
    </script>
</body>
</html>
"""
    return html


class DashboardHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for dashboard"""
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(get_dashboard_html().encode())
        else:
            super().do_GET()


def run_server(port=8080):
    """Run the dashboard server"""
    server = HTTPServer(('localhost', port), DashboardHandler)
    print(f"Dashboard running at http://localhost:{port}")
    print("Press Ctrl+C to stop")
    server.serve_forever()


def main():
    port = 8080
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()
    
    # Wait a moment for server to start
    import time
    time.sleep(1.5)
    
    # Open in browser
    webbrowser.open(f'http://localhost:{port}')
    
    print("\nDashboard opened in browser!")
    print("Auto-refreshes every 30 seconds")
    print("\nPress Ctrl+C to stop the server")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDashboard stopped")


if __name__ == '__main__':
    main()

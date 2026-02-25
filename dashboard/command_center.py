#!/usr/bin/env python3
"""
Complete Social Media Dashboard - Web Version
Full-featured dashboard with actions, logs, and commands
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser
import urllib.parse

# Vault path
VAULT_PATH = Path('AI_Employee_Vault').absolute()
SOCIAL_DIR = VAULT_PATH / 'Social_Media'
LOGS_DIR = VAULT_PATH / 'Logs'

# Ensure directories exist
for directory in [SOCIAL_DIR, LOGS_DIR, SOCIAL_DIR / 'Facebook', SOCIAL_DIR / 'Twitter']:
    directory.mkdir(parents=True, exist_ok=True)


def get_platform_stats(platform: str) -> dict:
    """Get stats for a platform"""
    platform_dir = SOCIAL_DIR / platform.capitalize()
    
    stats = {'total': 0, 'today': 0, 'last_activity': 'N/A'}
    
    state_file = platform_dir / '.state.json'
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
            stats['total'] = state.get('posts_count', 0)
            stats['last_activity'] = state.get('last_check', 'N/A')
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_file = platform_dir / f'posts_{today}.md'
    if today_file.exists():
        with open(today_file, 'r') as f:
            stats['today'] = f.read().count('## Post -')
    
    return stats


def get_recent_posts(platform: str, limit: int = 10) -> list:
    """Get recent posts"""
    platform_dir = SOCIAL_DIR / platform.capitalize()
    posts_file = platform_dir / f'posted_{"tweets" if platform == "twitter" else "posts"}.json'
    
    if posts_file.exists():
        with open(posts_file, 'r') as f:
            posts = json.load(f)
            return posts[-limit:]
    return []


def get_all_logs() -> list:
    """Get all activity logs"""
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS_DIR / f'social_media_{today}.json'
    
    if log_file.exists():
        with open(log_file, 'r') as f:
            return json.load(f)
    return []


def execute_command(action: str, content: str = "") -> dict:
    """Execute a command"""
    result = {'success': False, 'message': '', 'output': None}
    
    try:
        if action == 'post_facebook':
            if not content:
                result['message'] = 'Content required'
                return result
            
            from watchers.facebook_watcher import FacebookWatcher
            watcher = FacebookWatcher(vault_path=str(VAULT_PATH))
            post_data = watcher.post_to_facebook(content)
            result['success'] = True
            result['message'] = 'Posted to Facebook!'
            result['output'] = post_data
            
        elif action == 'post_twitter':
            if not content:
                result['message'] = 'Content required'
                return result
            
            from watchers.twitter_watcher import TwitterWatcher
            watcher = TwitterWatcher(vault_path=str(VAULT_PATH))
            tweet_data = watcher.post_tweet(content)
            result['success'] = True
            result['message'] = 'Posted to Twitter!'
            result['output'] = tweet_data
            
        elif action == 'post_both':
            if not content:
                result['message'] = 'Content required'
                return result
            
            subprocess.run([
                'python', 'social_media_unified_post.py',
                '--text', content,
                '--vault', str(VAULT_PATH)
            ], capture_output=True)
            
            result['success'] = True
            result['message'] = 'Posted to both platforms!'
            
        elif action == 'refresh_dashboard':
            subprocess.run([
                'python', 'dashboard/update_social_dashboard.py',
                '--update',
                '--vault', str(VAULT_PATH)
            ], capture_output=True)
            result['success'] = True
            result['message'] = 'Dashboard refreshed!'
            
        else:
            result['message'] = 'Unknown action'
            
    except Exception as e:
        result['message'] = f'Error: {str(e)}'
    
    return result


def get_dashboard_html():
    """Generate complete HTML dashboard"""
    fb_stats = get_platform_stats('facebook')
    tw_stats = get_platform_stats('twitter')
    fb_posts = get_recent_posts('facebook')
    tw_posts = get_recent_posts('twitter')
    logs = get_all_logs()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Build Facebook posts HTML
    fb_posts_html = ""
    if fb_posts:
        for post in reversed(fb_posts[-10:]):
            content = post.get('content', 'No content')
            timestamp = post.get('timestamp', '')[:16]
            fb_posts_html += f"""
            <div class="post-card facebook">
                <div class="post-header">
                    <span class="platform-badge facebook">📘 Facebook</span>
                    <span class="post-time">{timestamp}</span>
                </div>
                <div class="post-content">{content}</div>
            </div>
            """
    else:
        fb_posts_html = '<div class="no-posts">No Facebook posts yet. Post something!</div>'
    
    # Build Twitter posts HTML
    tw_posts_html = ""
    if tw_posts:
        for post in reversed(tw_posts[-10:]):
            content = post.get('content', 'No content')
            timestamp = post.get('timestamp', '')[:16]
            tw_posts_html += f"""
            <div class="post-card twitter">
                <div class="post-header">
                    <span class="platform-badge twitter">🐦 Twitter</span>
                    <span class="post-time">{timestamp}</span>
                </div>
                <div class="post-content">{content}</div>
            </div>
            """
    else:
        tw_posts_html = '<div class="no-posts">No Twitter posts yet. Post something!</div>'
    
    # Build logs HTML
    logs_html = ""
    if logs:
        for log in reversed(logs[-20:]):
            timestamp = log.get('timestamp', '')[:19].replace('T', ' ')
            platforms = log.get('platforms', {})
            fb_status = '✓' if platforms.get('facebook', {}).get('success') else '✗'
            tw_status = '✓' if platforms.get('twitter', {}).get('success') else '✗'
            content = log.get('content', '')[:100]
            
            logs_html += f"""
            <div class="log-entry">
                <div class="log-time">{timestamp}</div>
                <div class="log-content">{content}...</div>
                <div class="log-status">FB: {fb_status} | TW: {tw_status}</div>
            </div>
            """
    else:
        logs_html = '<div class="no-posts">No activity logs yet</div>'
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Command Center</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }}
        .container {{ max-width: 1600px; margin: 0 auto; padding: 20px; }}
        
        header {{ 
            text-align: center; 
            padding: 30px 0;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            margin-bottom: 30px;
        }}
        header h1 {{ font-size: 2.5em; margin-bottom: 10px; background: linear-gradient(90deg, #1877f2, #1da1f2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        header .timestamp {{ color: #888; font-size: 0.9em; }}
        
        /* Stats Grid */
        .stats-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        
        .stat-card.facebook {{ border-left: 4px solid #1877f2; }}
        .stat-card.twitter {{ border-left: 4px solid #1da1f2; }}
        .stat-card.logs {{ border-left: 4px solid #4caf50; }}
        
        .stat-card h2 {{ font-size: 1.3em; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }}
        .stat-card .stat-row {{ 
            display: flex; 
            justify-content: space-between; 
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }}
        .stat-card .stat-row:last-child {{ border-bottom: none; }}
        .stat-card .stat-value {{ font-size: 1.5em; font-weight: bold; color: #4caf50; }}
        
        /* Command Section */
        .command-section {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .command-section h2 {{ margin-bottom: 20px; font-size: 1.5em; }}
        
        .command-form {{ display: grid; gap: 15px; }}
        
        .form-group {{ display: flex; flex-direction: column; gap: 8px; }}
        .form-group label {{ font-weight: 600; color: #aaa; }}
        
        textarea {{
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.08);
            color: #fff;
            font-size: 1em;
            resize: vertical;
        }}
        textarea:focus {{ outline: none; border-color: #4caf50; }}
        
        .button-group {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        
        .btn {{
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .btn-facebook {{ background: #1877f2; color: white; }}
        .btn-facebook:hover {{ background: #166fe5; }}
        
        .btn-twitter {{ background: #1da1f2; color: white; }}
        .btn-twitter:hover {{ background: #1a91da; }}
        
        .btn-both {{ background: linear-gradient(90deg, #1877f2, #1da1f2); color: white; }}
        .btn-both:hover {{ transform: scale(1.05); }}
        
        .btn-refresh {{ background: #4caf50; color: white; }}
        .btn-refresh:hover {{ background: #45a049; }}
        
        /* Posts Grid */
        .posts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .posts-column {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            max-height: 600px;
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
            border-left: 3px solid transparent;
        }}
        .post-card.facebook {{ border-left-color: #1877f2; }}
        .post-card.twitter {{ border-left-color: #1da1f2; }}
        
        .post-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .platform-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .platform-badge.facebook {{ background: rgba(24, 119, 242, 0.3); }}
        .platform-badge.twitter {{ background: rgba(29, 161, 242, 0.3); }}
        
        .post-time {{ color: #888; font-size: 0.85em; }}
        .post-content {{ line-height: 1.6; color: #ddd; }}
        
        .no-posts {{
            text-align: center;
            color: #666;
            padding: 40px;
            font-style: italic;
        }}
        
        /* Activity Logs */
        .logs-section {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            margin-top: 30px;
        }}
        
        .logs-section h3 {{
            font-size: 1.3em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }}
        
        .log-entry {{
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            display: grid;
            grid-template-columns: 180px 1fr 100px;
            gap: 15px;
            align-items: center;
        }}
        
        .log-time {{ color: #888; font-size: 0.85em; font-family: monospace; }}
        .log-content {{ color: #ddd; }}
        .log-status {{ text-align: right; color: #4caf50; font-weight: bold; }}
        
        /* Status Messages */
        .status-message {{
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            font-weight: 600;
            z-index: 1000;
            display: none;
            animation: slideIn 0.3s ease;
        }}
        
        .status-message.success {{ background: #4caf50; color: white; }}
        .status-message.error {{ background: #f44336; color: white; }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        /* Auto-refresh indicator */
        .auto-refresh {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 50px;
            font-size: 0.85em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .pulse {{
            width: 10px;
            height: 10px;
            background: #4caf50;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.2); }}
        }}
        
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.05); }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.2); border-radius: 4px; }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .posts-grid {{ grid-template-columns: 1fr; }}
            .log-entry {{ grid-template-columns: 1fr; }}
            .button-group {{ flex-direction: column; }}
            .btn {{ width: 100%; justify-content: center; }}
        }}
    </style>
</head>
<body>
    <div class="status-message" id="statusMessage"></div>
    
    <div class="container">
        <header>
            <h1>📊 Social Media Command Center</h1>
            <p class="timestamp">Last updated: {now}</p>
        </header>
        
        <!-- Stats -->
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
            
            <div class="stat-card logs">
                <h2>📋 Activity Logs</h2>
                <div class="stat-row">
                    <span>Today's Actions:</span>
                    <span class="stat-value">{len(logs)}</span>
                </div>
                <div class="stat-row">
                    <span>Watchers:</span>
                    <span class="stat-value" style="color: #4caf50;">● Running</span>
                </div>
                <div class="stat-row">
                    <span>Auto-refresh:</span>
                    <span class="stat-value">30s</span>
                </div>
            </div>
        </div>
        
        <!-- Command Section -->
        <div class="command-section">
            <h2>🎯 Post Commands</h2>
            <div class="command-form">
                <div class="form-group">
                    <label>📝 Enter your post content:</label>
                    <textarea id="postContent" placeholder="Type your message here..."></textarea>
                </div>
                <div class="button-group">
                    <button class="btn btn-facebook" onclick="postTo('facebook')">
                        📘 Post to Facebook
                    </button>
                    <button class="btn btn-twitter" onclick="postTo('twitter')">
                        🐦 Post to Twitter
                    </button>
                    <button class="btn btn-both" onclick="postTo('both')">
                        🚀 Post to Both
                    </button>
                    <button class="btn btn-refresh" onclick="refreshDashboard()">
                        🔄 Refresh Dashboard
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Posts Grid -->
        <div class="posts-grid">
            <div class="posts-column">
                <h3>📘 Recent Facebook Posts</h3>
                {fb_posts_html}
            </div>
            <div class="posts-column">
                <h3>🐦 Recent Twitter Posts</h3>
                {tw_posts_html}
            </div>
        </div>
        
        <!-- Activity Logs -->
        <div class="logs-section">
            <h3>📜 Recent Activity Logs</h3>
            {logs_html}
        </div>
    </div>
    
    <div class="auto-refresh">
        <div class="pulse"></div>
        Auto-refresh: <span id="countdown">30</span>s
    </div>
    
    <script>
        // Post to platform
        async function postTo(platform) {{
            const content = document.getElementById('postContent').value;
            if (!content) {{
                showStatus('Please enter post content!', 'error');
                return;
            }}
            
            const btn = event.target;
            const originalText = btn.innerHTML;
            btn.innerHTML = '⏳ Posting...';
            btn.disabled = true;
            
            try {{
                const response = await fetch('/api/post', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ action: 'post_' + platform, content: content }})
                }});
                
                const result = await response.json();
                
                if (result.success) {{
                    showStatus(result.message, 'success');
                    document.getElementById('postContent').value = '';
                    setTimeout(() => location.reload(), 1500);
                }} else {{
                    showStatus(result.message, 'error');
                }}
            }} catch (error) {{
                showStatus('Error: ' + error.message, 'error');
            }} finally {{
                btn.innerHTML = originalText;
                btn.disabled = false;
            }}
        }}
        
        // Refresh dashboard
        function refreshDashboard() {{
            showStatus('Refreshing dashboard...', 'success');
            setTimeout(() => location.reload(), 1000);
        }}
        
        // Show status message
        function showStatus(message, type) {{
            const msg = document.getElementById('statusMessage');
            msg.textContent = message;
            msg.className = 'status-message ' + type;
            msg.style.display = 'block';
            
            setTimeout(() => {{
                msg.style.display = 'none';
            }}, 3000);
        }}
        
        // Auto-refresh countdown
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
    """Custom HTTP handler"""
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(get_dashboard_html().encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/post':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            result = execute_command(data.get('action'), data.get('content'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            super().do_POST()


def run_server(port=8080):
    """Run dashboard server"""
    server = HTTPServer(('localhost', port), DashboardHandler)
    print(f"Dashboard running at http://localhost:{port}")
    server.serve_forever()


def main():
    port = 8080
    
    # Start server in background
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()
    
    time.sleep(1.5)
    
    # Open in browser
    webbrowser.open(f'http://localhost:{port}')
    
    print("Dashboard opened in browser!")
    print("\nFeatures:")
    print("  ✓ Post to Facebook, Twitter, or Both")
    print("  ✓ View all recent posts")
    print("  ✓ Activity logs")
    print("  ✓ Auto-refresh every 30 seconds")
    print("\nPress Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDashboard stopped")


if __name__ == '__main__':
    import time
    main()

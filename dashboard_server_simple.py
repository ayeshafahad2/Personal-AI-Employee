#!/usr/bin/env python3
"""
Simple Dashboard Server - Fixed Version
"""

import os
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Reload .env on every request
def load_env_fresh():
    env_path = Path('.env')
    config = {}
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config

app = Flask(__name__, static_folder='dashboard', static_url_path='')
CORS(app)

PROJECT_ROOT = Path(__file__).parent.absolute()
VAULT_PATH = PROJECT_ROOT / 'AI_Employee_Vault'
SOCIAL_MEDIA_PATH = VAULT_PATH / 'Social_Media'
LOGS_PATH = VAULT_PATH / 'Logs'

@app.route('/')
def index():
    return send_from_directory('dashboard', 'dashboard.html')

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/api/status', methods=['GET'])
def api_get_status():
    """Get configuration status - reads fresh from .env"""
    env = load_env_fresh()
    
    status = {}
    
    # Twitter
    twitter_bearer = env.get('TWITTER_BEARER_TOKEN', '')
    status['twitter'] = {
        'configured': bool(twitter_bearer and 'AAAA' in twitter_bearer),
        'last_error': None,
        'hint': 'TWITTER_BEARER_TOKEN in .env'
    }
    
    # LinkedIn
    linkedin_token = env.get('LINKEDIN_ACCESS_TOKEN', '')
    status['linkedin'] = {
        'configured': bool(linkedin_token and 'AQ' in linkedin_token),
        'last_error': None,
        'hint': 'LINKEDIN_ACCESS_TOKEN in .env'
    }
    
    # Gmail
    gmail_id = env.get('GMAIL_CLIENT_ID', '')
    gmail_secret = env.get('GMAIL_CLIENT_SECRET', '')
    status['gmail'] = {
        'configured': bool(gmail_id and gmail_secret),
        'last_error': None,
        'hint': 'GMAIL_CLIENT_ID + SECRET in .env'
    }
    
    # WhatsApp
    twilio_sid = env.get('TWILIO_ACCOUNT_SID', '')
    twilio_token = env.get('TWILIO_AUTH_TOKEN', '')
    whatsapp_number = env.get('WHATSAPP_RECIPIENT_NUMBER', '')
    status['whatsapp'] = {
        'configured': bool(whatsapp_number),
        'partial': not (twilio_sid and twilio_token),
        'last_error': None,
        'hint': 'Browser method ready' if not twilio_sid else 'Twilio configured'
    }
    
    # Facebook
    fb_token = env.get('FACEBOOK_PAGE_ACCESS_TOKEN', '')
    status['facebook'] = {
        'configured': bool(fb_token),
        'last_error': None,
        'hint': 'FACEBOOK_PAGE_ACCESS_TOKEN in .env'
    }
    
    # Instagram
    ig_token = env.get('INSTAGRAM_PAGE_ACCESS_TOKEN', '')
    ig_account = env.get('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
    status['instagram'] = {
        'configured': bool(ig_token and ig_account),
        'last_error': None,
        'hint': 'INSTAGRAM_PAGE_ACCESS_TOKEN + ACCOUNT_ID in .env'
    }
    
    return jsonify(status), 200

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    """Get posting statistics"""
    stats = {}
    today = datetime.now().strftime('%Y-%m-%d')
    
    platforms = {
        'gmail': 'Gmail',
        'whatsapp': 'WhatsApp',
        'linkedin': 'LinkedIn',
        'facebook': 'Facebook',
        'twitter': 'Twitter'
    }
    
    for platform_key, platform_name in platforms.items():
        log_file = SOCIAL_MEDIA_PATH / platform_name / f'posted_{platform_key}.json'
        
        total = 0
        today_count = 0
        
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    posts = json.load(f)
                    total = len(posts)
                    today_count = sum(
                        1 for p in posts
                        if p.get('timestamp', '').startswith(today)
                    )
            except:
                pass
        
        stats[platform_key] = {
            'total': total,
            'today': today_count
        }
    
    return jsonify(stats), 200

@app.route('/api/posts/<platform>', methods=['GET'])
def api_get_posts(platform: str):
    """Get posts for a platform"""
    platform_map = {
        'twitter': 'Twitter',
        'facebook': 'Facebook',
        'linkedin': 'LinkedIn',
        'gmail': 'Gmail',
        'whatsapp': 'WhatsApp'
    }
    
    platform_name = platform_map.get(platform.lower())
    if not platform_name:
        return jsonify([]), 200
    
    log_file = SOCIAL_MEDIA_PATH / platform_name / f'posted_{platform.lower()}.json'
    
    if not log_file.exists():
        return jsonify([]), 200
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            posts = json.load(f)
        return jsonify(posts), 200
    except:
        return jsonify([]), 200

@app.route('/api/logs', methods=['GET'])
def api_get_logs():
    """Get activity logs"""
    date = request.args.get('date', datetime.now().strftime('%Y%m%d'))
    log_file = LOGS_PATH / f'social_media_{date}.json'
    
    if not log_file.exists():
        return jsonify([]), 200
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        return jsonify(logs), 200
    except:
        return jsonify([]), 200

@app.route('/api/post', methods=['POST'])
def api_post():
    """Post to social media platforms"""
    data = request.json
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    action = data.get('action', '')
    content = data.get('content', '')
    
    if not content:
        return jsonify({'status': 'error', 'message': 'Content is required'}), 400
    
    # WhatsApp - return info about browser method
    if action == 'post_whatsapp':
        return jsonify({
            'status': 'info',
            'message': 'WhatsApp: Please use browser method. Run: python whatsapp_send_browser.py'
        }), 200
    
    # For other platforms, return not configured message
    return jsonify({
        'status': 'error',
        'message': f'{action}: Platform not fully configured yet. Use browser method.'
    }), 400

if __name__ == '__main__':
    print("=" * 70)
    print("  SIMPLE DASHBOARD SERVER - FIXED")
    print("=" * 70)
    print("\n  Starting server...")
    print("  URL: http://localhost:8081")
    print("\n  Press Ctrl+C to stop")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=8081, debug=False)

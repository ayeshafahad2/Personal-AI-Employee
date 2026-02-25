#!/usr/bin/env python3
"""
Social Media Dashboard Server - Backend API

Provides REST API for the dashboard to:
- Post to all social media platforms
- Fetch post history and logs
- Get platform statistics

Usage:
    python dashboard_server.py
    
Then open: http://localhost:8081
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='dashboard', static_url_path='')
CORS(app)

# Paths
PROJECT_ROOT = Path(__file__).parent.absolute()
VAULT_PATH = PROJECT_ROOT / 'AI_Employee_Vault'
SOCIAL_MEDIA_PATH = VAULT_PATH / 'Social_Media'
LOGS_PATH = VAULT_PATH / 'Logs'

# Ensure directories exist
for platform in ['Twitter', 'Facebook', 'LinkedIn', 'Instagram', 'Gmail', 'WhatsApp']:
    (SOCIAL_MEDIA_PATH / platform).mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)


class SocialMediaPoster:
    """Handles posting to all social media platforms"""

    def __init__(self):
        self.vault_path = VAULT_PATH
        self.social_path = SOCIAL_MEDIA_PATH

        # Load credentials from .env
        self.twitter_bearer = os.getenv('TWITTER_BEARER_TOKEN', '')
        self.facebook_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
        self.linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
        self.instagram_token = os.getenv('INSTAGRAM_PAGE_ACCESS_TOKEN', '')
        self.instagram_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
        self.gmail_client_id = os.getenv('GMAIL_CLIENT_ID', '')
        self.gmail_client_secret = os.getenv('GMAIL_CLIENT_SECRET', '')
        self.gmail_token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.twilio_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER', '')
        self.whatsapp_recipient = os.getenv('WHATSAPP_RECIPIENT_NUMBER', '')

    def _log_post(self, platform: str, content: str, status: str, post_id: str = None):
        """Log post to platform history and activity log"""
        timestamp = datetime.now().isoformat()
        today = datetime.now().strftime('%Y%m%d')

        # Platform-specific log
        platform_dir = self.social_path / platform
        log_file = platform_dir / f'posted_{platform.lower()}.json'

        posts = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    posts = json.load(f)
            except:
                posts = []

        posts.append({
            'timestamp': timestamp,
            'content': content,
            'status': status,
            'post_id': post_id
        })

        # Keep last 100 posts
        posts = posts[-100:]

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

        # Activity log
        log_entry = {
            'timestamp': timestamp,
            'platform': platform,
            'content': content,
            'status': status,
            'post_id': post_id
        }

        activity_log = LOGS_PATH / f'social_media_{today}.json'
        activity_logs = []
        if activity_log.exists():
            try:
                with open(activity_log, 'r', encoding='utf-8') as f:
                    activity_logs = json.load(f)
            except:
                activity_logs = []

        activity_logs.append(log_entry)
        activity_logs = activity_logs[-100:]

        with open(activity_log, 'w', encoding='utf-8') as f:
            json.dump(activity_logs, f, indent=2, ensure_ascii=False)

    def post_twitter(self, content: str) -> dict:
        """Post to Twitter/X using API v2"""
        if not self.twitter_bearer:
            return {'status': 'error', 'message': 'Twitter credentials not configured'}

        try:
            endpoint = "https://api.twitter.com/2/tweets"
            headers = {
                'Authorization': f'Bearer {self.twitter_bearer}',
                'Content-Type': 'application/json'
            }
            payload = {'text': content[:280]}  # Twitter character limit

            response = requests.post(endpoint, json=payload, headers=headers, timeout=30)

            if response.status_code == 201:
                data = response.json()
                tweet_id = data.get('data', {}).get('id')
                self._log_post('Twitter', content, 'success', tweet_id)
                return {'status': 'success', 'message': 'Posted to Twitter!', 'post_id': tweet_id}
            else:
                error = response.json().get('errors', [{}])[0].get('message', str(response.status_code))
                self._log_post('Twitter', content, f'error: {error}')
                return {'status': 'error', 'message': f'Twitter API error: {error}'}

        except Exception as e:
            self._log_post('Twitter', content, f'error: {str(e)}')
            return {'status': 'error', 'message': f'Twitter error: {str(e)}'}

    def post_facebook(self, content: str) -> dict:
        """Post to Facebook Page using Graph API"""
        if not self.facebook_token:
            return {'status': 'error', 'message': 'Facebook credentials not configured'}

        try:
            # Get page ID from token
            token_info_url = "https://graph.facebook.com/me/accounts"
            params = {'access_token': self.facebook_token}
            info_response = requests.get(token_info_url, params=params, timeout=30)

            if info_response.status_code != 200:
                return {'status': 'error', 'message': 'Invalid Facebook token'}

            pages = info_response.json().get('data', [])
            if not pages:
                return {'status': 'error', 'message': 'No Facebook pages found'}

            page_id = pages[0]['id']

            # Post to page
            endpoint = f"https://graph.facebook.com/v18.0/{page_id}/feed"
            params = {
                'message': content,
                'access_token': self.facebook_token
            }

            response = requests.post(endpoint, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                post_id = data.get('id')
                self._log_post('Facebook', content, 'success', post_id)
                return {'status': 'success', 'message': 'Posted to Facebook!', 'post_id': post_id}
            else:
                error = response.json().get('error', {}).get('message', str(response.status_code))
                self._log_post('Facebook', content, f'error: {error}')
                return {'status': 'error', 'message': f'Facebook error: {error}'}

        except Exception as e:
            self._log_post('Facebook', content, f'error: {str(e)}')
            return {'status': 'error', 'message': f'Facebook error: {str(e)}'}

    def post_linkedin(self, content: str) -> dict:
        """Post to LinkedIn using API"""
        if not self.linkedin_token:
            return {'status': 'error', 'message': 'LinkedIn credentials not configured'}

        try:
            # Get person URN
            me_url = "https://api.linkedin.com/v2/me"
            headers = {
                'Authorization': f'Bearer {self.linkedin_token}',
                'X-Restli-Protocol-Version': '2.0.0'
            }

            me_response = requests.get(me_url, headers=headers, timeout=30)
            if me_response.status_code != 200:
                return {'status': 'error', 'message': 'LinkedIn auth error'}

            person_urn = me_response.json().get('id')

            # Create post
            post_url = "https://api.linkedin.com/v2/shares"
            payload = {
                "author": f"urn:li:person:{person_urn}",
                "text": {
                    "text": content
                },
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": [],
                    "thirdPartyDistributionChannels": []
                }
            }

            response = requests.post(post_url, json=payload, headers=headers, timeout=30)

            if response.status_code == 201:
                data = response.json()
                post_id = data.get('id')
                self._log_post('LinkedIn', content, 'success', post_id)
                return {'status': 'success', 'message': 'Posted to LinkedIn!', 'post_id': post_id}
            else:
                error = response.text[:200]
                self._log_post('LinkedIn', content, f'error: {error}')
                return {'status': 'error', 'message': f'LinkedIn error: {error}'}

        except Exception as e:
            self._log_post('LinkedIn', content, f'error: {str(e)}')
            return {'status': 'error', 'message': f'LinkedIn error: {str(e)}'}

    def post_instagram(self, content: str, image_url: str = None) -> dict:
        """Post to Instagram Business account"""
        if not self.instagram_token or not self.instagram_account_id:
            return {'status': 'error', 'message': 'Instagram credentials not configured'}

        try:
            # For image posts, we need an image URL
            # For now, we'll use a placeholder or skip if no image
            if not image_url:
                # Text-only post not supported on Instagram API
                # Use browser automation instead
                return {
                    'status': 'info',
                    'message': 'Instagram requires images. Use Instagram dashboard for image posts.'
                }

            # Create media container
            container_url = f"https://graph.facebook.com/v18.0/{self.instagram_account_id}/media"
            params = {
                'image_url': image_url,
                'caption': content,
                'access_token': self.instagram_token
            }

            container_response = requests.post(container_url, params=params, timeout=30)

            if container_response.status_code != 200:
                error = container_response.json().get('error', {}).get('message', 'Unknown error')
                return {'status': 'error', 'message': f'Instagram error: {error}'}

            container_id = container_response.json().get('id')

            # Publish media
            publish_url = f"https://graph.facebook.com/v18.0/{self.instagram_account_id}/media_publish"
            params = {
                'creation_id': container_id,
                'access_token': self.instagram_token
            }

            publish_response = requests.post(publish_url, params=params, timeout=30)

            if publish_response.status_code == 200:
                data = publish_response.json()
                post_id = data.get('id')
                self._log_post('Instagram', content, 'success', post_id)
                return {'status': 'success', 'message': 'Posted to Instagram!', 'post_id': post_id}
            else:
                error = publish_response.json().get('error', {}).get('message', 'Publish failed')
                self._log_post('Instagram', content, f'error: {error}')
                return {'status': 'error', 'message': f'Instagram publish error: {error}'}

        except Exception as e:
            self._log_post('Instagram', content, f'error: {str(e)}')
            return {'status': 'error', 'message': f'Instagram error: {str(e)}'}

    def send_gmail(self, content: str, subject: str = None, to: str = None) -> dict:
        """Send email via Gmail API"""
        if not self.gmail_client_id or not self.gmail_client_secret:
            return {'status': 'error', 'message': 'Gmail credentials not configured'}

        try:
            # For simplicity, use a basic email sending approach
            # In production, implement full OAuth2 flow
            import base64
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            # Default recipient (you can configure this)
            recipient = to or os.getenv('GMAIL_DEFAULT_RECIPIENT', '')
            if not recipient:
                return {'status': 'error', 'message': 'No recipient configured for Gmail'}

            # Create message
            msg = MIMEMultipart()
            msg['To'] = recipient
            msg['From'] = 'AI Employee <ai@company.com>'
            msg['Subject'] = subject or 'AI Employee Update'
            msg.attach(MIMEText(content, 'plain', 'utf-8'))

            # Encode message
            raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')

            # Send via Gmail API
            send_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"

            # Get OAuth token (simplified - in production use proper OAuth flow)
            token_file = Path(self.gmail_token_path)
            if not token_file.exists():
                return {
                    'status': 'error',
                    'message': 'Gmail token not found. Run Gmail auth setup first.'
                }

            with open(token_file, 'r') as f:
                token_data = json.load(f)
                access_token = token_data.get('access_token')

            if not access_token:
                return {'status': 'error', 'message': 'Gmail token expired'}

            headers = {'Authorization': f'Bearer {access_token}'}
            payload = {'raw': raw_message}

            response = requests.post(send_url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                message_id = data.get('id')
                self._log_post('Gmail', f'Subject: {subject}\n{content}', 'success', message_id)
                return {'status': 'success', 'message': 'Email sent!', 'message_id': message_id}
            else:
                error = response.json().get('error', {}).get('message', str(response.status_code))
                self._log_post('Gmail', content, f'error: {error}')
                return {'status': 'error', 'message': f'Gmail error: {error}'}

        except Exception as e:
            self._log_post('Gmail', content, f'error: {str(e)}')
            return {'status': 'error', 'message': f'Gmail error: {str(e)}'}

    def send_whatsapp(self, content: str, to: str = None) -> dict:
        """Send WhatsApp message via Twilio"""
        if not self.twilio_sid or not self.twilio_token:
            return {'status': 'error', 'message': 'Twilio credentials not configured'}

        try:
            from twilio.rest import Client

            client = Client(self.twilio_sid, self.twilio_token)

            recipient = to or self.whatsapp_recipient
            if not recipient:
                return {'status': 'error', 'message': 'No WhatsApp recipient configured'}

            message = client.messages.create(
                body=content,
                from_=self.twilio_whatsapp,
                to=recipient
            )

            self._log_post('WhatsApp', content, 'success', message.sid)
            return {'status': 'success', 'message': 'WhatsApp sent!', 'message_id': message.sid}

        except ImportError:
            # Twilio not installed, use fallback
            self._log_post('WhatsApp', content, 'info', 'manual')
            return {
                'status': 'info',
                'message': 'Twilio not installed. Install with: pip install twilio'
            }
        except Exception as e:
            self._log_post('WhatsApp', content, f'error: {str(e)}')
            return {'status': 'error', 'message': f'WhatsApp error: {str(e)}'}


# Initialize poster
poster = SocialMediaPoster()


# =============================================================================
# API Routes
# =============================================================================

@app.route('/')
def index():
    """Serve the dashboard HTML"""
    return send_from_directory('dashboard', 'dashboard.html')


@app.route('/<path:path>')
def static_files(path):
    """Serve static files from dashboard folder"""
    return send_from_directory('dashboard', path)


@app.route('/api/post', methods=['POST'])
def api_post():
    """
    Post to social media platforms

    Request body:
    {
        "action": "post_twitter|post_facebook|post_linkedin|post_instagram|send_gmail|send_whatsapp",
        "content": "message content",
        "subject": "email subject (optional)",
        "to": "recipient (optional)",
        "image_url": "image URL for Instagram (optional)"
    }
    """
    data = request.json

    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400

    action = data.get('action', '')
    content = data.get('content', '')

    if not content:
        return jsonify({'status': 'error', 'message': 'Content is required'}), 400

    # Route to appropriate handler
    handlers = {
        'post_twitter': lambda: poster.post_twitter(content),
        'post_facebook': lambda: poster.post_facebook(content),
        'post_linkedin': lambda: poster.post_linkedin(content),
        'post_instagram': lambda: poster.post_instagram(content, data.get('image_url')),
        'send_gmail': lambda: poster.send_gmail(content, data.get('subject'), data.get('to')),
        'send_whatsapp': lambda: poster.send_whatsapp(content, data.get('to'))
    }

    if action not in handlers:
        return jsonify({'status': 'error', 'message': f'Unknown action: {action}'}), 400

    result = handlers[action]()
    status_code = 200 if result['status'] == 'success' else 400
    return jsonify(result), status_code


@app.route('/api/posts/<platform>', methods=['GET'])
def api_get_posts(platform: str):
    """Get posts for a specific platform"""
    platform_map = {
        'twitter': 'Twitter',
        'facebook': 'Facebook',
        'linkedin': 'LinkedIn',
        'instagram': 'Instagram',
        'gmail': 'Gmail',
        'whatsapp': 'WhatsApp'
    }

    platform_name = platform_map.get(platform.lower())
    if not platform_name:
        return jsonify([]), 400

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


@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    """Get posting statistics for all platforms"""
    stats = {}
    today = datetime.now().strftime('%Y-%m-%d')

    platform_map = {
        'gmail': 'Gmail',
        'whatsapp': 'WhatsApp',
        'instagram': 'Instagram',
        'linkedin': 'LinkedIn',
        'facebook': 'Facebook',
        'twitter': 'Twitter'
    }

    for platform_key, platform_name in platform_map.items():
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


@app.route('/api/status', methods=['GET'])
def api_get_status():
    """Get configuration status for all platforms"""
    status = {}
    
    # Check Twitter
    twitter_configured = bool(poster.twitter_bearer and poster.twitter_bearer and poster.twitter_bearer != 'newTokenHash12345678901234567890')
    status['twitter'] = {
        'configured': twitter_configured,
        'last_error': None,
        'hint': 'Run: python refresh_twitter_token.py' if not twitter_configured else 'TWITTER_BEARER_TOKEN in .env'
    }
    
    # Check Facebook
    status['facebook'] = {
        'configured': bool(poster.facebook_token),
        'last_error': None,
        'hint': 'Get from: https://developers.facebook.com/apps/'
    }
    
    # Check LinkedIn
    linkedin_configured = bool(poster.linkedin_token)
    status['linkedin'] = {
        'configured': linkedin_configured,
        'last_error': None,
        'hint': 'LINKEDIN_ACCESS_TOKEN in .env'
    }
    
    # Check Instagram
    status['instagram'] = {
        'configured': bool(poster.instagram_token and poster.instagram_account_id),
        'last_error': None,
        'hint': 'INSTAGRAM_PAGE_ACCESS_TOKEN + ACCOUNT_ID in .env'
    }
    
    # Check Gmail
    status['gmail'] = {
        'configured': bool(poster.gmail_client_id and poster.gmail_client_secret),
        'last_error': None,
        'hint': 'GMAIL_CLIENT_ID + SECRET in .env'
    }
    
    # Check WhatsApp
    status['whatsapp'] = {
        'configured': bool(poster.twilio_sid and poster.twilio_token),
        'last_error': None,
        'hint': 'TWILIO_ACCOUNT_SID + AUTH_TOKEN in .env'
    }
    
    return jsonify(status), 200


@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("  SOCIAL MEDIA DASHBOARD SERVER")
    print("=" * 70)
    print("\n  Starting server...")
    print("  URL: http://localhost:8081")
    print("  API: http://localhost:8081/api")
    print("\n  Press Ctrl+C to stop")
    print("=" * 70)

    app.run(host='0.0.0.0', port=8081, debug=False)

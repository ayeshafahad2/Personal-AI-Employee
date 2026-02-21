"""
LinkedIn Watcher Implementation
Monitors LinkedIn for important messages/posts and creates action files in Needs_Action folder
Also includes functionality to post content to LinkedIn
"""
import time
import logging
import sys
from pathlib import Path
import os
import requests
from datetime import datetime
from urllib.parse import urlencode
from typing import Dict, List, Optional

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.watchers.base_watcher import BaseWatcher
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LinkedIn API constants
LINKEDIN_API_BASE_URL = "https://api.linkedin.com/v2"
LINKEDIN_OAUTH_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_SHARE_API_URL = "https://api.linkedin.com/v2/sharePosts"

class LinkedInWatcher(BaseWatcher):
    def __init__(self, vault_path: str, access_token: str = None):
        super().__init__(vault_path, check_interval=300)  # Check every 5 minutes
        self.access_token = access_token or os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost')
        
        # Track processed posts/messages to avoid duplicates
        self.processed_posts = set()
        self.processed_messages = set()
        
        # Keywords to monitor for important content
        self.keywords = [
            'urgent', 'asap', 'important', 'meeting', 'opportunity', 'collaboration',
            'proposal', 'contract', 'offer', 'interview', 'position', 'job', 'hiring',
            'business', 'partnership', 'investment', 'funding', 'pitch', 'networking'
        ]

        if not self.access_token:
            self.logger.warning("LinkedIn access token not found. LinkedIn watcher will run in simulation mode.")

    def _make_request(self, endpoint: str, params: dict = None, method: str = 'GET', data=None) -> Optional[Dict]:
        """Make authenticated request to LinkedIn API"""
        if not self.access_token:
            return None
            
        url = f"{LINKEDIN_API_BASE_URL}/{endpoint}" if endpoint != "sharePosts" else LINKEDIN_SHARE_API_URL
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                if data:
                    response = requests.post(url, headers=headers, json=data)
                else:
                    response = requests.post(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request to LinkedIn API: {e}")
            return None

    def post_content(self, text: str, visibility: str = "PUBLIC") -> Optional[Dict]:
        """
        Post content to LinkedIn
        :param text: The text content to post
        :param visibility: Who can see the post (PUBLIC, CONNECTIONS, etc.)
        :return: Response from the LinkedIn API
        """
        if not self.access_token:
            self.logger.error("Cannot post to LinkedIn: No access token available")
            return None

        # Format the post according to LinkedIn's API requirements
        post_data = {
            "author": f"urn:li:person:{self._get_person_urn()}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }

        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            response = requests.post(LINKEDIN_SHARE_API_URL, headers=headers, json=post_data)
            response.raise_for_status()
            result = response.json()
            
            self.logger.info(f"Successfully posted to LinkedIn: {result.get('id', 'Unknown ID')}")
            return result
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error posting to LinkedIn: {e}")
            return None

    def _get_person_urn(self) -> str:
        """
        Get the person URN for the authenticated user
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            response = requests.get(
                f"{LINKEDIN_API_BASE_URL}/me", 
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('id', '')
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error getting person URN: {e}")
            return ""

    def _refresh_access_token(self) -> Optional[str]:
        """Refresh the LinkedIn access token using refresh token if available"""
        refresh_token = os.getenv('LINKEDIN_REFRESH_TOKEN')
        if not refresh_token:
            return None
        
        try:
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            response = requests.post(LINKEDIN_OAUTH_URL, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            new_access_token = token_data.get('access_token')
            
            # Update the instance variable
            self.access_token = new_access_token
            
            # Optionally update the environment variable if using a way to persist it
            return new_access_token
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error refreshing LinkedIn access token: {e}")
            return None

    def check_for_updates(self) -> list:
        """Check LinkedIn for new important posts/messages"""
        updates = []
        
        if not self.access_token:
            # Simulation mode - return sample data
            return self._get_sample_updates()
        
        # Check for new posts/updates in network feed
        posts = self._check_network_feed()
        updates.extend(posts)
        
        # Check for new messages
        messages = self._check_messages()
        updates.extend(messages)
        
        return updates

    def _get_sample_updates(self) -> list:
        """Return sample LinkedIn updates for simulation mode"""
        sample_updates = [
            {
                'type': 'post',
                'id': 'sample_post_1',
                'author': 'John Doe',
                'author_headline': 'Senior Developer at Tech Corp',
                'content': 'Looking for a senior Python developer for an urgent project. Contact me if interested!',
                'timestamp': datetime.now().isoformat(),
                'url': 'https://linkedin.com/posts/sample1'
            },
            {
                'type': 'message',
                'id': 'sample_msg_1',
                'sender': 'Jane Smith',
                'sender_headline': 'HR Manager at Startup Inc',
                'content': 'Hi there! Saw your profile and thought you might be interested in our new opening. Would love to chat!',
                'timestamp': datetime.now().isoformat(),
                'url': 'https://linkedin.com/inbox/sample1'
            }
        ]
        
        filtered_updates = []
        for update in sample_updates:
            # Check if it contains important keywords
            content = update.get('content', '').lower()
            if any(keyword in content for keyword in self.keywords):
                filtered_updates.append(update)
        
        return filtered_updates

    def _check_network_feed(self) -> list:
        """Check the LinkedIn network feed for important posts"""
        # Note: LinkedIn's API has strict limitations on reading feeds
        # This is a simplified implementation that would need to be adapted
        # based on the specific LinkedIn API permissions granted
        
        updates = []
        
        # For now, we'll simulate checking for posts mentioning the user
        # In a real implementation, this would use the appropriate LinkedIn API endpoints
        try:
            # This is a placeholder - actual implementation would depend on granted permissions
            # LinkedIn API v2 doesn't allow reading arbitrary feeds without special permissions
            # So we'll focus on notifications and user-specific content
            
            # Get user's own posts and activity
            # This is just a conceptual example - actual implementation would vary
            pass
            
        except Exception as e:
            self.logger.error(f"Error checking LinkedIn network feed: {e}")
        
        return updates

    def _check_messages(self) -> list:
        """Check LinkedIn messages for important content"""
        updates = []
        
        try:
            # LinkedIn API v2 doesn't have direct message endpoints
            # This would require special permissions or using the Notifications API
            # For now, we'll simulate this functionality
            
            # In a real implementation, this would use the LinkedIn Communications API
            # or other approved methods to access messages
            pass
            
        except Exception as e:
            self.logger.error(f"Error checking LinkedIn messages: {e}")
        
        return updates

    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder for important LinkedIn activity"""
        content = f"""---
type: linkedin_activity
activity_type: {item['type']}
author: {item.get('author', item.get('sender', 'Unknown'))}
timestamp: {item['timestamp']}
priority: medium
status: pending
linkedin_id: {item['id']}
---

# Important LinkedIn Activity

## Activity Details
- **Type**: {item['type'].title()}
- **Author/Sender**: {item.get('author', item.get('sender', 'Unknown'))}
- **Author Headline**: {item.get('author_headline', 'Not available')}
- **Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **LinkedIn ID**: {item['id']}

## Content
{item['content']}

## Link
[View on LinkedIn]({item.get('url', '#')})

## Suggested Actions
- [ ] Review the LinkedIn activity
- [ ] Respond appropriately if necessary
- [ ] Follow up on opportunities
- [ ] Mark as processed

## Classification
- [ ] Urgent - Requires immediate attention
- [ ] Important - Should be addressed today
- [ ] Opportunity - Potential business/professional opportunity
- [ ] Routine - Can be handled later

## Next Steps
1. Determine the nature of the activity
2. Assess if action is required
3. Decide on appropriate response
4. Execute response or delegate as needed
"""

        # Create filename with timestamp and activity details
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        author_clean = item.get('author', item.get('sender', 'unknown')).replace(' ', '_').replace('/', '_').replace('\\', '_')
        activity_type = item['type']
        
        filepath = self.needs_action / f'LINKEDIN_{timestamp}_{activity_type}_{author_clean}.md'
        filepath.write_text(content)

        self.logger.info(f'Created LinkedIn action file: {filepath.name}')
        return filepath


if __name__ == "__main__":
    # Example usage
    # Replace with your actual vault path
    vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'  # Adjust as needed
    watcher = LinkedInWatcher(str(vault_path))

    # For testing purposes, you can run a single check:
    # new_updates = watcher.check_for_updates()
    # for update in new_updates:
    #     watcher.create_action_file(update)

    # Or run continuously:
    # watcher.run()
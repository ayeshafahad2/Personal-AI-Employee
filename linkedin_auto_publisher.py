"""
LinkedIn Auto Publisher - Automatically publish posts to LinkedIn
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class LinkedInAutoPublisher:
    """Automatically publish posts to LinkedIn using the API"""
    
    def __init__(self):
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI', 'https://localhost')
        
        if not all([self.client_id, self.client_secret, self.access_token]):
            raise ValueError(
                "Missing LinkedIn credentials. Please set in .env:\n"
                "- LINKEDIN_CLIENT_ID\n"
                "- LINKEDIN_CLIENT_SECRET\n"
                "- LINKEDIN_ACCESS_TOKEN"
            )
        
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
    
    def get_urn(self) -> str:
        """
        Get the person URN for the authenticated user
        
        Returns:
            Person URN string (e.g., 'urn:li:person:ABC123')
        """
        try:
            response = requests.get(
                f"{self.base_url}/me",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            return data['id']
        except Exception as e:
            print(f"Error getting person URN: {e}")
            # Fallback - construct from subdomain if available
            return None
    
    def publish_post(self, text: str, title: str = None) -> dict:
        """
        Publish a text post to LinkedIn
        
        Args:
            text: The post content
            title: Optional title for the post
            
        Returns:
            dict with status and post URL
        """
        person_urn = self.get_urn()
        
        if not person_urn:
            return {
                'status': 'error',
                'error': 'Could not retrieve person URN'
            }
        
        # LinkedIn post payload
        payload = {
            "author": f"urn:li:person:{person_urn}",
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
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            post_id = data.get('id', '')
            post_urn = data.get('urn', '')
            
            # Extract person ID for URL
            post_url = f"https://www.linkedin.com/feed/update/{post_urn}" if post_urn else None
            
            return {
                'status': 'success',
                'post_id': post_id,
                'post_urn': post_urn,
                'post_url': post_url,
                'message': 'Post published successfully'
            }
            
        except requests.exceptions.HTTPError as e:
            error_detail = str(e)
            try:
                error_response = e.response.json()
                error_detail = error_response.get('message', str(e))
            except:
                pass
            
            return {
                'status': 'error',
                'error': error_detail,
                'status_code': e.response.status_code
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def publish_from_file(self, filepath: str) -> dict:
        """
        Publish a post from a text file
        
        Args:
            filepath: Path to the file containing post content
            
        Returns:
            dict with status
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                return {
                    'status': 'error',
                    'error': 'File is empty'
                }
            
            return self.publish_post(content)
            
        except FileNotFoundError:
            return {
                'status': 'error',
                'error': f'File not found: {filepath}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def test_connection(self) -> bool:
        """
        Test if LinkedIn credentials are valid
        
        Returns:
            True if connection successful, False otherwise
        """
        person_urn = self.get_urn()
        return person_urn is not None


if __name__ == '__main__':
    # Test the publisher
    print("Testing LinkedIn Auto Publisher...")
    
    try:
        publisher = LinkedInAutoPublisher()
        result = publisher.test_connection()
        print(f"Connection test: {'✅ PASSED' if result else '❌ FAILED'}")
        
        if result:
            print("\nLinkedIn credentials are valid and ready to use!")
        else:
            print("\nPlease check your LinkedIn credentials in .env file")
            
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease configure LinkedIn credentials in .env file")

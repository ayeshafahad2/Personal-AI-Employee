"""
WhatsApp Notifier - Send WhatsApp messages via Twilio
"""

import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

load_dotenv()


class WhatsAppNotifier:
    """Send WhatsApp notifications using Twilio API"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        self.recipient_number = os.getenv('WHATSAPP_RECIPIENT_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.twilio_whatsapp_number, self.recipient_number]):
            raise ValueError(
                "Missing Twilio credentials. Please set in .env:\n"
                "- TWILIO_ACCOUNT_SID\n"
                "- TWILIO_AUTH_TOKEN\n"
                "- TWILIO_WHATSAPP_NUMBER (e.g., whatsapp:+14155238886)\n"
                "- WHATSAPP_RECIPIENT_NUMBER (e.g., whatsapp:+923298374240)"
            )
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_message(self, message_body: str) -> dict:
        """
        Send a WhatsApp message
        
        Args:
            message_body: The message text to send
            
        Returns:
            dict with status and message SID
        """
        try:
            message = self.client.messages.create(
                from_=self.twilio_whatsapp_number,
                body=message_body,
                to=self.recipient_number
            )
            
            return {
                'status': 'success',
                'sid': message.sid,
                'message': f'Message sent successfully'
            }
            
        except TwilioRestException as e:
            return {
                'status': 'error',
                'error': str(e),
                'code': e.code
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def send_linkedin_post_notification(self, post_content: str, post_url: str = None) -> dict:
        """
        Send a formatted notification about a LinkedIn post
        
        Args:
            post_content: The content of the LinkedIn post
            post_url: Optional URL to the published post
            
        Returns:
            dict with status
        """
        message = "🚀 LinkedIn Post Published!\n\n"
        message += f"Content:\n{post_content[:200]}{'...' if len(post_content) > 200 else ''}\n\n"
        
        if post_url:
            message += f"View post: {post_url}\n"
        else:
            message += "Check your LinkedIn profile to view the post.\n"
        
        message += "\n— Your AI Assistant"
        
        return self.send_message(message)
    
    def test_connection(self) -> bool:
        """
        Test if Twilio credentials are valid
        
        Returns:
            True if connection successful, False otherwise
        """
        result = self.send_message("🔔 Test message from your AI Assistant - Twilio connection successful!")
        return result['status'] == 'success'


if __name__ == '__main__':
    # Test the notifier
    print("Testing WhatsApp Notifier...")
    
    try:
        notifier = WhatsAppNotifier()
        result = notifier.test_connection()
        print(f"Connection test: {'✅ PASSED' if result else '❌ FAILED'}")
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease configure Twilio credentials in .env file")

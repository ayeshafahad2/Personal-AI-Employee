"""
Script to send a test email from the AI Employee to the tester
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.gmail_sender import GmailSender

def send_homeschooling_email():
    """
    Send an email about homeschooling to the tester
    """
    print("Initializing Gmail sender...")
    
    try:
        sender = GmailSender()
        print("Gmail sender initialized successfully!")
        
        # Define the email details
        to_email = os.getenv('TEST_EMAIL', 'ayeshafahad661@gmail.com')
        subject = "Important: Time for Homeschooling"
        body = """Dear Tester,

This is an important notification from your AI Employee regarding homeschooling time.

As part of our testing process, we're verifying the AI employee's ability to send important notifications.

Please acknowledge receipt of this message.

Best regards,
Your AI Employee Assistant
"""
        
        print(f"Sending email to: {to_email}")
        print(f"Subject: {subject}")
        
        # Send the email
        result = sender.send_email(to_email, subject, body)
        
        if result:
            print(f"Email sent successfully with ID: {result}")
            print("The AI employee has successfully sent an email to the tester!")
        else:
            print("Failed to send email. Please check the logs for details.")
            
    except Exception as e:
        print(f"Error initializing Gmail sender: {e}")

if __name__ == "__main__":
    send_homeschooling_email()
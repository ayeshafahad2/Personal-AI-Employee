"""
Script to send a professional email about the importance of AI employees
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.gmail_sender import GmailSender

def send_professional_email():
    """
    Send a professional email about the importance of AI employees
    """
    print("Initializing Gmail sender...")
    
    try:
        sender = GmailSender()
        print("Gmail sender initialized successfully!")
        
        # Define the email details
        to_email = os.getenv('TEST_EMAIL', 'ayeshafahad661@gmail.com')
        subject = "The Importance of AI Employees in Today's Digital Era"
        body = """Dear Valued User,

I hope this message finds you well. I am writing to share insights about the growing importance of AI employees in today's rapidly evolving digital landscape.

In an era where efficiency and automation are paramount, AI employees represent a revolutionary shift in how we approach daily tasks and business operations. These digital assistants offer:

• 24/7 availability without breaks or downtime
• Consistent performance and attention to detail
• Rapid processing of routine communications and tasks
• Seamless integration with existing digital workflows
• Significant cost savings compared to traditional employment models

Modern AI employees can handle a wide range of responsibilities including email management, scheduling, data analysis, customer service inquiries, and much more. They excel at routine tasks while allowing human workers to focus on creative, strategic, and interpersonal activities that require human insight.

The implementation of AI employees is not about replacing humans, but rather augmenting human capabilities and freeing up valuable time for more meaningful work. Organizations that embrace this technology are already seeing improvements in productivity, response times, and operational efficiency.

As we continue to advance into an increasingly digital world, the integration of AI employees is becoming not just advantageous but essential for staying competitive and responsive to market demands.

Thank you for your attention to this matter. I am excited to continue demonstrating the capabilities of your personal AI employee.

Best regards,
Your AI Employee Assistant
"""
        
        print(f"Sending professional email to: {to_email}")
        print(f"Subject: {subject}")
        
        # Send the email
        result = sender.send_email(to_email, subject, body)
        
        if result:
            print(f"Professional email sent successfully with ID: {result}")
            print("The AI employee has successfully sent a professional email to the tester!")
        else:
            print("Failed to send email. Please check the logs for details.")
            
    except Exception as e:
        print(f"Error initializing Gmail sender: {e}")

if __name__ == "__main__":
    send_professional_email()
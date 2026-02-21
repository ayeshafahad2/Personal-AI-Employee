"""
Script to send a detailed professional email about the importance of AI employees
with a meeting invitation for tomorrow at 5 PM
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.utils.gmail_sender import GmailSender

def send_detailed_professional_email():
    """
    Send a detailed professional email about the importance of AI employees
    """
    print("Initializing Gmail sender...")
    
    try:
        sender = GmailSender()
        print("Gmail sender initialized successfully!")
        
        # Define the email details
        to_email = os.getenv('TEST_EMAIL', 'ayeshafahad661@gmail.com')
        subject = "The Strategic Importance of AI Employees in Today's Business Landscape - Meeting Tomorrow at 5 PM Sharp"
        body = """Dear Esteemed Colleague,

I trust this correspondence finds you in excellent health and spirits. I am writing to provide a comprehensive overview of the transformative role that AI employees are playing in today's dynamic business environment.

In an age where technological advancement drives competitive advantage, AI employees represent a paradigm shift in operational efficiency and strategic capability. These sophisticated digital entities offer unprecedented advantages:

• **Round-the-Clock Productivity**: Unlike traditional workforce models, AI employees operate continuously without interruption, ensuring seamless business operations across all time zones.

• **Precision and Consistency**: AI employees deliver consistent performance with minimal error rates, maintaining high-quality standards across repetitive and complex tasks alike.

• **Rapid Information Processing**: Capable of analyzing vast datasets and processing communications at extraordinary speeds, significantly reducing response times.

• **Cost Optimization**: Substantial reduction in operational costs while maintaining, or improving, service quality and output.

• **Scalability**: Effortlessly scale operations up or down based on demand without the complexities associated with human resource adjustments.

• **Integration Capability**: Seamlessly integrate with existing systems and workflows, enhancing rather than disrupting current operations.

• **Data-Driven Insights**: Provide valuable analytics and insights derived from continuous monitoring and processing of information streams.

The implementation of AI employees does not seek to replace human intelligence but rather to augment human capabilities, allowing professionals to focus on creative, strategic, and relationship-building activities that require uniquely human skills.

Organizations leveraging AI employees are witnessing remarkable improvements in operational efficiency, customer satisfaction, and competitive positioning. The technology enables businesses to remain agile and responsive in an ever-evolving marketplace.

Furthermore, AI employees contribute to sustainability initiatives by reducing the need for physical infrastructure and resources traditionally required for expanded human teams.

I invite you to join me for a comprehensive discussion on this topic:

**Meeting Invitation**
Date: Tomorrow
Time: 5:00 PM Sharp
Location: [To be confirmed - please respond with your preference]
Agenda: Deep dive into AI employee implementation strategies and benefits

Please confirm your attendance at your earliest convenience. I look forward to exploring this exciting frontier together and discussing how AI employees can revolutionize your operational framework.

Thank you for your continued interest in innovative solutions that drive success in the modern business landscape.

Warm regards,

Your AI Employee Assistant
Senior Digital Productivity Specialist
"""
        
        print(f"Sending detailed professional email to: {to_email}")
        print(f"Subject: {subject}")
        
        # Send the email
        result = sender.send_email(to_email, subject, body)
        
        if result:
            print(f"Detailed professional email sent successfully with ID: {result}")
            print("The AI employee has successfully sent a detailed professional email with a meeting invitation!")
        else:
            print("Failed to send email. Please check the logs for details.")
            
    except Exception as e:
        print(f"Error initializing Gmail sender: {e}")

if __name__ == "__main__":
    send_detailed_professional_email()
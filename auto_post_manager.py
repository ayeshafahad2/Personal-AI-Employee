#!/usr/bin/env python3
"""
Auto Post Manager - Main orchestrator for automated LinkedIn posting with WhatsApp notifications

Usage:
    python auto_post_manager.py                    # Run full automation
    python auto_post_manager.py --test             # Test connections only
    python auto_post_manager.py --post "Your text" # Post custom text
    python auto_post_manager.py --file path.txt    # Post from file
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from linkedin_auto_publisher import LinkedInAutoPublisher
from whatsapp_notifier import WhatsAppNotifier


class AutoPostManager:
    """Orchestrate LinkedIn auto-posting with WhatsApp notifications"""
    
    def __init__(self):
        self.publisher = None
        self.notifier = None
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize LinkedIn and WhatsApp services"""
        try:
            self.publisher = LinkedInAutoPublisher()
            print("✅ LinkedIn Auto Publisher initialized")
        except ValueError as e:
            print(f"⚠️  LinkedIn not configured: {e}")
        
        try:
            self.notifier = WhatsAppNotifier()
            print("✅ WhatsApp Notifier initialized")
        except ValueError as e:
            print(f"⚠️  WhatsApp not configured: {e}")
    
    def test_connections(self) -> dict:
        """
        Test all service connections
        
        Returns:
            dict with test results
        """
        results = {
            'linkedin': False,
            'whatsapp': False
        }
        
        print("\n" + "=" * 50)
        print("Testing Service Connections")
        print("=" * 50)
        
        if self.publisher:
            print("\nTesting LinkedIn...")
            results['linkedin'] = self.publisher.test_connection()
            print(f"LinkedIn: {'✅ PASSED' if results['linkedin'] else '❌ FAILED'}")
        else:
            print("LinkedIn: ⚠️  Not configured")
        
        if self.notifier:
            print("\nTesting WhatsApp...")
            results['whatsapp'] = self.notifier.test_connection()
            print(f"WhatsApp: {'✅ PASSED' if results['whatsapp'] else '❌ FAILED'}")
        else:
            print("WhatsApp: ⚠️  Not configured")
        
        print("\n" + "=" * 50)
        
        return results
    
    def publish_and_notify(self, post_content: str, send_notification: bool = True) -> dict:
        """
        Publish to LinkedIn and send WhatsApp notification
        
        Args:
            post_content: The content to publish
            send_notification: Whether to send WhatsApp notification
            
        Returns:
            dict with results
        """
        results = {
            'linkedin': None,
            'whatsapp': None,
            'timestamp': datetime.now().isoformat()
        }
        
        print("\n" + "=" * 50)
        print("Publishing LinkedIn Post")
        print("=" * 50)
        
        # Publish to LinkedIn
        if self.publisher:
            print("\nPublishing to LinkedIn...")
            results['linkedin'] = self.publisher.publish_post(post_content)
            
            if results['linkedin']['status'] == 'success':
                print(f"✅ Post published successfully!")
                print(f"Post URL: {results['linkedin'].get('post_url', 'N/A')}")
            else:
                print(f"❌ Failed to publish: {results['linkedin'].get('error', 'Unknown error')}")
        else:
            results['linkedin'] = {
                'status': 'error',
                'error': 'LinkedIn not configured'
            }
            print("❌ LinkedIn not configured")
        
        # Send WhatsApp notification
        if send_notification and self.notifier and results['linkedin']:
            print("\nSending WhatsApp notification...")
            
            if results['linkedin']['status'] == 'success':
                results['whatsapp'] = self.notifier.send_linkedin_post_notification(
                    post_content,
                    results['linkedin'].get('post_url')
                )
            else:
                results['whatsapp'] = self.notifier.send_message(
                    f"❌ LinkedIn post failed:\n{results['linkedin'].get('error', 'Unknown error')}"
                )
            
            if results['whatsapp']['status'] == 'success':
                print(f"✅ WhatsApp notification sent!")
            else:
                print(f"❌ WhatsApp failed: {results['whatsapp'].get('error', 'Unknown error')}")
        
        print("\n" + "=" * 50)
        print("Automation Complete")
        print("=" * 50)
        
        return results
    
    def run_demo_post(self) -> dict:
        """
        Run a demo post about Personal AI Employee
        
        Returns:
            dict with results
        """
        post_content = f"""The Future of Personal Productivity: Why Everyone Needs a Personal AI Employee

In today's fast-paced world, managing personal and business affairs can feel overwhelming. Between emails, messages, social media, and daily tasks, it's easy to miss important opportunities or deadlines.

What if you had a dedicated employee working 24/7 to handle routine tasks, flag important communications, and keep you organized? That's exactly what a Personal AI Employee system does!

Key Benefits:
• 24/7 Monitoring: Never miss important emails, messages, or opportunities
• Smart Filtering: Automatically identifies urgent vs. routine communications
• Task Automation: Handles repetitive tasks so you can focus on what matters
• Seamless Integration: Works across Gmail, WhatsApp, LinkedIn, and more
• Privacy First: All data stays on your local machine
• Human-in-the-Loop: Critical decisions still require your approval

With advanced AI systems, your personal AI employee can:
• Monitor your inbox and flag urgent requests
• Engage with your network on LinkedIn
• Schedule and manage appointments
• Generate reports and insights
• Handle routine inquiries

The result? More time for strategic thinking, creative work, and personal well-being. It's like having a senior executive assistant who never sleeps and gets smarter over time.

The future of productivity isn't about working harder—it's about working smarter with AI augmentation. A Personal AI Employee system transforms how you manage your digital life, turning technology into your competitive advantage.

Ready to explore the possibilities? The technology exists today to create your own digital FTE (Full-Time Equivalent).

#AI #Productivity #FutureOfWork #ArtificialIntelligence #PersonalAssistant #TechInnovation #DigitalTransformation #Automation #PersonalProductivity #LinkedInAPI

{datetime.now().strftime('%B %d, %Y')}
"""
        
        return self.publish_and_notify(post_content.strip())


def main():
    parser = argparse.ArgumentParser(
        description='Auto Post Manager - Automated LinkedIn posting with WhatsApp notifications',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_post_manager.py                    # Run full automation with demo post
  python auto_post_manager.py --test             # Test all connections
  python auto_post_manager.py --post "Hello!"    # Post custom text
  python auto_post_manager.py --file post.txt    # Post from file
  python auto_post_manager.py --no-notify        # Skip WhatsApp notification
        """
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test connections only (no posting)'
    )
    
    parser.add_argument(
        '--post',
        type=str,
        help='Custom post content to publish'
    )
    
    parser.add_argument(
        '--file',
        type=str,
        help='Path to file containing post content'
    )
    
    parser.add_argument(
        '--no-notify',
        action='store_true',
        help='Skip WhatsApp notification'
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("  AUTO POST MANAGER - LinkedIn + WhatsApp Automation")
    print("=" * 60)
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    manager = AutoPostManager()
    
    # Test mode
    if args.test:
        manager.test_connections()
        return
    
    # Custom post from command line
    if args.post:
        manager.publish_and_notify(args.post, send_notification=not args.no_notify)
        return
    
    # Post from file
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {args.file}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        manager.publish_and_notify(content, send_notification=not args.no_notify)
        return
    
    # Default: Run demo post
    print("\n🚀 Running automated demo post...")
    manager.run_demo_post()


if __name__ == '__main__':
    main()

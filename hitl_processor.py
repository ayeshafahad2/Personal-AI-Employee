#!/usr/bin/env python3
"""
HITL Approval Processor - Human-in-the-Loop approval workflow

Monitors the /Approved folder and executes actions that have been
approved by humans. Also handles expiration of pending approvals.

Usage:
    python hitl_processor.py              # Run continuously
    python hitl_processor.py --process    # Process approved items now
    python hitl_processor.py --cleanup    # Clean up expired approvals
"""

import os
import sys
import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class HITLProcessor:
    """Human-in-the-Loop approval processor"""
    
    def __init__(self, vault_path: str = None):
        """
        Initialize HITL processor
        
        Args:
            vault_path: Path to Obsidian vault
        """
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        
        if not self.vault_path.exists():
            raise ValueError(f"Vault not found: {self.vault_path}")
        
        # Folder paths
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure directories exist
        for folder in [self.pending_approval, self.approved, self.rejected, 
                       self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Approval expiry (default: 24 hours)
        self.approval_expiry_hours = int(os.getenv('APPROVAL_EXPIRY_HOURS', '24'))
    
    def _setup_logging(self):
        """Setup logging"""
        import logging
        log_file = self.logs / f'hitl_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('HITL')
    
    def process_approved(self) -> int:
        """
        Process all approved items
        
        Returns:
            Number of items processed
        """
        self.logger.info("Processing approved items...")
        
        approved_files = list(self.approved.glob('*.md'))
        
        if not approved_files:
            self.logger.info("No approved items to process")
            return 0
        
        self.logger.info(f"Found {len(approved_files)} approved item(s)")
        
        processed_count = 0
        
        for approved_file in approved_files:
            try:
                result = self._execute_approval(approved_file)
                
                if result:
                    processed_count += 1
                    
            except Exception as e:
                self.logger.error(f"Error processing {approved_file.name}: {e}")
        
        self.logger.info(f"Processed {processed_count} item(s)")
        
        return processed_count
    
    def _execute_approval(self, approved_file: Path) -> bool:
        """
        Execute an approved action
        
        Args:
            approved_file: Path to approved file
            
        Returns:
            True if successfully executed
        """
        self.logger.info(f"Executing approval: {approved_file.name}")
        
        # Read the approved file
        content = approved_file.read_text(encoding='utf-8')
        
        # Parse frontmatter to get action type
        import re
        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        
        action_type = "general"
        action_details = {}
        
        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if key == 'action':
                        action_type = value
                    elif key == 'type':
                        action_type = value
                    else:
                        action_details[key] = value
        
        # Execute based on action type
        success = False
        
        if action_type == 'email_draft':
            success = self._execute_email_approval(approved_file, action_details)
        elif action_type == 'payment':
            success = self._execute_payment_approval(approved_file, action_details)
        elif action_type == 'linkedin_post':
            success = self._execute_linkedin_approval(approved_file, action_details)
        else:
            success = self._execute_general_approval(approved_file, action_details)
        
        if success:
            # Move to Done
            dest = self.done / approved_file.name
            try:
                shutil.move(str(approved_file), str(dest))
                self.logger.info(f"Moved {approved_file.name} to Done")
                
                # Update dashboard
                self._update_dashboard(f"Approved action completed: {approved_file.name}")
                
            except Exception as e:
                self.logger.error(f"Could not move file to Done: {e}")
        
        return success
    
    def _execute_email_approval(self, approved_file: Path, details: dict) -> bool:
        """Execute approved email send"""
        self.logger.info("Executing email send...")
        
        to = details.get('to', '')
        subject = details.get('subject', '')
        cc = details.get('cc', '')
        
        if not to or not subject:
            self.logger.error("Missing email to/subject")
            return False
        
        # Extract email body from content
        content = approved_file.read_text(encoding='utf-8')
        body_match = re.search(r'## Body\n+(.+?)(?=##|\Z)', content, re.DOTALL)
        body = body_match.group(1).strip() if body_match else "No body"
        
        # Send email using agent_skills
        try:
            from agent_skills import AgentSkills
            skills = AgentSkills(str(self.vault_path))
            
            result = skills.send_email(
                to=to,
                subject=subject,
                body=body,
                cc=cc if cc else None
            )
            
            if result.get('status') == 'success':
                self.logger.info(f"Email sent to {to}")
                self._log_action('email_send', {'to': to, 'subject': subject}, 'success')
                return True
            else:
                self.logger.error(f"Email send failed: {result.get('error')}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False
    
    def _execute_payment_approval(self, approved_file: Path, details: dict) -> bool:
        """Execute approved payment"""
        self.logger.info("Payment approval detected - requires manual execution")
        
        # Payments should be executed manually by human
        # Just log and move to Done
        
        amount = details.get('amount', 'Unknown')
        recipient = details.get('recipient', 'Unknown')
        
        self.logger.info(f"Payment approved: ${amount} to {recipient}")
        self._log_action('payment_approved', {
            'amount': amount,
            'recipient': recipient,
            'status': 'requires_manual_execution'
        })
        
        # Update dashboard
        self._update_dashboard(f"Payment approved: ${amount} to {recipient} (pending manual execution)")
        
        return True
    
    def _execute_linkedin_approval(self, approved_file: Path, details: dict) -> bool:
        """Execute approved LinkedIn post"""
        self.logger.info("Executing LinkedIn post...")
        
        # Extract post content
        content = approved_file.read_text(encoding='utf-8')
        
        # Look for post content in the file
        body_match = re.search(r'## Post Content\n+(.+?)(?=##|\Z)', content, re.DOTALL)
        
        if not body_match:
            # Use entire content minus frontmatter
            frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
            if frontmatter_match:
                post_content = content[frontmatter_match.end():].strip()
            else:
                post_content = content
        else:
            post_content = body_match.group(1).strip()
        
        # Publish to LinkedIn
        try:
            from linkedin_auto_publisher import LinkedInAutoPublisher
            publisher = LinkedInAutoPublisher()
            
            result = publisher.publish_post(post_content)
            
            if result.get('status') == 'success':
                post_url = result.get('post_url', 'Unknown')
                self.logger.info(f"LinkedIn post published: {post_url}")
                self._log_action('linkedin_post', {'url': post_url}, 'success')
                self._update_dashboard(f"LinkedIn post published: {post_url}")
                return True
            else:
                self.logger.error(f"LinkedIn post failed: {result.get('error')}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error publishing LinkedIn post: {e}")
            return False
    
    def _execute_general_approval(self, approved_file: Path, details: dict) -> bool:
        """Execute general approval - just log and move to Done"""
        self.logger.info("Executing general approval...")
        
        action = details.get('action', 'unknown')
        
        self._log_action('general_approval', {'action': action}, 'success')
        self._update_dashboard(f"General approval executed: {action}")
        
        return True
    
    def cleanup_expired(self) -> int:
        """
        Clean up expired pending approvals
        
        Returns:
            Number of items cleaned up
        """
        self.logger.info("Cleaning up expired approvals...")
        
        pending_files = list(self.pending_approval.glob('*.md'))
        expiry_threshold = datetime.now() - timedelta(hours=self.approval_expiry_hours)
        
        cleaned_count = 0
        
        for pending_file in pending_files:
            try:
                # Check file modification time
                mtime = datetime.fromtimestamp(pending_file.stat().st_mtime)
                
                if mtime < expiry_threshold:
                    # Move to Rejected
                    dest = self.rejected / pending_file.name
                    shutil.move(str(pending_file), str(dest))
                    
                    self.logger.info(f"Expired approval moved to Rejected: {pending_file.name}")
                    cleaned_count += 1
                    
            except Exception as e:
                self.logger.error(f"Error processing {pending_file.name}: {e}")
        
        self.logger.info(f"Cleaned up {cleaned_count} expired approval(s)")
        
        return cleaned_count
    
    def _log_action(self, action_type: str, details: dict, result: str):
        """Log action to audit log"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'actor': 'hitl_processor',
            'parameters': details,
            'result': result
        }
        
        log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}.json'
        
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def _update_dashboard(self, entry: str):
        """Update dashboard with entry"""
        if not self.dashboard.exists():
            return
        
        content = self.dashboard.read_text(encoding='utf-8')
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = f"- [{timestamp}] {entry}"
        
        import re
        if '## Recent Activity' in content:
            pattern = r'(## Recent Activity\n\n)'
            content = re.sub(pattern, f'\\1{new_entry}\n', content, count=1)
        else:
            content += f"\n## Recent Activity\n\n{new_entry}\n"
        
        self.dashboard.write_text(content, encoding='utf-8')
    
    def run(self, interval: int = 60):
        """
        Run processor in loop
        
        Args:
            interval: Seconds between checks
        """
        self.logger.info(f"Starting HITL Processor (interval: {interval}s)")
        
        import time
        
        while True:
            try:
                # Process approved items
                self.process_approved()
                
                # Cleanup expired (every hour)
                if datetime.now().minute == 0:
                    self.cleanup_expired()
                
            except Exception as e:
                self.logger.error(f"Error in processor loop: {e}")
            
            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description='HITL Approval Processor')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault', help='Vault path')
    parser.add_argument('--process', action='store_true', help='Process approved items now')
    parser.add_argument('--cleanup', action='store_true', help='Clean up expired approvals')
    parser.add_argument('--interval', type=int, default=60, help='Check interval in seconds')
    
    args = parser.parse_args()
    
    try:
        processor = HITLProcessor(args.vault)
    except ValueError as e:
        print(f"ERROR: {e}")
        return
    
    print("=" * 60)
    print("  HITL APPROVAL PROCESSOR")
    print("=" * 60)
    print(f"  Vault: {processor.vault_path}")
    print("=" * 60)
    
    if args.cleanup:
        count = processor.cleanup_expired()
        print(f"\nCleaned up {count} expired approval(s)")
        return
    
    if args.process:
        count = processor.process_approved()
        print(f"\nProcessed {count} approved item(s)")
        return
    
    # Default: Run in loop
    print(f"\nStarting processor loop (interval: {args.interval}s)")
    print("Press Ctrl+C to stop")
    
    try:
        processor.run(interval=args.interval)
    except KeyboardInterrupt:
        print("\n\nStopping Processor...")


if __name__ == '__main__':
    main()

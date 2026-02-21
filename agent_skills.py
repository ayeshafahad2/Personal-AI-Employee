#!/usr/bin/env python3
"""
Agent Skills - Reusable skills for AI Employee

These skills can be invoked by Claude Code to perform specific tasks.
Each skill is a self-contained function that can be called programmatically.

Usage:
    from agent_skills import AgentSkills
    
    skills = AgentSkills(vault_path='AI_Employee_Vault')
    skills.send_email(to='example@email.com', subject='Hello', body='Test')
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()


class AgentSkills:
    """Collection of reusable skills for AI Employee"""
    
    def __init__(self, vault_path: str = None):
        """
        Initialize Agent Skills
        
        Args:
            vault_path: Path to Obsidian vault (default: AI_Employee_Vault)
        """
        self.vault_path = Path(vault_path or 'AI_Employee_Vault').absolute()
        
        if not self.vault_path.exists():
            raise ValueError(f"Vault not found: {self.vault_path}")
        
        # Folder paths
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.done = self.vault_path / 'Done'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure directories exist
        for folder in [self.needs_action, self.plans, self.done,
                       self.pending_approval, self.approved, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging"""
        import logging
        log_file = self.logs / f'skills_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AgentSkills')
    
    def log_action(self, action_type: str, details: Dict, result: str = 'success'):
        """
        Log an action to the audit log
        
        Args:
            action_type: Type of action (email_send, file_move, etc.)
            details: Dict with action details
            result: success, failed, skipped
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'actor': 'agent_skills',
            'parameters': details,
            'result': result
        }
        
        log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}.json'
        
        # Load existing logs
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
        
        self.logger.info(f"Logged action: {action_type} - {result}")
    
    # === FILE OPERATIONS ===
    
    def move_to_done(self, file_pattern: str, source_folder: str = 'In_Progress') -> List[Path]:
        """
        Move files matching pattern to Done folder
        
        Args:
            file_pattern: Glob pattern (e.g., '*.md', 'EMAIL_*')
            source_folder: Source folder name
            
        Returns:
            List of moved file paths
        """
        source = self.vault_path / source_folder
        if not source.exists():
            self.logger.warning(f"Source folder not found: {source}")
            return []
        
        # Handle nested folders (In_Progress/<agent>/)
        moved = []
        for subdir in source.iterdir():
            if subdir.is_dir():
                for file in subdir.glob(file_pattern):
                    try:
                        dest = self.done / file.name
                        shutil.move(str(file), str(dest))
                        moved.append(dest)
                        self.logger.info(f"Moved {file.name} to Done")
                    except Exception as e:
                        self.logger.error(f"Could not move {file.name}: {e}")
        
        # Also check root of source folder
        for file in source.glob(file_pattern):
            try:
                dest = self.done / file.name
                shutil.move(str(file), str(dest))
                moved.append(dest)
                self.logger.info(f"Moved {file.name} to Done")
            except Exception as e:
                self.logger.error(f"Could not move {file.name}: {e}")
        
        self.log_action('file_move', {
            'pattern': file_pattern,
            'source': source_folder,
            'destination': 'Done',
            'count': len(moved)
        })
        
        return moved
    
    def move_to_pending_approval(self, file_path: Path, reason: str = None) -> Path:
        """
        Move a file to Pending_Approval folder
        
        Args:
            file_path: Path to file
            reason: Reason for approval request
            
        Returns:
            Path to moved file
        """
        if not file_path.exists():
            self.logger.error(f"File not found: {file_path}")
            return None
        
        dest = self.pending_approval / file_path.name
        
        try:
            shutil.move(str(file_path), str(dest))
            
            # Add reason to file if provided
            if reason:
                content = dest.read_text(encoding='utf-8')
                content += f"\n\n## Approval Reason\n\n{reason}\n"
                dest.write_text(content, encoding='utf-8')
            
            self.logger.info(f"Moved {file_path.name} to Pending_Approval")
            
            self.log_action('file_move', {
                'file': str(file_path),
                'destination': 'Pending_Approval',
                'reason': reason
            })
            
            return dest
            
        except Exception as e:
            self.logger.error(f"Could not move file: {e}")
            return None
    
    def create_plan(self, title: str, steps: List[str], context: str = None) -> Path:
        """
        Create a plan file in the Plans folder
        
        Args:
            title: Plan title
            steps: List of step descriptions
            context: Optional context/objective
            
        Returns:
            Path to created plan file
        """
        # Create filename
        safe_title = title.replace(' ', '_').replace('/', '_')[:50]
        filename = f'PLAN_{safe_title}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath = self.plans / filename
        
        content = f'''---
type: plan
title: {title}
created: {datetime.now().isoformat()}
status: pending
---

# Plan: {title}

## Objective

{context or 'Process the associated action item'}

## Steps

'''
        
        for i, step in enumerate(steps, 1):
            content += f"{i}. [ ] {step}\n"
        
        content += f'''

## Notes

_Add notes during execution_


## Completion Checklist

- [ ] All steps completed
- [ ] Files moved to Done
- [ ] Dashboard updated

'''
        
        filepath.write_text(content, encoding='utf-8')
        
        self.logger.info(f"Created plan: {filename}")
        
        self.log_action('plan_created', {
            'title': title,
            'steps': len(steps),
            'file': str(filepath)
        })
        
        return filepath
    
    def create_approval_request(self, action_type: str, details: Dict, file_path: Path = None) -> Path:
        """
        Create an approval request file
        
        Args:
            action_type: Type of action requiring approval
            details: Dict with action details
            file_path: Optional associated file
            
        Returns:
            Path to created approval request
        """
        filename = f'APPROVAL_{action_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath = self.pending_approval / filename
        
        content = f'''---
type: approval_request
action: {action_type}
created: {datetime.now().isoformat()}
status: pending
expires: {(datetime.now() + timedelta(days=1)).isoformat()}
---

# Approval Required: {action_type}

## Details

'''
        
        for key, value in details.items():
            content += f"**{key}:** {value}\n"
        
        content += f'''

## Instructions

- **To Approve:** Move this file to /Approved folder
- **To Reject:** Move this file to /Rejected folder

## Approval Log

- Requested: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Approved by: _Pending_
- Approved at: _Pending_

'''
        
        if file_path:
            content += f"\n**Associated File:** {file_path.name}\n"
        
        filepath.write_text(content, encoding='utf-8')
        
        self.logger.info(f"Created approval request: {filename}")
        
        self.log_action('approval_request', {
            'type': action_type,
            'details': details
        })
        
        return filepath
    
    # === EMAIL OPERATIONS ===
    
    def draft_email(self, to: str, subject: str, body: str, 
                    cc: str = None, requires_approval: bool = True) -> Path:
        """
        Draft an email (requires approval to send)
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body
            cc: Optional CC recipient
            requires_approval: Whether approval is needed (default: True)
            
        Returns:
            Path to draft file
        """
        filename = f'EMAIL_DRAFT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath = self.pending_approval / filename
        
        content = f'''---
type: email_draft
to: {to}
subject: {subject}
cc: {cc or 'N/A'}
created: {datetime.now().isoformat()}
status: pending_approval
---

# Email Draft

**To:** {to}
**Subject:** {subject}
**CC:** {cc or 'N/A'}


## Body

{body}


## Approval

Move this file to /Approved to send, or /Rejected to discard.

'''
        
        filepath.write_text(content, encoding='utf-8')
        
        self.logger.info(f"Created email draft: {filename}")
        
        self.log_action('email_draft', {
            'to': to,
            'subject': subject,
            'requires_approval': requires_approval
        })
        
        return filepath
    
    def send_email(self, to: str, subject: str, body: str, 
                   cc: str = None, attachment: Path = None) -> Dict:
        """
        Send an email via Gmail API
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body
            cc: Optional CC recipient
            attachment: Optional attachment path
            
        Returns:
            Dict with status and message_id
        """
        self.logger.info(f"Sending email to {to}: {subject}")
        
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.errors import HttpError
            import base64
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.base import MIMEBase
            from email import encoders
            
            # Load credentials
            token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
            
            if not Path(token_path).exists():
                raise ValueError("Gmail token not found. Run gmail_watcher.py --auth first")
            
            creds = Credentials.from_authorized_user_file(token_path, [
                'https://www.googleapis.com/auth/gmail.send'
            ])
            
            service = build('gmail', 'v1', credentials=creds)
            
            # Create message
            message = MIMEMultipart()
            message['to'] = to
            message['from'] = 'me'
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            
            message.attach(MIMEText(body, 'plain'))
            
            # Add attachment if provided
            if attachment and attachment.exists():
                with open(attachment, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{attachment.name}"'
                    )
                    message.attach(part)
            
            # Encode and send
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            result = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            self.logger.info(f"Email sent: {result['id']}")
            
            self.log_action('email_send', {
                'to': to,
                'subject': subject,
                'message_id': result['id']
            }, 'success')
            
            return {
                'status': 'success',
                'message_id': result['id']
            }
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            
            self.log_action('email_send', {
                'to': to,
                'subject': subject
            }, 'failed')
            
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    # === DASHBOARD OPERATIONS ===
    
    def update_dashboard(self, entry: str, section: str = 'Recent Activity'):
        """
        Update the dashboard with a new entry
        
        Args:
            entry: Entry text to add
            section: Section to update
        """
        if not self.dashboard.exists():
            self.dashboard.write_text("# AI Employee Dashboard\n\n")
        
        content = self.dashboard.read_text(encoding='utf-8')
        
        # Create timestamped entry
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = f"- [{timestamp}] {entry}"
        
        # Add to recent activity
        import re
        
        if f'## {section}' in content:
            # Insert after section header
            pattern = rf'(## {section}\n\n)'
            content = re.sub(pattern, f'\\1{new_entry}\n', content, count=1)
        else:
            # Add new section
            content += f"\n## {section}\n\n{new_entry}\n"
        
        self.dashboard.write_text(content, encoding='utf-8')
        self.logger.info(f"Updated dashboard: {entry[:50]}...")
    
    # === UTILITY METHODS ===
    
    def get_pending_items(self) -> List[Path]:
        """Get list of pending items in Needs_Action"""
        return list(self.needs_action.glob('*.md'))
    
    def get_approval_requests(self) -> List[Path]:
        """Get list of pending approval requests"""
        return list(self.pending_approval.glob('*.md'))
    
    def read_action_file(self, file_path: Path) -> Dict:
        """
        Read and parse an action file
        
        Args:
            file_path: Path to action file
            
        Returns:
            Dict with file metadata and content
        """
        if not file_path.exists():
            return None
        
        content = file_path.read_text(encoding='utf-8')
        
        # Parse frontmatter
        import re
        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        
        frontmatter = {}
        body = content
        
        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            body = content[frontmatter_match.end():]
        
        return {
            'path': str(file_path),
            'name': file_path.name,
            'frontmatter': frontmatter,
            'body': body,
            'content': content
        }


# Import timedelta for approval request expiry
from datetime import timedelta


if __name__ == '__main__':
    # Test the skills
    print("Testing Agent Skills...")
    
    try:
        skills = AgentSkills()
        print("✅ Agent Skills initialized")
        
        # Test getting pending items
        pending = skills.get_pending_items()
        print(f"Pending items: {len(pending)}")
        
        # Test dashboard update
        skills.update_dashboard("Test entry from Agent Skills")
        print("✅ Dashboard updated")
        
    except Exception as e:
        print(f"Error: {e}")

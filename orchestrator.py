#!/usr/bin/env python3
"""
Orchestrator - Master process for AI Employee System

Manages watchers, triggers Claude Code processing, and handles
the human-in-the-loop approval workflow.

Usage:
    python orchestrator.py              # Run full orchestration
    python orchestrator.py --process    # Process Needs_Action folder now
    python orchestrator.py --watchers   # Start all watchers
    python orchestrator.py --briefing   # Generate CEO briefing
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class Orchestrator:
    """Master orchestrator for AI Employee system"""
    
    def __init__(self, vault_path: str = None):
        """
        Initialize orchestrator
        
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
        self.rejected = self.vault_path / 'Rejected'
        self.logs = self.vault_path / 'Logs'
        self.briefings = self.vault_path / 'Briefings'
        self.in_progress = self.vault_path / 'In_Progress'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure all directories exist
        for folder in [self.needs_action, self.plans, self.done, 
                       self.pending_approval, self.approved, self.rejected,
                       self.logs, self.briefings, self.in_progress]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Claude Code command (or Qwen)
        self.claude_cmd = os.getenv('AI_COMMAND', 'claude')  # Use 'qwen' or custom command
        
        # Agent name for claim-by-move
        self.agent_name = os.getenv('AGENT_NAME', 'orchestrator')
    
    def _setup_logging(self):
        """Setup logging"""
        import logging
        log_file = self.logs / f'orchestrator_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Orchestrator')
    
    def process_needs_action(self, max_items: int = 5) -> int:
        """
        Process items in Needs_Action folder using Claude Code
        
        Args:
            max_items: Maximum items to process per run
            
        Returns:
            Number of items processed
        """
        self.logger.info(f"Processing Needs_Action folder...")
        
        # Get all action files
        action_files = list(self.needs_action.glob('*.md'))
        
        if not action_files:
            self.logger.info("No items to process")
            return 0
        
        # Limit items
        action_files = action_files[:max_items]
        self.logger.info(f"Found {len(action_files)} item(s) to process")
        
        processed_count = 0
        
        for action_file in action_files:
            try:
                # Claim the item (move to In_Progress)
                claimed = self._claim_item(action_file)
                
                if not claimed:
                    self.logger.warning(f"Could not claim {action_file.name}, skipping")
                    continue
                
                # Process with Claude Code
                result = self._process_with_claude(action_file)
                
                if result:
                    processed_count += 1
                    
            except Exception as e:
                self.logger.error(f"Error processing {action_file.name}: {e}")
        
        self.logger.info(f"Processed {processed_count} item(s)")
        self._update_dashboard()
        
        return processed_count
    
    def _claim_item(self, action_file: Path) -> bool:
        """
        Claim an item by moving to In_Progress/<agent>/
        
        Args:
            action_file: Path to action file
            
        Returns:
            True if successfully claimed
        """
        agent_dir = self.in_progress / self.agent_name
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        dest = agent_dir / action_file.name
        
        try:
            action_file.rename(dest)
            self.logger.info(f"Claimed {action_file.name}")
            return True
        except Exception as e:
            self.logger.error(f"Could not claim {action_file.name}: {e}")
            return False
    
    def _process_with_claude(self, action_file: Path) -> bool:
        """
        Process an action file with AI assistant (Claude Code or Qwen)

        Args:
            action_file: Path to action file (in In_Progress)

        Returns:
            True if successfully processed
        """
        self.logger.info(f"Processing with AI Assistant: {action_file.name}")

        # Read the action file
        content = action_file.read_text(encoding='utf-8')

        # Create a plan first
        plan_file = self._create_plan_for_action(action_file, content)
        self.logger.info(f"Created plan: {plan_file.name}")

        # Create a prompt for AI
        prompt = self._create_claude_prompt(action_file, content, plan_file)

        # Run AI assistant (Claude Code or Qwen)
        try:
            # Check if using Qwen API or Claude Code CLI
            if self.claude_cmd.lower() == 'qwen':
                # Use Qwen API directly
                result = self._run_qwen_api(prompt)
            else:
                # Use CLI command (Claude Code or other)
                result = subprocess.run(
                    [self.claude_cmd, '--prompt', prompt],
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                result = {
                    'success': result.returncode == 0,
                    'output': result.stdout if result.returncode == 0 else None,
                    'error': result.stderr if result.returncode != 0 else None
                }

            if result.get('success'):
                self.logger.info(f"AI processed {action_file.name} successfully")
                self._execute_claude_actions(action_file, result.get('output', ''))
                return True
            else:
                self.logger.error(f"AI error: {result.get('error')}")
                return False

        except Exception as e:
            self.logger.error(f"Error running AI: {e}")
            return False

    def _run_qwen_api(self, prompt: str) -> dict:
        """
        Run Qwen API directly
        
        Args:
            prompt: Prompt to send to Qwen
            
        Returns:
            Dict with success status and output
        """
        try:
            import requests
            
            # Get Qwen API credentials from .env
            api_key = os.getenv('DASHSCOPE_API_KEY', '')
            if not api_key:
                # Try Alibaba Cloud credentials
                api_key = os.getenv('ALIBABA_CLOUD_API_KEY', '')
            
            if not api_key:
                return {
                    'success': False,
                    'error': 'DASHSCOPE_API_KEY or ALIBABA_CLOUD_API_KEY not set in .env'
                }
            
            # Qwen API endpoint (DashScope)
            url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': os.getenv('QWEN_MODEL', 'qwen-max'),
                'input': {
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are an AI Employee assistant. Process tasks according to company guidelines.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                },
                'parameters': {
                    'max_tokens': 4000,
                    'temperature': 0.7
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=300)
            response.raise_for_status()
            
            result_data = response.json()
            output = result_data.get('output', {}).get('text', '')
            
            return {
                'success': True,
                'output': output
            }
            
        except requests.exceptions.HTTPError as e:
            return {
                'success': False,
                'error': f'API Error: {e.response.status_code} - {e.response.text}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_plan_for_action(self, action_file: Path, content: str) -> Path:
        """
        Create a Plan.md file for an action item
        
        Args:
            action_file: Path to action file
            content: Action file content
            
        Returns:
            Path to created plan file
        """
        # Parse action type from frontmatter
        import re
        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        
        action_type = "general"
        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)
            for line in frontmatter_text.split('\n'):
                if 'type:' in line.lower():
                    action_type = line.split(':')[1].strip()
                    break
        
        # Create plan filename
        safe_name = action_file.stem[:50]
        plan_filename = f'PLAN_{safe_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        plan_filepath = self.plans / plan_filename
        
        # Generate plan content based on action type
        if action_type == 'email':
            steps = [
                "Read and analyze the email content",
                "Determine if reply is needed or if it should be forwarded",
                "Check if the email requires human approval (sensitive topics, new contacts)",
                "Draft reply or create approval request if needed",
                "Send email via MCP email server (if auto-approved)",
                "Move action file to Done folder"
            ]
        elif action_type == 'file_drop':
            steps = [
                "Read the file content and understand what needs to be done",
                "Determine if file requires processing or just archival",
                "Check if any action is needed based on file content",
                "Create approval request if sensitive action required",
                "Process file according to Company Handbook rules",
                "Move file and action item to Done folder"
            ]
        elif action_type == 'linkedin_post':
            steps = [
                "Review the LinkedIn post content",
                "Check if post aligns with Business_Goals.md",
                "Verify post follows company guidelines",
                "Create approval request for human review",
                "Publish via MCP LinkedIn server after approval",
                "Log post to vault and update Dashboard",
                "Move to Done folder"
            ]
        else:
            steps = [
                "Analyze the action item and understand requirements",
                "Check Company_Handbook.md for relevant rules",
                "Determine if human approval is required",
                "Execute action or create approval request",
                "Update Dashboard with progress",
                "Move to Done folder when complete"
            ]
        
        plan_content = f'''---
type: plan
title: Process {action_type} action
created: {datetime.now().isoformat()}
status: in_progress
action_file: {action_file.name}
---

# Plan: Process {action_type} Action

## Objective

Process the action item from {action_file.name} according to company guidelines.

## Steps

'''
        
        for i, step in enumerate(steps, 1):
            plan_content += f"{i}. [ ] {step}\n"
        
        plan_content += f'''

## Resources

- Company Handbook: ../Company_Handbook.md
- Business Goals: ../Business_Goals.md
- Dashboard: ../Dashboard.md

## MCP Tools Available

- **email**: send_email, draft_email, search_emails
- **browser**: navigate, click, fill, get_text, screenshot
- **linkedin**: publish_post, publish_from_file
- **filesystem**: read, write, list files

## Execution Log

'''
        
        plan_content += f'''
- [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Plan created
- [_] Claude Code processing started
- [_] Actions executed
- [_] Files moved to Done

## Notes

_Add notes during execution_

'''
        
        plan_filepath.write_text(plan_content, encoding='utf-8')
        
        return plan_filepath
    
    def _create_claude_prompt(self, action_file: Path, content: str, plan_file: Path = None) -> str:
        """Create a prompt for AI assistant (Claude/Qwen)"""

        # Read company handbook for context
        handbook_path = self.vault_path / 'Company_Handbook.md'
        handbook = handbook_path.read_text(encoding='utf-8') if handbook_path.exists() else ""

        # Read business goals
        goals_path = self.vault_path / 'Business_Goals.md'
        goals = goals_path.read_text(encoding='utf-8') if goals_path.exists() else ""

        # Read plan file if exists
        plan_content = ""
        if plan_file and plan_file.exists():
            plan_content = plan_file.read_text(encoding='utf-8')

        prompt = f"""You are an AI Employee assistant. Process the following action item according to the company handbook and business goals.

## Company Handbook
{handbook[:2000] if handbook else 'No handbook available'}

## Business Goals
{goals[:1000] if goals else 'No goals available'}

## Action Item
File: {action_file.name}

{content}

## Your Plan
{plan_content if plan_content else 'No plan file - create one first'}

## Your Tasks

1. Follow the plan created in {plan_file.name if plan_file else 'Plans folder'}
2. If the action requires human approval (payments, sensitive emails, etc.), create an approval request in Pending_Approval
3. If the action can be auto-approved, execute it using available tools
4. When complete, move all related files to the Done folder
5. Update the Dashboard.md with a summary of what was done
6. Update the plan file with completion status

## Output Format

After processing, output a summary in this format:

<summary>
- Action Type: [type]
- Status: [completed|pending_approval|needs_review]
- Files Created: [list]
- Next Steps: [list]
</summary>

Remember: Always follow the company handbook rules and escalate when in doubt.
"""

        return prompt
    
    def _execute_claude_actions(self, action_file: Path, claude_output: str):
        """
        Execute actions from Claude's output
        
        Args:
            action_file: Path to action file
            claude_output: Claude's output
        """
        # Parse output for summary
        import re
        
        summary_match = re.search(r'<summary>(.*?)</summary>', claude_output, re.DOTALL)
        
        if summary_match:
            summary = summary_match.group(1).strip()
            self.logger.info(f"Claude summary: {summary[:200]}...")
            
            # Move action file to Done if completed
            if 'Status: completed' in summary.lower():
                dest = self.done / action_file.name
                try:
                    action_file.rename(dest)
                    self.logger.info(f"Moved {action_file.name} to Done")
                except Exception as e:
                    self.logger.error(f"Could not move file: {e}")
        else:
            # No summary found, move back to Needs_Action for retry
            dest = self.needs_action / action_file.name
            try:
                action_file.rename(dest)
                self.logger.warning(f"Moved {action_file.name} back to Needs_Action (no summary)")
            except Exception as e:
                self.logger.error(f"Could not move file: {e}")
    
    def _update_dashboard(self):
        """Update the Dashboard.md with current status"""
        self.logger.info("Updating dashboard...")
        
        # Count items in each folder
        needs_action_count = len(list(self.needs_action.glob('*.md')))
        plans_count = len(list(self.plans.glob('*.md')))
        pending_approval_count = len(list(self.pending_approval.glob('*.md')))
        done_today = len([
            f for f in self.done.glob('*.md')
            if datetime.fromtimestamp(f.stat().st_mtime) > datetime.now() - timedelta(days=1)
        ])
        
        # Read current dashboard
        if self.dashboard.exists():
            content = self.dashboard.read_text(encoding='utf-8')
        else:
            content = "# AI Employee Dashboard\n\n"
        
        # Update status section
        status_section = f"""## Status: Active

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Queue Status
| Folder | Count |
|--------|-------|
| Needs Action | {needs_action_count} |
| In Progress | {self._count_in_progress()} |
| Pending Approval | {pending_approval_count} |
| Done (today) | {done_today} |

"""
        
        # Replace or add status section
        import re
        if re.search(r'## Status:', content):
            content = re.sub(r'## Status:.*?(?=##|\Z)', status_section, content, flags=re.DOTALL)
        else:
            content = status_section + content
        
        # Add recent activity
        recent_activity = self._get_recent_activity()
        if recent_activity:
            activity_section = "## Recent Activity\n\n" + "\n".join(recent_activity[:10])
            
            if re.search(r'## Recent Activity', content):
                content = re.sub(r'## Recent Activity.*?(?=##|\Z)', activity_section, content, flags=re.DOTALL)
            else:
                content += "\n" + activity_section
        
        self.dashboard.write_text(content, encoding='utf-8')
        self.logger.info("Dashboard updated")
    
    def _count_in_progress(self) -> int:
        """Count items in In_Progress folders"""
        count = 0
        for folder in self.in_progress.iterdir():
            if folder.is_dir():
                count += len(list(folder.glob('*.md')))
        return count
    
    def _get_recent_activity(self) -> list:
        """Get recent activity log entries"""
        activities = []
        
        # Check Done folder for recent completions
        done_files = sorted(
            self.done.glob('*.md'),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )[:5]
        
        for f in done_files:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            activities.append(f"- [{mtime.strftime('%Y-%m-%d %H:%M')}] Completed: {f.name}")
        
        return activities
    
    def generate_ceo_briefing(self) -> Path:
        """
        Generate a Monday Morning CEO Briefing
        
        Returns:
            Path to generated briefing file
        """
        self.logger.info("Generating CEO Briefing...")
        
        # Get this week's completed tasks
        week_ago = datetime.now() - timedelta(days=7)
        
        done_files = [
            f for f in self.done.glob('*.md')
            if datetime.fromtimestamp(f.stat().st_mtime) > week_ago
        ]
        
        # Get pending items
        pending_files = list(self.pending_approval.glob('*.md'))
        needs_action_files = list(self.needs_action.glob('*.md'))
        
        # Create briefing
        briefing_date = datetime.now().strftime('%Y-%m-%d')
        briefing_content = f'''# Monday Morning CEO Briefing

---
generated: {datetime.now().isoformat()}
period: {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}
---

## Executive Summary

This week's activity summary and key insights.

## Completed Tasks This Week

**Total:** {len(done_files)} tasks completed

'''
        
        # List completed tasks
        for f in done_files[:10]:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            briefing_content += f"- [x] {f.stem}\n"
        
        if len(done_files) > 10:
            briefing_content += f"- ... and {len(done_files) - 10} more\n"
        
        briefing_content += f'''

## Pending Approvals

**Total:** {len(pending_files)} items awaiting approval

'''
        
        for f in pending_files:
            briefing_content += f"- [ ] {f.stem}\n"
        
        briefing_content += f'''

## Bottlenecks

**Items in Needs_Action:** {len(needs_action_files)}

'''
        
        for f in needs_action_files[:5]:
            briefing_content += f"- ⚠️ {f.stem}\n"
        
        briefing_content += f'''

## Recommendations

Based on this week's activity:

1. Review pending approvals in the Pending_Approval folder
2. Process {len(needs_action_files)} items in Needs_Action
3. Consider automating frequently occurring task types

---
*Generated by AI Employee v0.1*
'''
        
        # Write briefing
        briefing_file = self.briefings / f'{briefing_date}_CEO_Briefing.md'
        briefing_file.write_text(briefing_content, encoding='utf-8')
        
        self.logger.info(f"Briefing generated: {briefing_file}")
        
        return briefing_file
    
    def start_watchers(self):
        """Start all watcher processes"""
        self.logger.info("Starting watchers...")
        
        watchers = []
        
        # Start Gmail Watcher
        gmail_watcher = Path(__file__).parent / 'watchers' / 'gmail_watcher.py'
        if gmail_watcher.exists():
            cmd = [sys.executable, str(gmail_watcher), '--vault', str(self.vault_path)]
            proc = subprocess.Popen(cmd)
            watchers.append(('Gmail', proc))
            self.logger.info("Started Gmail Watcher")
        
        # Start File System Watcher
        fs_watcher = Path(__file__).parent / 'watchers' / 'filesystem_watcher.py'
        if fs_watcher.exists():
            cmd = [sys.executable, str(fs_watcher), '--vault', str(self.vault_path)]
            proc = subprocess.Popen(cmd)
            watchers.append(('FileSystem', proc))
            self.logger.info("Started File System Watcher")
        
        return watchers
    
    def run(self, interval: int = 300):
        """
        Run the orchestrator in a loop
        
        Args:
            interval: Seconds between processing runs (default: 300 = 5 min)
        """
        self.logger.info(f"Starting Orchestrator (interval: {interval}s)")
        
        import time
        
        while True:
            try:
                # Process needs action
                self.process_needs_action()
                
                # Update dashboard
                self._update_dashboard()
                
            except Exception as e:
                self.logger.error(f"Error in orchestrator loop: {e}")
            
            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault', help='Path to Obsidian vault')
    parser.add_argument('--process', action='store_true', help='Process Needs_Action folder now')
    parser.add_argument('--watchers', action='store_true', help='Start all watchers')
    parser.add_argument('--briefing', action='store_true', help='Generate CEO briefing')
    parser.add_argument('--interval', type=int, default=300, help='Processing interval in seconds')
    
    args = parser.parse_args()
    
    try:
        orchestrator = Orchestrator(args.vault)
    except ValueError as e:
        print(f"ERROR: {e}")
        return
    
    print("=" * 60)
    print("  AI EMPLOYEE ORCHESTRATOR")
    print("=" * 60)
    print(f"  Vault: {orchestrator.vault_path}")
    print("=" * 60)
    
    if args.briefing:
        briefing_path = orchestrator.generate_ceo_briefing()
        print(f"\n✅ CEO Briefing generated: {briefing_path}")
        return
    
    if args.watchers:
        print("\nStarting watchers...")
        watchers = orchestrator.start_watchers()
        print(f"Started {len(watchers)} watcher(s)")
        
        # Keep running
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nStopping watchers...")
            for name, proc in watchers:
                proc.terminate()
        return
    
    if args.process:
        count = orchestrator.process_needs_action()
        print(f"\n✅ Processed {count} item(s)")
        return
    
    # Default: Run in loop
    print(f"\nStarting orchestrator loop (interval: {args.interval}s)")
    print("Press Ctrl+C to stop")
    
    try:
        orchestrator.run(interval=args.interval)
    except KeyboardInterrupt:
        print("\n\nStopping Orchestrator...")


if __name__ == '__main__':
    main()

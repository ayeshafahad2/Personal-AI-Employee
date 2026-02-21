#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Keep Claude Code working until task is complete

This implements the "Ralph Wiggum" pattern - a Stop hook that intercepts
Claude's exit and re-injects the prompt if the task is not complete.

The loop continues until:
1. Task file is moved to /Done (completion)
2. Max iterations reached
3. User interrupts

Usage:
    python ralph_wiggum.py "Process all files in Needs_Action" --vault AI_Employee_Vault
    python ralph_wiggum.py "Generate weekly report" --max-iterations 5
"""

import os
import sys
import argparse
import subprocess
import signal
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class RalphWiggumLoop:
    """Keep Claude Code working until task completion"""
    
    def __init__(self, vault_path: str, max_iterations: int = 10,
                 completion_signal: str = 'TASK_COMPLETE'):
        """
        Initialize Ralph Wiggum Loop
        
        Args:
            vault_path: Path to Obsidian vault
            max_iterations: Maximum loop iterations
            completion_signal: String Claude should output when done
        """
        self.vault_path = Path(vault_path).absolute()
        
        if not self.vault_path.exists():
            raise ValueError(f"Vault not found: {self.vault_path}")
        
        self.max_iterations = max_iterations
        self.completion_signal = completion_signal
        
        # Folder paths
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.logs = self.vault_path / 'Logs'
        
        # Ensure directories exist
        for folder in [self.needs_action, self.done, self.plans, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Claude Code command
        self.claude_cmd = os.getenv('CLAUDE_COMMAND', 'claude')
        
        # Track iterations
        self.iteration = 0
        self.conversation_history = []
    
    def _setup_logging(self):
        """Setup logging"""
        import logging
        log_file = self.logs / f'ralph_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('RalphWiggum')
    
    def is_task_complete(self) -> bool:
        """
        Check if the task is complete
        
        Returns:
            True if task is complete (no items in Needs_Action)
        """
        # Check if Needs_Action is empty
        pending = list(self.needs_action.glob('*.md'))
        
        if pending:
            self.logger.info(f"Task not complete: {len(pending)} items pending")
            return False
        
        self.logger.info("Task complete: Needs_Action is empty")
        return True
    
    def get_task_status(self) -> dict:
        """
        Get current task status
        
        Returns:
            Dict with status information
        """
        return {
            'needs_action': len(list(self.needs_action.glob('*.md'))),
            'plans': len(list(self.plans.glob('*.md'))),
            'done': len(list(self.done.glob('*.md'))),
            'iteration': self.iteration
        }
    
    def create_state_file(self, prompt: str) -> Path:
        """
        Create a state file for the current task
        
        Args:
            prompt: Current prompt
            
        Returns:
            Path to state file
        """
        state_file = self.logs / f'ralph_state_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        content = f'''---
type: ralph_state
created: {datetime.now().isoformat()}
iteration: {self.iteration}
status: in_progress
---

# Ralph Wiggum Loop State

## Current Prompt

{prompt}

## Iteration History

'''
        
        for i, entry in enumerate(self.conversation_history, 1):
            content += f"### Iteration {i}\n\n"
            content += f"**Time:** {entry.get('timestamp', 'Unknown')}\n"
            content += f"**Status:** {entry.get('status', 'Unknown')}\n\n"
        
        content += f'''

## Completion Criteria

Task is complete when:
1. Needs_Action folder is empty
2. All files moved to Done
3. Claude outputs: {self.completion_signal}

'''
        
        state_file.write_text(content, encoding='utf-8')
        return state_file
    
    def run(self, initial_prompt: str):
        """
        Run the Ralph Wiggum loop
        
        Args:
            initial_prompt: Initial prompt for Claude
        """
        self.logger.info(f"Starting Ralph Wiggum Loop")
        self.logger.info(f"Vault: {self.vault_path}")
        self.logger.info(f"Max iterations: {self.max_iterations}")
        
        print("=" * 60)
        print("  RALPH WIGGUM LOOP - Autonomous Task Completion")
        print("=" * 60)
        print(f"  Vault: {self.vault_path}")
        print(f"  Max iterations: {self.max_iterations}")
        print(f"  Completion signal: {self.completion_signal}")
        print("=" * 60)
        
        # Create initial state file
        self.create_state_file(initial_prompt)
        
        current_prompt = initial_prompt
        
        while self.iteration < self.max_iterations:
            self.iteration += 1
            
            print(f"\n{'=' * 60}")
            print(f"  ITERATION {self.iteration}/{self.max_iterations}")
            print(f"{'=' * 60}")
            
            # Get task status
            status = self.get_task_status()
            print(f"  Needs Action: {status['needs_action']}")
            print(f"  Plans: {status['plans']}")
            print(f"  Done: {status['done']}")
            print(f"{'=' * 60}\n")
            
            # Check completion
            if self.is_task_complete():
                print("\n✅ TASK COMPLETE - Needs_Action folder is empty")
                self._log_iteration('complete', 'Task completed successfully')
                break
            
            # Run Claude
            print(f"Running Claude Code...")
            print(f"Prompt: {current_prompt[:100]}...")
            print("-" * 60)
            
            result = self._run_claude(current_prompt)
            
            if result['success']:
                output = result['output']
                
                # Check for completion signal
                if self.completion_signal in output:
                    print(f"\n✅ Completion signal detected: {self.completion_signal}")
                    self._log_iteration('complete', output[:500])
                    break
                
                # Extract summary from output
                summary = self._extract_summary(output)
                print(f"\nClaude output summary: {summary[:200]}...")
                
                # Prepare next prompt based on output
                current_prompt = self._prepare_next_prompt(current_prompt, output)
                
                self._log_iteration('success', output[:500])
                
            else:
                error = result.get('error', 'Unknown error')
                print(f"\n❌ Claude failed: {error}")
                self._log_iteration('error', error)
                
                # Retry with error context
                current_prompt = f"{current_prompt}\n\nPrevious attempt failed: {error}. Please retry."
        
        # Final status
        print(f"\n{'=' * 60}")
        if self.iteration >= self.max_iterations:
            print(f"  ⚠️  MAX ITERATIONS REACHED ({self.max_iterations})")
        else:
            print(f"  ✅ LOOP COMPLETED")
        
        final_status = self.get_task_status()
        print(f"  Final - Needs Action: {final_status['needs_action']}, Done: {final_status['done']}")
        print(f"{'=' * 60}\n")
        
        self.logger.info(f"Ralph Wiggum Loop finished after {self.iteration} iterations")
    
    def _run_claude(self, prompt: str) -> dict:
        """
        Run Claude Code with the given prompt
        
        Args:
            prompt: Prompt to send to Claude
            
        Returns:
            Dict with success status and output/error
        """
        try:
            # Build the command with context about the vault
            full_prompt = f"""You are working on an autonomous task in the AI Employee system.

Current working directory: {self.vault_path}

Your goal is to process all items in the Needs_Action folder and move them to Done when complete.

IMPORTANT: When you have completed the task, output exactly: {self.completion_signal}

## Task

{prompt}

## Available Folders

- Needs_Action: Items waiting to be processed
- Plans: Your planning documents
- Done: Completed items
- Pending_Approval: Items waiting for human approval

## Instructions

1. Read items from Needs_Action
2. Create plans for complex tasks
3. Process items according to Company_Handbook.md rules
4. Move completed items to Done
5. Create approval requests for sensitive actions
6. When ALL items are processed, output: {self.completion_signal}

Begin working now.
"""
            
            result = subprocess.run(
                [self.claude_cmd, '--prompt', full_prompt],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout per iteration
            )
            
            if result.returncode == 0:
                print(result.stdout)
                return {
                    'success': True,
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr or f"Exit code: {result.returncode}"
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout (10 minutes exceeded)'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_summary(self, output: str) -> str:
        """Extract summary from Claude's output"""
        import re
        
        # Look for summary tags
        summary_match = re.search(r'<summary>(.*?)</summary>', output, re.DOTALL)
        if summary_match:
            return summary_match.group(1).strip()
        
        # Look for completion markers
        if 'TASK_COMPLETE' in output:
            return "Task marked as complete"
        
        # Return first 200 chars as fallback
        return output[:200]
    
    def _prepare_next_prompt(self, current_prompt: str, previous_output: str) -> str:
        """
        Prepare the next prompt based on previous output
        
        Args:
            current_prompt: Current prompt
            previous_output: Claude's previous output
            
        Returns:
            New prompt
        """
        # Get current status
        status = self.get_task_status()
        
        return f"""Continue processing. Previous iteration output:

{previous_output[:1000]}...

Current status:
- Needs Action: {status['needs_action']}
- Plans: {status['plans']}
- Done: {status['done']}

Continue working until all items are processed. Remember to output {self.completion_signal} when done.
"""
    
    def _log_iteration(self, status: str, details: str):
        """Log iteration details"""
        self.conversation_history.append({
            'iteration': self.iteration,
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'details': details[:500]
        })


def main():
    parser = argparse.ArgumentParser(
        description='Ralph Wiggum Loop - Keep Claude working until task complete',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ralph_wiggum.py "Process all files in Needs_Action"
  python ralph_wiggum.py "Generate weekly report" --max-iterations 5
  python ralph_wiggum.py "Audit all transactions" --vault AI_Employee_Vault
        """
    )
    
    parser.add_argument('prompt', type=str, help='Initial prompt for Claude')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault', 
                        help='Path to Obsidian vault')
    parser.add_argument('--max-iterations', type=int, default=10,
                        help='Maximum loop iterations')
    parser.add_argument('--completion-signal', type=str, default='TASK_COMPLETE',
                        help='String Claude outputs when done')
    
    args = parser.parse_args()
    
    try:
        loop = RalphWiggumLoop(
            vault_path=args.vault,
            max_iterations=args.max_iterations,
            completion_signal=args.completion_signal
        )
        
        loop.run(args.prompt)
        
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)


if __name__ == '__main__':
    main()

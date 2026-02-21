#!/usr/bin/env python3
"""
Scheduler - Run AI Employee tasks on a schedule

Supports:
- Windows Task Scheduler
- Linux/Unix cron
- Direct execution

Usage:
    python scheduler.py --install         # Install scheduled tasks
    python scheduler.py --run             # Run all scheduled tasks now
    python scheduler.py --run-process     # Run orchestrator process
    python scheduler.py --run-briefing    # Generate weekly briefing
    python scheduler.py --uninstall       # Remove scheduled tasks
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.absolute()
VAULT_PATH = PROJECT_ROOT / 'AI_Employee_Vault'
PYTHON = sys.executable


def run_task(name: str, command: list) -> bool:
    """Run a task and log result"""
    print(f"\n{'=' * 60}")
    print(f"  RUNNING: {name}")
    print(f"  COMMAND: {' '.join(command)}")
    print(f"{'=' * 60}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {name}")
            if result.stdout:
                print(result.stdout[:500])  # First 500 chars
            return True
        else:
            print(f"❌ FAILED: {name}")
            if result.stderr:
                print(f"Error: {result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT: {name}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {name} - {e}")
        return False


def run_orchestrator_process():
    """Run orchestrator to process Needs_Action folder"""
    return run_task(
        "Orchestrator Process",
        [PYTHON, str(PROJECT_ROOT / 'orchestrator.py'), '--process', '--vault', str(VAULT_PATH)]
    )


def run_hitl_processor():
    """Run HITL processor for approved items"""
    return run_task(
        "HITL Processor",
        [PYTHON, str(PROJECT_ROOT / 'hitl_processor.py'), '--process', '--vault', str(VAULT_PATH)]
    )


def run_briefing():
    """Generate CEO briefing"""
    return run_task(
        "CEO Briefing",
        [PYTHON, str(PROJECT_ROOT / 'orchestrator.py'), '--briefing', '--vault', str(VAULT_PATH)]
    )


def run_all_tasks():
    """Run all scheduled tasks"""
    results = []
    
    results.append(("Orchestrator", run_orchestrator_process()))
    results.append(("HITL Processor", run_hitl_processor()))
    
    # Generate briefing on Mondays
    if datetime.now().weekday() == 0:  # Monday
        results.append(("CEO Briefing", run_briefing()))
    
    # Summary
    print(f"\n{'=' * 60}")
    print("  TASK SUMMARY")
    print(f"{'=' * 60}")
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {name}")
    
    all_passed = all(success for _, success in results)
    print(f"\n  Overall: {'✅ ALL PASSED' if all_passed else '❌ SOME FAILED'}")
    
    return all_passed


def install_windows_scheduler():
    """Install tasks in Windows Task Scheduler"""
    print("\nInstalling Windows Task Scheduler tasks...")
    
    # Create PowerShell script for task installation
    ps_script = f'''
$taskName = "AI_Employee_Orchestrator"
$taskPath = "\\AI_Employee\\"

# Create task folder
$folder = $taskPath -replace '\\\\', ''
if ($folder) {{
    $existingFolder = Get-ScheduledTask -TaskPath $taskPath -ErrorAction SilentlyContinue
    if (-not $existingFolder) {{
        New-ScheduledTaskFolder -TaskPath $taskPath
    }}
}}

# Create trigger (every 5 minutes)
$trigger = New-ScheduledTaskTrigger -Once (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)

# Create action
$action = New-ScheduledTaskAction -Execute "{PYTHON}" `
    -Argument "{PROJECT_ROOT / 'orchestrator.py'} --process --vault {VAULT_PATH}" `
    -WorkingDirectory "{PROJECT_ROOT}"

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

# Register task
Register-ScheduledTask `
    -TaskName $taskName `
    -TaskPath $taskPath `
    -Trigger $trigger `
    -Action $action `
    -Settings $settings `
    -Description "AI Employee Orchestrator - Processes Needs_Action folder every 5 minutes" `
    -Force

Write-Host "Task installed: $taskName"
Write-Host "Location: Task Scheduler Library > AI_Employee"
'''
    
    ps_file = PROJECT_ROOT / 'install_windows_tasks.ps1'
    ps_file.write_text(ps_script)
    
    print(f"\nPowerShell script created: {ps_file}")
    print("\nTo install, run in PowerShell (as Administrator):")
    print(f"  powershell -ExecutionPolicy Bypass -File {ps_file}")
    
    # Also create HITL processor task
    ps_script_hitl = f'''
$taskName = "AI_Employee_HITL_Processor"
$taskPath = "\\AI_Employee\\"

# Create trigger (every 2 minutes)
$trigger = New-ScheduledTaskTrigger -Once (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 2)

# Create action
$action = New-ScheduledTaskAction -Execute "{PYTHON}" `
    -Argument "{PROJECT_ROOT / 'hitl_processor.py'} --process --vault {VAULT_PATH}" `
    -WorkingDirectory "{PROJECT_ROOT}"

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

# Register task
Register-ScheduledTask `
    -TaskName $taskName `
    -TaskPath $taskPath `
    -Trigger $trigger `
    -Action $action `
    -Settings $settings `
    -Description "AI Employee HITL Processor - Processes approved items every 2 minutes" `
    -Force

Write-Host "Task installed: $taskName"
'''
    
    ps_file_hitl = PROJECT_ROOT / 'install_windows_tasks_hitl.ps1'
    ps_file_hitl.write_text(ps_script_hitl)
    
    print(f"\nPowerShell script created: {ps_file_hitl}")
    print(f"To install, run in PowerShell (as Administrator):")
    print(f"  powershell -ExecutionPolicy Bypass -File {ps_file_hitl}")
    
    # Create weekly briefing task (Mondays at 8 AM)
    ps_script_briefing = f'''
$taskName = "AI_Employee_Weekly_Briefing"
$taskPath = "\\AI_Employee\\"

# Create trigger (Mondays at 8 AM)
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 8am

# Create action
$action = New-ScheduledTaskAction -Execute "{PYTHON}" `
    -Argument "{PROJECT_ROOT / 'orchestrator.py'} --briefing --vault {VAULT_PATH}" `
    -WorkingDirectory "{PROJECT_ROOT}"

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

# Register task
Register-ScheduledTask `
    -TaskName $taskName `
    -TaskPath $taskPath `
    -Trigger $trigger `
    -Action $action `
    -Settings $settings `
    -Description "AI Employee Weekly Briefing - Generated every Monday at 8 AM" `
    -Force

Write-Host "Task installed: $taskName"
'''
    
    ps_file_briefing = PROJECT_ROOT / 'install_windows_tasks_briefing.ps1'
    ps_file_briefing.write_text(ps_script_briefing)
    
    print(f"\nPowerShell script created: {ps_file_briefing}")
    print(f"To install, run in PowerShell (as Administrator):")
    print(f"  powershell -ExecutionPolicy Bypass -File {ps_file_briefing}")
    
    print("\n" + "=" * 60)
    print("INSTALLATION INSTRUCTIONS (Windows):")
    print("=" * 60)
    print("""
1. Open PowerShell as Administrator

2. Run each installation script:
   powershell -ExecutionPolicy Bypass -File install_windows_tasks.ps1
   powershell -ExecutionPolicy Bypass -File install_windows_tasks_hitl.ps1
   powershell -ExecutionPolicy Bypass -File install_windows_tasks_briefing.ps1

3. Verify in Task Scheduler:
   - Open Task Scheduler
   - Look for "AI_Employee" folder
   - You should see 3 tasks

4. Tasks will run automatically:
   - Orchestrator: Every 5 minutes
   - HITL Processor: Every 2 minutes
   - Weekly Briefing: Mondays at 8 AM
""")


def install_linux_cron():
    """Install tasks in Linux cron"""
    print("\nInstalling cron jobs...")
    
    cron_jobs = f'''
# AI Employee Scheduler
# Add these lines to your crontab (run: crontab -e)

# Orchestrator - Every 5 minutes
*/5 * * * * {PYTHON} {PROJECT_ROOT}/orchestrator.py --process --vault {VAULT_PATH} >> {PROJECT_ROOT}/logs/cron_orchestrator.log 2>&1

# HITL Processor - Every 2 minutes  
*/2 * * * * {PYTHON} {PROJECT_ROOT}/hitl_processor.py --process --vault {VAULT_PATH} >> {PROJECT_ROOT}/logs/cron_hitl.log 2>&1

# Weekly Briefing - Every Monday at 8 AM
0 8 * * 1 {PYTHON} {PROJECT_ROOT}/orchestrator.py --briefing --vault {VAULT_PATH} >> {PROJECT_ROOT}/logs/cron_briefing.log 2>&1
'''
    
    # Create instructions file
    instructions_file = PROJECT_ROOT / 'install_cron_jobs.txt'
    instructions_file.write_text(cron_jobs)
    
    print(f"\nCron job instructions saved to: {instructions_file}")
    print("\nTo install, run:")
    print(f"  crontab {instructions_file}")
    print("\nOr manually add these lines to your crontab:")
    print(cron_jobs)


def main():
    parser = argparse.ArgumentParser(description='AI Employee Scheduler')
    parser.add_argument('--install', action='store_true', help='Install scheduled tasks')
    parser.add_argument('--uninstall', action='store_true', help='Remove scheduled tasks')
    parser.add_argument('--run', action='store_true', help='Run all tasks now')
    parser.add_argument('--run-process', action='store_true', help='Run orchestrator process')
    parser.add_argument('--run-briefing', action='store_true', help='Generate briefing')
    parser.add_argument('--run-hitl', action='store_true', help='Run HITL processor')
    
    args = parser.parse_args()
    
    if args.install:
        if sys.platform == 'win32':
            install_windows_scheduler()
        else:
            install_linux_cron()
        return
    
    if args.uninstall:
        print("\nTo uninstall scheduled tasks:")
        if sys.platform == 'win32':
            print("1. Open Task Scheduler")
            print("2. Delete tasks in 'AI_Employee' folder")
        else:
            print("Run: crontab -r")
        return
    
    if args.run_briefing:
        run_briefing()
        return
    
    if args.run_process:
        run_orchestrator_process()
        return
    
    if args.run_hitl:
        run_hitl_processor()
        return
    
    if args.run:
        run_all_tasks()
        return
    
    # Default: Show help
    parser.print_help()
    
    print("\n\n" + "=" * 60)
    print("QUICK START:")
    print("=" * 60)
    print("""
Install scheduled tasks:
  python scheduler.py --install

Run all tasks now:
  python scheduler.py --run

Generate briefing:
  python scheduler.py --run-briefing
""")


if __name__ == '__main__':
    main()

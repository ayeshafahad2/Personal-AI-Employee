#!/usr/bin/env python3
"""
Silver Tier Verification Script

Run this to verify all Silver Tier requirements are met.
"""

import sys
from pathlib import Path

def check_mark(passed: bool) -> str:
    return "OK" if passed else "FAIL"

def main():
    print("=" * 60)
    print("  SILVER TIER VERIFICATION")
    print("=" * 60)
    
    all_passed = True
    silver_requirements = []
    
    # 1. Bronze Tier Requirements (prerequisites)
    print("\n1. BRONZE TIER (Prerequisites)")
    print("-" * 40)
    
    vault = Path("AI_Employee_Vault")
    bronze_items = [
        ("Vault folder", vault.exists()),
        ("Dashboard.md", (vault / "Dashboard.md").exists()),
        ("Company_Handbook.md", (vault / "Company_Handbook.md").exists()),
        ("Business_Goals.md", (vault / "Business_Goals.md").exists()),
        ("Needs_Action/", (vault / "Needs_Action").exists()),
        ("Plans/", (vault / "Plans").exists()),
        ("Done/", (vault / "Done").exists()),
        ("Pending_Approval/", (vault / "Pending_Approval").exists()),
    ]
    
    for name, exists in bronze_items:
        status = check_mark(exists)
        print(f"   {status}: {name}")
        if not exists:
            all_passed = False
    
    # 2. Watchers
    print("\n2. WATCHER SCRIPTS (2+ required)")
    print("-" * 40)
    
    watchers_path = Path("watchers")
    watchers = [
        ("base_watcher.py", (watchers_path / "base_watcher.py").exists()),
        ("gmail_watcher.py", (watchers_path / "gmail_watcher.py").exists()),
        ("filesystem_watcher.py", (watchers_path / "filesystem_watcher.py").exists()),
    ]
    
    watcher_count = sum(1 for _, exists in watchers if exists)
    for name, exists in watchers:
        status = check_mark(exists)
        print(f"   {status}: {name}")
        if not exists:
            all_passed = False
    
    watchers_pass = watcher_count >= 2
    silver_requirements.append(("Watchers (2+)", watchers_pass))
    print(f"   => Watchers available: {watcher_count} (need 2+)")
    
    # 3. MCP Servers
    print("\n3. MCP SERVERS")
    print("-" * 40)
    
    mcp_servers = [
        ("mcp_email_server.py", Path("mcp_email_server.py").exists()),
        ("mcp_browser_server.py", Path("mcp_browser_server.py").exists()),
        ("mcp_linkedin_server.py", Path("mcp_linkedin_server.py").exists()),
    ]
    
    mcp_count = sum(1 for _, exists in mcp_servers if exists)
    for name, exists in mcp_servers:
        status = check_mark(exists)
        print(f"   {status}: {name}")
        if not exists:
            all_passed = False
    
    silver_requirements.append(("MCP Servers", mcp_count >= 1))
    print(f"   => MCP servers available: {mcp_count}")
    
    # 4. Orchestrator with Plan.md
    print("\n4. ORCHESTRATOR (Plan.md creation)")
    print("-" * 40)
    
    orchestrator_exists = Path("orchestrator.py").exists()
    print(f"   {check_mark(orchestrator_exists)}: orchestrator.py")
    
    orchestrator_has_plan = False
    if orchestrator_exists:
        content = Path("orchestrator.py").read_text(encoding='utf-8')
        orchestrator_has_plan = "_create_plan_for_action" in content
        print(f"   {check_mark(orchestrator_has_plan)}: Plan.md creation method")
    
    silver_requirements.append(("Orchestrator + Plans", orchestrator_has_plan))
    
    if not orchestrator_exists:
        all_passed = False
    
    # 5. HITL Approval Workflow
    print("\n5. HITL APPROVAL WORKFLOW")
    print("-" * 40)
    
    hitl_items = [
        ("hitl_processor.py", Path("hitl_processor.py").exists()),
        ("Pending_Approval/", (vault / "Pending_Approval").exists()),
        ("Approved/", (vault / "Approved").exists()),
        ("Rejected/", (vault / "Rejected").exists()),
    ]
    
    for name, exists in hitl_items:
        status = check_mark(exists)
        print(f"   {status}: {name}")
        if not exists:
            all_passed = False
    
    silver_requirements.append(("HITL Workflow", all(x[1] for x in hitl_items)))
    
    # 6. Scheduler
    print("\n6. SCHEDULER (cron/Task Scheduler)")
    print("-" * 40)
    
    scheduler_exists = Path("scheduler.py").exists()
    print(f"   {check_mark(scheduler_exists)}: scheduler.py")
    
    scheduler_has_install = False
    if scheduler_exists:
        content = Path("scheduler.py").read_text(encoding='utf-8')
        scheduler_has_install = "install_windows_scheduler" in content or "install_linux_cron" in content
        print(f"   {check_mark(scheduler_has_install)}: Installation support")
    
    silver_requirements.append(("Scheduler", scheduler_has_install))
    
    if not scheduler_exists:
        all_passed = False
    
    # 7. LinkedIn Integration
    print("\n7. LINKEDIN AUTO-POSTING")
    print("-" * 40)
    
    linkedin_items = [
        ("linkedin_auto_publisher.py", Path("linkedin_auto_publisher.py").exists()),
        ("auto_post_manager.py", Path("auto_post_manager.py").exists()),
        ("whatsapp_notifier.py", Path("whatsapp_notifier.py").exists()),
    ]
    
    for name, exists in linkedin_items:
        status = check_mark(exists)
        print(f"   {status}: {name}")
        if not exists:
            all_passed = False
    
    silver_requirements.append(("LinkedIn Integration", all(x[1] for x in linkedin_items)))
    
    # 8. Agent Skills
    print("\n8. AGENT SKILLS")
    print("-" * 40)
    
    agent_skills_exists = Path("agent_skills.py").exists()
    print(f"   {check_mark(agent_skills_exists)}: agent_skills.py")
    
    silver_requirements.append(("Agent Skills", agent_skills_exists))
    
    if not agent_skills_exists:
        all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    print("  SILVER TIER REQUIREMENTS SUMMARY")
    print("=" * 60)
    
    for name, passed in silver_requirements:
        status = "PASS" if passed else "FAIL"
        print(f"  {status}: {name}")
    
    all_silver_passed = all(passed for _, passed in silver_requirements)
    
    print("\n" + "=" * 60)
    if all_silver_passed and all_passed:
        print("  SILVER TIER COMPLETE - All requirements met!")
    else:
        print("  SOME REQUIREMENTS NOT MET - Review output above")
    print("=" * 60)
    
    print("\nNext Steps:")
    print("1. Configure .env with your credentials")
    print("2. Run: python watchers/gmail_watcher.py --auth")
    print("3. Configure MCP servers in Claude Code settings")
    print("4. Install scheduler: python scheduler.py --install")
    print("5. Test: python scheduler.py --run")
    
    return 0 if all_silver_passed else 1

if __name__ == '__main__':
    sys.exit(main())

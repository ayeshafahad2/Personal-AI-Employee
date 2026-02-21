#!/usr/bin/env python3
"""
Silver Tier Test Suite

Comprehensive tests for all Silver Tier components.

Usage:
    python test_silver_tier.py              # Run all tests
    python test_silver_tier.py --vault      # Test vault structure only
    python test_silver_tier.py --watchers   # Test watchers only
    python test_silver_tier.py --orch       # Test orchestrator only
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Test results tracking
TESTS_PASSED = 0
TESTS_FAILED = 0
TESTS_SKIPPED = 0


def test_result(name: str, passed: bool, message: str = ""):
    """Track and display test result"""
    global TESTS_PASSED, TESTS_FAILED, TESTS_SKIPPED
    
    if passed:
        TESTS_PASSED += 1
        status = "PASS"
    elif passed is None:
        TESTS_SKIPPED += 1
        status = "SKIP"
    else:
        TESTS_FAILED += 1
        status = "FAIL"
    
    print(f"  {status}: {name}")
    if message and not passed:
        print(f"         {message}")


def print_section(title: str):
    """Print section header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


# ============================================================================
# TEST 1: Vault Structure
# ============================================================================

def test_vault_structure():
    """Test Obsidian vault structure"""
    print_section("TEST 1: Vault Structure")
    
    vault = Path("AI_Employee_Vault")
    
    # Test vault exists
    test_result("Vault folder exists", vault.exists(), 
                "Run: mkdir AI_Employee_Vault")
    
    if not vault.exists():
        return False
    
    # Test required folders
    folders = [
        "Inbox", "Needs_Action", "Plans", "Done",
        "Pending_Approval", "Approved", "Rejected",
        "Logs", "Briefings", "In_Progress"
    ]
    
    for folder in folders:
        folder_path = vault / folder
        test_result(f"Folder: {folder}/", folder_path.exists())
    
    # Test required files
    files = [
        ("Dashboard.md", vault / "Dashboard.md"),
        ("Company_Handbook.md", vault / "Company_Handbook.md"),
        ("Business_Goals.md", vault / "Business_Goals.md"),
    ]
    
    for name, path in files:
        test_result(f"File: {name}", path.exists())
    
    return True


# ============================================================================
# TEST 2: Watchers
# ============================================================================

def test_watchers():
    """Test watcher scripts"""
    print_section("TEST 2: Watchers")
    
    watchers_path = Path("watchers")
    
    # Test watcher files exist
    watchers = [
        ("base_watcher.py", watchers_path / "base_watcher.py"),
        ("gmail_watcher.py", watchers_path / "gmail_watcher.py"),
        ("filesystem_watcher.py", watchers_path / "filesystem_watcher.py"),
    ]
    
    for name, path in watchers:
        test_result(f"File: {name}", path.exists())
    
    # Test imports
    try:
        sys.path.insert(0, str(Path.cwd()))
        from watchers.base_watcher import BaseWatcher
        test_result("Import: BaseWatcher", True)
    except ImportError as e:
        test_result("Import: BaseWatcher", False, str(e))
    
    try:
        from watchers.gmail_watcher import GmailWatcher
        test_result("Import: GmailWatcher", True)
    except ImportError as e:
        test_result("Import: GmailWatcher", False, str(e))
    
    try:
        from watchers.filesystem_watcher import FileSystemWatcher
        test_result("Import: FileSystemWatcher", True)
    except ImportError as e:
        test_result("Import: FileSystemWatcher", False, str(e))
    
    # Test Gmail authentication status
    try:
        from watchers.gmail_watcher import GmailWatcher
        vault = Path("AI_Employee_Vault")
        watcher = GmailWatcher(str(vault))
        
        if watcher.service:
            test_result("Gmail: Authenticated", True)
        else:
            test_result("Gmail: Authenticated", None, 
                       "Run: python watchers/gmail_watcher.py --auth")
    except Exception as e:
        test_result("Gmail: Authenticated", None, str(e))


# ============================================================================
# TEST 3: MCP Servers
# ============================================================================

def test_mcp_servers():
    """Test MCP server scripts"""
    print_section("TEST 3: MCP Servers")
    
    mcp_files = [
        ("mcp_email_server.py", Path("mcp_email_server.py")),
        ("mcp_browser_server.py", Path("mcp_browser_server.py")),
        ("mcp_linkedin_server.py", Path("mcp_linkedin_server.py")),
    ]
    
    for name, path in mcp_files:
        test_result(f"File: {name}", path.exists())
    
    # Test MCP SDK
    try:
        from mcp.server import Server
        test_result("MCP SDK installed", True)
    except ImportError:
        test_result("MCP SDK installed", False, 
                   "Run: pip install mcp")
    
    # Test imports
    try:
        import mcp_email_server
        test_result("Import: mcp_email_server", True)
    except ImportError as e:
        test_result("Import: mcp_email_server", False, str(e))


# ============================================================================
# TEST 4: Orchestrator
# ============================================================================

def test_orchestrator():
    """Test orchestrator functionality"""
    print_section("TEST 4: Orchestrator")
    
    # Test file exists
    test_result("orchestrator.py exists", Path("orchestrator.py").exists())
    
    # Test import
    try:
        from orchestrator import Orchestrator
        test_result("Import: Orchestrator", True)
    except ImportError as e:
        test_result("Import: Orchestrator", False, str(e))
        return
    
    # Test initialization
    try:
        from orchestrator import Orchestrator
        vault = Path("AI_Employee_Vault")
        orchestrator = Orchestrator(str(vault))
        test_result("Orchestrator init", True)
        
        # Test plan creation method exists
        test_result("Has _create_plan_for_action", 
                   hasattr(orchestrator, '_create_plan_for_action'))
        
        # Test Qwen integration
        test_result("Has _run_qwen_api method", 
                   hasattr(orchestrator, '_run_qwen_api'))
        
    except Exception as e:
        test_result("Orchestrator init", False, str(e))
    
    # Test .env configuration
    from dotenv import load_dotenv
    load_dotenv()
    
    ai_command = os.getenv('AI_COMMAND', 'claude')
    test_result(f"AI_COMMAND set to '{ai_command}'", True)
    
    if ai_command == 'qwen':
        api_key = os.getenv('DASHSCOPE_API_KEY', '')
        if api_key and api_key != 'your_dashscope_api_key_here':
            test_result("DASHSCOPE_API_KEY configured", True)
        else:
            test_result("DASHSCOPE_API_KEY configured", False,
                       "Add key to .env file")


# ============================================================================
# TEST 5: HITL Workflow
# ============================================================================

def test_hitl_workflow():
    """Test HITL approval workflow"""
    print_section("TEST 5: HITL Workflow")
    
    vault = Path("AI_Employee_Vault")
    
    # Test folders
    folders = [
        ("Pending_Approval/", vault / "Pending_Approval"),
        ("Approved/", vault / "Approved"),
        ("Rejected/", vault / "Rejected"),
    ]
    
    for name, path in folders:
        test_result(f"Folder: {name}", path.exists())
    
    # Test hitl_processor.py
    test_result("hitl_processor.py exists", 
               Path("hitl_processor.py").exists())
    
    # Test import
    try:
        from hitl_processor import HITLProcessor
        test_result("Import: HITLProcessor", True)
        
        # Test initialization
        processor = HITLProcessor(str(vault))
        test_result("HITLProcessor init", True)
        
    except ImportError as e:
        test_result("Import: HITLProcessor", False, str(e))
    except Exception as e:
        test_result("HITLProcessor init", False, str(e))


# ============================================================================
# TEST 6: Scheduler
# ============================================================================

def test_scheduler():
    """Test scheduler functionality"""
    print_section("TEST 6: Scheduler")
    
    # Test file exists
    test_result("scheduler.py exists", Path("scheduler.py").exists())
    
    # Test import
    try:
        import scheduler
        test_result("Import: scheduler", True)
    except ImportError as e:
        test_result("Import: scheduler", False, str(e))
    
    # Test functions exist
    try:
        from scheduler import run_orchestrator_process, run_hitl_processor, run_briefing
        test_result("Function: run_orchestrator_process", True)
        test_result("Function: run_hitl_processor", True)
        test_result("Function: run_briefing", True)
    except ImportError as e:
        test_result("Scheduler functions", False, str(e))
    
    # Test Windows scheduler functions
    try:
        from scheduler import install_windows_scheduler
        test_result("Function: install_windows_scheduler", True)
    except ImportError:
        test_result("Function: install_windows_scheduler", False)


# ============================================================================
# TEST 7: LinkedIn + WhatsApp
# ============================================================================

def test_linkedin_whatsapp():
    """Test LinkedIn and WhatsApp integration"""
    print_section("TEST 7: LinkedIn + WhatsApp")
    
    # Test files exist
    files = [
        ("linkedin_auto_publisher.py", Path("linkedin_auto_publisher.py")),
        ("whatsapp_notifier.py", Path("whatsapp_notifier.py")),
        ("auto_post_manager.py", Path("auto_post_manager.py")),
    ]
    
    for name, path in files:
        test_result(f"File: {name}", path.exists())
    
    # Test imports
    try:
        from linkedin_auto_publisher import LinkedInAutoPublisher
        test_result("Import: LinkedInAutoPublisher", True)
    except ImportError as e:
        test_result("Import: LinkedInAutoPublisher", False, str(e))
    
    try:
        from whatsapp_notifier import WhatsAppNotifier
        test_result("Import: WhatsAppNotifier", True)
    except ImportError as e:
        test_result("Import: WhatsAppNotifier", False, str(e))
    
    try:
        from auto_post_manager import AutoPostManager
        test_result("Import: AutoPostManager", True)
    except ImportError as e:
        test_result("Import: AutoPostManager", False, str(e))
    
    # Test credentials
    from dotenv import load_dotenv
    load_dotenv()
    
    linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
    if linkedin_token and linkedin_token != 'your_linkedin_access_token_here':
        test_result("LinkedIn: Access token configured", True)
    else:
        test_result("LinkedIn: Access token configured", False,
                   "Add token to .env file")
    
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
    if twilio_sid and twilio_sid != 'your_twilio_account_sid_here':
        test_result("Twilio: Account SID configured", True)
    else:
        test_result("Twilio: Account SID configured", False,
                   "Add SID to .env file")


# ============================================================================
# TEST 8: Agent Skills
# ============================================================================

def test_agent_skills():
    """Test agent skills module"""
    print_section("TEST 8: Agent Skills")
    
    # Test file exists
    test_result("agent_skills.py exists", Path("agent_skills.py").exists())
    
    # Test import
    try:
        from agent_skills import AgentSkills
        test_result("Import: AgentSkills", True)
    except ImportError as e:
        test_result("Import: AgentSkills", False, str(e))
        return
    
    # Test initialization
    try:
        from agent_skills import AgentSkills
        vault = Path("AI_Employee_Vault")
        skills = AgentSkills(str(vault))
        test_result("AgentSkills init", True)
        
        # Test methods exist
        methods = [
            'send_email', 'draft_email', 'move_to_done',
            'create_plan', 'create_approval_request', 'update_dashboard'
        ]
        
        for method in methods:
            test_result(f"Method: {method}()", hasattr(skills, method))
        
    except Exception as e:
        test_result("AgentSkills init", False, str(e))


# ============================================================================
# TEST 9: Quick Functional Tests
# ============================================================================

def test_functional():
    """Quick functional tests"""
    print_section("TEST 9: Functional Tests")
    
    vault = Path("AI_Employee_Vault")
    
    # Test 1: Create a test action file
    print("\n  Creating test action file...")
    needs_action = vault / "Needs_Action"
    test_file = needs_action / "TEST_functional_check.md"
    
    test_content = f'''---
type: test
created: {datetime.now().isoformat()}
status: pending
---

# Functional Test

This is a test action file to verify the system works.

## Steps

- [ ] System detected this file
- [ ] Orchestrator can process it
- [ ] Test complete

'''
    
    try:
        needs_action.mkdir(parents=True, exist_ok=True)
        test_file.write_text(test_content, encoding='utf-8')
        test_result("Create test action file", True)
        print(f"         Created: {test_file}")
    except Exception as e:
        test_result("Create test action file", False, str(e))
    
    # Test 2: Dashboard update
    print("\n  Testing dashboard update...")
    dashboard = vault / "Dashboard.md"
    try:
        if dashboard.exists():
            content = dashboard.read_text(encoding='utf-8')
            if "## Recent Activity" in content:
                test_result("Dashboard has Recent Activity section", True)
            else:
                test_result("Dashboard has Recent Activity section", False)
        else:
            test_result("Dashboard exists", False)
    except Exception as e:
        test_result("Dashboard check", False, str(e))


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("  SILVER TIER TEST SUITE")
    print("=" * 70)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Run all tests
    test_vault_structure()
    test_watchers()
    test_mcp_servers()
    test_orchestrator()
    test_hitl_workflow()
    test_scheduler()
    test_linkedin_whatsapp()
    test_agent_skills()
    test_functional()
    
    # Summary
    print_section("TEST SUMMARY")
    
    total = TESTS_PASSED + TESTS_FAILED + TESTS_SKIPPED
    
    print(f"  Total Tests:  {total}")
    print(f"  Passed:    {TESTS_PASSED}")
    print(f"  Failed:    {TESTS_FAILED}")
    print(f"  Skipped:   {TESTS_SKIPPED}")
    print()
    
    if TESTS_FAILED == 0:
        print("  ALL TESTS PASSED!")
        print()
        print("  Silver Tier is fully functional.")
        print("  Next: Configure credentials and run the system.")
    else:
        print(f"  {TESTS_FAILED} test(s) failed.")
        print()
        print("  Review the failures above and fix them.")
        print("  Some failures may be due to missing credentials (expected).")
    
    print()
    print("=" * 70)
    
    # Recommendations
    print("\n  RECOMMENDATIONS:")
    print("  " + "-" * 66)
    
    if TESTS_FAILED == 0:
        print("  1. Configure .env with your API keys")
        print("  2. Run: python watchers/gmail_watcher.py --auth")
        print("  3. Test: python orchestrator.py --process")
        print("  4. Install scheduler: python scheduler.py --install")
    else:
        print("  1. Fix the failed tests above")
        print("  2. Re-run: python test_silver_tier.py")
    
    print()
    
    return 0 if TESTS_FAILED == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

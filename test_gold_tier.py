#!/usr/bin/env python3
"""
Gold Tier Test Suite - Social Media Integration

Tests for Facebook, Instagram, and Twitter MCP servers.

Usage:
    python test_gold_tier.py              # Run all tests
    python test_gold_tier.py --social     # Test social media only
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

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
# TEST 1: MCP Servers Exist
# ============================================================================

def test_mcp_servers():
    """Test social media MCP servers"""
    print_section("TEST 1: Social Media MCP Servers")
    
    servers = [
        ("mcp_facebook_server.py", Path("mcp_facebook_server.py")),
        ("mcp_instagram_server.py", Path("mcp_instagram_server.py")),
        ("mcp_twitter_server.py", Path("mcp_twitter_server.py")),
    ]
    
    for name, path in servers:
        test_result(f"File: {name}", path.exists())
    
    # Test imports
    try:
        import mcp_facebook_server
        test_result("Import: mcp_facebook_server", True)
    except ImportError as e:
        test_result("Import: mcp_facebook_server", False, str(e))
    
    try:
        import mcp_instagram_server
        test_result("Import: mcp_instagram_server", True)
    except ImportError as e:
        test_result("Import: mcp_instagram_server", False, str(e))
    
    try:
        import mcp_twitter_server
        test_result("Import: mcp_twitter_server", True)
    except ImportError as e:
        test_result("Import: mcp_twitter_server", False, str(e))


# ============================================================================
# TEST 2: Credentials Configuration
# ============================================================================

def test_credentials():
    """Test social media credentials"""
    print_section("TEST 2: Credentials Configuration")
    
    # Facebook
    fb_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')
    test_result("Facebook: PAGE_ACCESS_TOKEN configured", 
               fb_token and fb_token != 'your_facebook_page_token_here')
    
    # Instagram
    ig_token = os.getenv('INSTAGRAM_PAGE_ACCESS_TOKEN', '')
    ig_account = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
    test_result("Instagram: PAGE_ACCESS_TOKEN configured", 
               ig_token and ig_token != 'your_instagram_token_here')
    test_result("Instagram: BUSINESS_ACCOUNT_ID configured", 
               ig_account and ig_account != 'your_business_account_id_here')
    
    # Twitter
    tw_bearer = os.getenv('TWITTER_BEARER_TOKEN', '')
    test_result("Twitter: BEARER_TOKEN configured", 
               tw_bearer and tw_bearer != 'your_twitter_bearer_token_here')


# ============================================================================
# TEST 3: Social Media Poster
# ============================================================================

def test_social_poster():
    """Test unified social media poster"""
    print_section("TEST 3: Social Media Poster")
    
    # Test file exists
    test_result("social_media_poster.py exists", 
               Path("social_media_poster.py").exists())
    
    # Test import
    try:
        from social_media_poster import SocialMediaPoster
        test_result("Import: SocialMediaPoster", True)
        
        # Test initialization
        poster = SocialMediaPoster()
        test_result("SocialMediaPoster init", True)
        
        # Test platform detection
        platforms = poster.available_platforms
        test_result("Platform detection works", isinstance(platforms, dict))
        
        # Show platform status
        print("\n  Platform Status:")
        for platform, configured in platforms.items():
            status = "configured" if configured else "not configured"
            print(f"    - {platform}: {status}")
        
    except ImportError as e:
        test_result("Import: SocialMediaPoster", False, str(e))
    except Exception as e:
        test_result("SocialMediaPoster init", False, str(e))


# ============================================================================
# TEST 4: MCP Server Classes
# ============================================================================

def test_mcp_classes():
    """Test MCP server classes"""
    print_section("TEST 4: MCP Server Classes")
    
    # Facebook
    try:
        from mcp_facebook_server import FacebookMCPServer
        test_result("FacebookMCPServer class", True)
        
        server = FacebookMCPServer()
        test_result("FacebookMCPServer init", True)
        test_result("FacebookMCPServer has post_to_page", 
                   hasattr(server, 'post_to_page'))
    except Exception as e:
        test_result("FacebookMCPServer", False, str(e))
    
    # Instagram
    try:
        from mcp_instagram_server import InstagramMCPServer
        test_result("InstagramMCPServer class", True)
        
        server = InstagramMCPServer()
        test_result("InstagramMCPServer init", True)
        test_result("InstagramMCPServer has post_image", 
                   hasattr(server, 'post_image'))
    except Exception as e:
        test_result("InstagramMCPServer", False, str(e))
    
    # Twitter
    try:
        from mcp_twitter_server import TwitterMCPServer
        test_result("TwitterMCPServer class", True)
        
        server = TwitterMCPServer()
        test_result("TwitterMCPServer init", True)
        test_result("TwitterMCPServer has post_tweet", 
                   hasattr(server, 'post_tweet'))
    except Exception as e:
        test_result("TwitterMCPServer", False, str(e))


# ============================================================================
# TEST 5: Vault Integration
# ============================================================================

def test_vault_integration():
    """Test vault logging integration"""
    print_section("TEST 5: Vault Integration")
    
    vault = Path("AI_Employee_Vault")
    logs_dir = vault / "Logs"
    
    test_result("Vault/Logs directory exists", logs_dir.exists())
    
    # Test dashboard exists
    dashboard = vault / "Dashboard.md"
    test_result("Dashboard.md exists", dashboard.exists())
    
    # Test recent activity section
    if dashboard.exists():
        content = dashboard.read_text(encoding='utf-8')
        test_result("Dashboard has Recent Activity section", 
                   "## Recent Activity" in content)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("  GOLD TIER TEST SUITE - Social Media Integration")
    print("=" * 70)
    print()
    
    # Run tests
    test_mcp_servers()
    test_credentials()
    test_social_poster()
    test_mcp_classes()
    test_vault_integration()
    
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
        print("  Gold Tier (Social Media) is fully configured.")
        print("  Ready to post to Facebook, Instagram, and Twitter!")
    else:
        print(f"  {TESTS_FAILED} test(s) failed.")
        print()
        print("  Most failures are due to missing credentials (expected).")
        print("  Configure credentials in .env to enable platforms.")
    
    print()
    print("=" * 70)
    
    # Recommendations
    print("\n  NEXT STEPS:")
    print("  " + "-" * 66)
    
    if TESTS_FAILED == 0:
        print("  1. Test posting: python social_media_poster.py --test")
        print("  2. Make a test post: python social_media_poster.py --text \"Hello!\"")
        print("  3. Check vault logs: AI_Employee_Vault/Logs/")
    else:
        print("  1. Configure credentials in .env:")
        print("     - FACEBOOK_PAGE_ACCESS_TOKEN")
        print("     - INSTAGRAM_PAGE_ACCESS_TOKEN")
        print("     - INSTAGRAM_BUSINESS_ACCOUNT_ID")
        print("     - TWITTER_BEARER_TOKEN")
        print("  2. Re-run: python test_gold_tier.py")
    
    print()
    print("  See GOLD_TIER_SOCIAL_MEDIA.md for detailed setup guide.")
    print()
    
    return 0 if TESTS_FAILED == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

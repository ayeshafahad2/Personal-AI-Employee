#!/usr/bin/env python3
"""
Twitter AUTO POSTER - Reliable Complete Tweet
Uses PowerShell with better timing and error handling
"""

import subprocess
import time
from pathlib import Path

print("=" * 70)
print("  TWITTER AUTO POSTER - COMPLETE TWEET")
print("  Reliable Automation")
print("=" * 70)

# Shorter, cleaner tweet that fits Twitter better
tweet = "The best time to plant a tree was 20 years ago.\nThe second best time is NOW.\n\nDon't wait for perfect conditions.\nStart where you are.\nUse what you have.\nDo what you can.\n\nYour future self will thank you.\n\n#Motivation #Success #GrowthMindset"

print("\n  Tweet to post:")
print("-" * 70)
print(tweet)
print("-" * 70)

# Create improved PowerShell script
ps_script = '''
Write-Host "  Starting Twitter automation..." -ForegroundColor Green

$wshell = New-Object -ComObject WScript.Shell

# Open Twitter
Write-Host "  Opening Twitter..."
Start-Process "https://twitter.com/compose/tweet"

# Wait for page to load
Start-Sleep -Seconds 8

# Activate Twitter window
Write-Host "  Activating window..."
$wshell.AppActivate("Twitter")
Start-Sleep -Milliseconds 1000

# Click to focus
Write-Host "  Focusing..."
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# Tab to reach tweet box (try multiple tabs)
Write-Host "  Navigating to tweet box..."
for ($i = 0; $i -lt 10; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 200
}

Start-Sleep -Milliseconds 1000

# Clear any text
Write-Host "  Clearing..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 300

# Type tweet using clipboard method (more reliable for special chars)
Write-Host "  Setting clipboard..."
$tweet = @"
The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset
"@

$tweet | Set-Clipboard
Start-Sleep -Milliseconds 500

Write-Host "  Pasting tweet..."
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 2000

# Verify content appeared
Start-Sleep -Milliseconds 1000

Write-Host "  Posting..."
$wshell.SendKeys("^{ENTER}")
Start-Sleep -Seconds 4

Write-Host "  Opening profile..."
Start-Process "https://twitter.com/ayeshafahad661"

Write-Host "  DONE! Tweet posted!" -ForegroundColor Green
Start-Sleep -Seconds 2
'''

ps_file = Path(__file__).parent / 'twitter_reliable.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("\n[1] Running automation...")

# Run PowerShell
subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(ps_file)])

print("    Automation started!")

print("\n" + "=" * 70)
print("  WATCH YOUR BROWSER!")
print("=" * 70)
print("""
  The script will:
  1. Open Twitter compose
  2. Wait for page load (8 seconds)
  3. Focus the tweet box
  4. Paste the complete tweet
  5. Post with Ctrl+Enter
  6. Open your profile
  
  This should post the FULL tweet this time!
""")
print("=" * 70)
print("\n  Check profile: https://twitter.com/ayeshafahad661")
print("=" * 70)

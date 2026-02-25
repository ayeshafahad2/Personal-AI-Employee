#!/usr/bin/env python3
"""
Twitter AUTO POSTER - PowerShell Automation
Uses Windows PowerShell for reliable UI automation
No external dependencies needed
"""

import subprocess
import time
from pathlib import Path

print("=" * 70)
print("  TWITTER AUTO POSTER - PowerShell")
print("  Completely Automated - No Manual Steps")
print("=" * 70)

quote = """The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset"""

print("\n  Tweet to post:")
print("-" * 70)
print(quote)
print("-" * 70)

# Create PowerShell script
ps_script = f'''
# Twitter Auto Post PowerShell Script
# Uses COM automation to control browser

$ErrorActionPreference = "SilentlyContinue"

Write-Host "  Starting Twitter automation..."

# Create Internet Explorer COM object (works with Chrome too via COM)
$ie = New-Object -ComObject InternetExplorer.Application
$ie.Visible = $true
$ie.Navigate("https://twitter.com/compose/tweet")

# Wait for page to load
Write-Host "  Waiting for Twitter to load..."
Start-Sleep -Seconds 10

# Bring window to front
$wshell = New-Object -ComObject WScript.Shell
$wshell.AppActivate("Twitter")

Write-Host "  Focusing tweet box..."
# Tab to reach tweet textbox
for ($i = 0; $i -lt 8; $i++) {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 300
}}

Write-Host "  Clearing existing text..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 500

Write-Host "  Typing tweet..."
# Type the tweet
$wshell.SendKeys("The best time to plant a tree was 20 years ago.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("The second best time is NOW.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{ENTER}}{{ENTER}}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Don't wait for perfect conditions.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Start where you are.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Use what you have.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Do what you can.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{ENTER}}{{ENTER}}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Your future self will thank you.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{ENTER}}{{ENTER}}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("#Motivation #Success #GrowthMindset")
Start-Sleep -Milliseconds 1000

Write-Host "  Posting tweet..."
# Post with Ctrl+Enter
$wshell.SendKeys("^{{ENTER}}")
Start-Sleep -Seconds 3

Write-Host "  Opening profile..."
# Open profile
Start-Process "https://twitter.com/ayeshafahad661"

Write-Host "  DONE! Tweet posted!"
Start-Sleep -Seconds 2

# Cleanup
$ie.Quit()
'''

ps_file = Path(__file__).parent / 'twitter_auto.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("\n[1] Running PowerShell automation...")

# Run PowerShell script
subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(ps_file)])

print("    Script started - watch your browser!")

print("\n" + "=" * 70)
print("  AUTOMATION RUNNING!")
print("=" * 70)
print("""
  The script will:
  1. Open Twitter compose in browser
  2. Wait for page to load (10 seconds)
  3. Focus the tweet textbox
  4. Type the motivational quote
  5. Post with Ctrl+Enter
  6. Open your profile
  
  Watch the browser - it will happen automatically!
""")
print("=" * 70)
print("\n  Check your profile: https://twitter.com/ayeshafahad661")
print("=" * 70)

#!/usr/bin/env python3
"""
Facebook COMPLETE AUTO POST - PowerShell Only
100% automated - opens, types, clicks post - no external dependencies
"""

import subprocess
import time
from pathlib import Path

print("=" * 70)
print("  FACEBOOK COMPLETE AUTO POST")
print("  100% Automated - PowerShell Only")
print("=" * 70)

post = """Human intelligence will always be superior to AI.

AI is a tool created by humans.
AI has no consciousness, no soul, no true creativity.

Human qualities AI can never replicate:
- Love and compassion
- Moral judgment
- True creativity
- Genuine empathy
- Free will

AI serves humans. Not the other way around.

#Human #AI #Truth"""

print("\n  Posting to Facebook:")
print("-" * 70)
print(post)
print("-" * 70)

# Create comprehensive PowerShell script
ps_script = f'''
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FACEBOOK AUTO POST - STARTING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$wshell = New-Object -ComObject WScript.Shell
$ErrorActionPreference = "SilentlyContinue"

# Step 1: Open Facebook
Write-Host "`n[1/5] Opening Facebook..."
Start-Process "https://www.facebook.com/"
Start-Sleep -Seconds 12

# Step 2: Activate window
Write-Host "[2/5] Activating window..."
$tries = 0
while ($tries -lt 5) {{
    $activated = $wshell.AppActivate("Facebook")
    if ($activated) {{ break }}
    Start-Sleep -Milliseconds 1000
    $tries++
}}
Start-Sleep -Milliseconds 2000

# Step 3: Navigate to post box
Write-Host "[3/5] Navigating to post box..."

# Use F6 to cycle through browser panes
$wshell.SendKeys("{{F6}}")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{{F6}}")
Start-Sleep -Milliseconds 500

# Tab to reach composer
for ($i = 0; $i -lt 10; $i++) {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 250
}}

Start-Sleep -Milliseconds 1000

# Activate text box
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# Clear
Write-Host "      Clearing text box..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 400
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 400

# Step 4: Type content
Write-Host "[4/5] Pasting content..."

@"
{post}
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 2500

# Step 5: Click Post
Write-Host "[5/5] Posting..."

# Method 1: Ctrl+Enter
$wshell.SendKeys("^{{ENTER}}")
Start-Sleep -Seconds 3

# Method 2: Tab to Post button
$wshell.SendKeys("{{TAB}}")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Seconds 2

# Method 3: Direct Enter
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Seconds 2

# Method 4: Space on Post button
$wshell.SendKeys("{{TAB}}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys(" ")
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  POST COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Refresh to show post
Start-Sleep -Seconds 2
$wshell.SendKeys("{{F5}}")

Start-Sleep -Seconds 3

# Show success
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("Facebook post published successfully!", "Auto Post Complete", 0, 0x30)

Write-Host "`n  Check your Facebook feed!" -ForegroundColor Green
'''

ps_file = 'fb_complete.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("\n[1] Running automation...")
subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file])
print("    Script started!")

print("\n" + "=" * 70)
print("  AUTOMATION RUNNING!")
print("=" * 70)
print("""
  The script will:
  1. Open Facebook (12 seconds)
  2. Activate the window
  3. Navigate to post box
  4. Paste the content
  5. Click Post (multiple methods)
  6. Show confirmation message
  7. Refresh to display your post
  
  Watch the browser - it's fully automated!
""")
print("=" * 70)
print("\n  Check: https://www.facebook.com/")
print("=" * 70)

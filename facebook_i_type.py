#!/usr/bin/env python3
"""
Facebook AUTO TYPE - Types everything automatically
User just clicks Post button at the end
No clipboard - types character by character
"""

import subprocess
import time
from pathlib import Path

print("=" * 70)
print("  FACEBOOK AUTO TYPE - I Type, You Click Post")
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

print("\n  I will type this post automatically:")
print("-" * 70)
print(post)
print("-" * 70)

# Create PowerShell script that types everything
ps_script = f'''
Write-Host "Opening Facebook..." -ForegroundColor Cyan
$wshell = New-Object -ComObject WScript.Shell

Start-Process "https://www.facebook.com/"
Start-Sleep -Seconds 10

Write-Host "Focusing window..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

Write-Host "Navigating to post box..."
# Tab to reach composer
for ($i = 0; $i -lt 8; $i++) {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 300
}}

Start-Sleep -Milliseconds 1000

Write-Host "Activating text box..."
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

Write-Host "Clearing any existing text..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 300

Write-Host "TYPING THE POST..." -ForegroundColor Yellow

# Type line by line
$wshell.SendKeys("Human intelligence will always be superior to AI.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200

$wshell.SendKeys("AI is a tool created by humans.")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("AI has no consciousness, no soul, no true creativity.")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200

$wshell.SendKeys("Human qualities AI can never replicate:")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200

$wshell.SendKeys("- Love and compassion")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("- Moral judgment")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("- True creativity")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("- Genuine empathy")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("- Free will")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200

$wshell.SendKeys("AI serves humans. Not the other way around.")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 200

$wshell.SendKeys("#Human #AI #Truth")

Start-Sleep -Milliseconds 1500

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  POST TYPED! CLICK THE POST BUTTON!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Show notification
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("I have typed the post!`n`nJust click the blue 'Post' button to publish!", "Ready to Post")
'''

ps_file = 'fb_auto_type.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("\n[1] Opening Facebook and typing post...")
subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file])

print("    Watch the browser - I'm typing!")

print("\n" + "=" * 70)
print("  WATCH YOUR BROWSER!")
print("=" * 70)
print("""
  The script will:
  1. Open Facebook
  2. Navigate to post box
  3. TYPE the entire post character by character
  4. Show a message when done
  
  YOUR JOB:
  When you see the message box, just click the blue "Post" button!
  
  That's it - I type, you click Post!
""")
print("=" * 70)

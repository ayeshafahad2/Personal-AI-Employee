#!/usr/bin/env python3
"""
Facebook AUTO POST - Direct and Fast
Completely automated - no user interaction needed
"""

import subprocess
import time
from pathlib import Path

print("=" * 70)
print("  FACEBOOK AUTO POST - Direct")
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

# Create simple, direct PowerShell script
ps_script = f'''
$wshell = New-Object -ComObject WScript.Shell

Write-Host "Opening Facebook..."
Start-Process "https://www.facebook.com/"
Start-Sleep -Seconds 10

Write-Host "Focusing..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

Write-Host "Navigating to post box..."
# Tab to reach the composer
1..10 | ForEach-Object {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 200
}}

Start-Sleep -Milliseconds 1000

Write-Host "Clearing..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 300

Write-Host "Pasting content..."
@"
{post}
"@ | Set-Clipboard
Start-Sleep -Milliseconds 300
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 2000

Write-Host "Posting..."
# Try Ctrl+Enter first
$wshell.SendKeys("^{{ENTER}}")
Start-Sleep -Seconds 3

# Then Enter as backup
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Seconds 2

Write-Host "DONE!"
Start-Sleep -Seconds 2

# Refresh to show post
$wshell.SendKeys("{{F5}}")
'''

ps_file = 'fb_post.ps1'
with open(ps_file, 'w') as f:
    f.write(ps_script)

print("\n  Running automation...")
subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file])

print("  Check Facebook in 15 seconds!")
print("\n  https://www.facebook.com/")

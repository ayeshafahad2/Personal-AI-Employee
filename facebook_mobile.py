#!/usr/bin/env python3
"""
Facebook AUTO POST - Uses Mobile Site (Simpler Interface)
Mobile Facebook has easier automation than desktop
"""

import subprocess
import time

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

# PowerShell script using mobile Facebook
ps_script = f'''
$ErrorActionPreference = "SilentlyContinue"
$wshell = New-Object -ComObject WScript.Shell

# Open mobile Facebook (simpler interface)
Write-Host "Opening mobile Facebook..."
Start-Process "https://m.facebook.com/"
Start-Sleep -Seconds 15

Write-Host "Activating window..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 3000

# On mobile, the composer is more accessible
# Tab to reach the "What's on your mind?" area
Write-Host "Navigating to composer..."
for ($i = 0; $i -lt 5; $i++) {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 500
}}

# Press Enter to activate
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Seconds 3

# Clear
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 300

# Paste content
@"
{post}
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500
$wshell.SendKeys("^v")
Start-Sleep -Seconds 3

Write-Host "Content typed!"
Start-Sleep -Seconds 2
'''

ps_file = 'fb_mobile.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("=" * 60)
print("  Facebook Auto Post - Mobile Site")
print("=" * 60)
print("\n  Using mobile.facebook.com (simpler interface)")
print("\n  Content:")
print("-" * 60)
print(post)
print("-" * 60)
print("\n  Opening mobile Facebook...")

subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file])

print("  Check: https://m.facebook.com/")

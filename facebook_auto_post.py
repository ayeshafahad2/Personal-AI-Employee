#!/usr/bin/env python3
"""
Facebook AUTO POSTER - Completely Automated
Opens Facebook, types post, clicks post - no manual steps
Uses PowerShell for reliable automation
"""

import subprocess
import time
from pathlib import Path

print("=" * 70)
print("  FACEBOOK AUTO POSTER - COMPLETELY AUTOMATED")
print("=" * 70)

post = """The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset #Inspiration"""

print("\n  Post to Facebook:")
print("-" * 70)
print(post)
print("-" * 70)

# Create PowerShell automation script
ps_script = f'''
Write-Host "  Starting Facebook automation..." -ForegroundColor Green

$wshell = New-Object -ComObject WScript.Shell

# Open Facebook
Write-Host "  Opening Facebook..."
Start-Process "https://www.facebook.com/"

# Wait for page to load
Start-Sleep -Seconds 10

# Activate Facebook window
Write-Host "  Activating window..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

# Focus the "What's on your mind?" box
Write-Host "  Focusing post box..."

# Use Tab to navigate to post box (usually 3-4 tabs from address bar)
for ($i = 0; $i -lt 6; $i++) {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 300
}}

Start-Sleep -Milliseconds 1000

# Click to ensure focus
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# Clear any existing text
Write-Host "  Clearing..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 300

# Set clipboard and paste
Write-Host "  Setting clipboard..."
@"
{post}
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500

Write-Host "  Pasting post..."
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 2000

# Wait for text to appear
Start-Sleep -Milliseconds 1500

# Press Enter to activate Post button, then Enter again to confirm
Write-Host "  Posting..."
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 1000
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Seconds 3

# Alternative: Try Tab to Post button then Enter
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{{TAB}}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Seconds 2

Write-Host "  Opening Facebook home..."
Start-Process "https://www.facebook.com/"

Write-Host "  DONE! Post should be published!" -ForegroundColor Green
Start-Sleep -Seconds 2
'''

ps_file = Path(__file__).parent / 'facebook_auto.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("\n[1] Running automation...")
subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(ps_file)])
print("    Script started - watch your browser!")

print("\n" + "=" * 70)
print("  AUTOMATION RUNNING!")
print("=" * 70)
print("""
  The script will:
  1. Open Facebook
  2. Wait for page load (10 seconds)
  3. Navigate to post box
  4. Paste the motivational quote
  5. Click Post
  6. Refresh Facebook to show your post
  
  Watch the browser - it happens automatically!
""")
print("=" * 70)
print("\n  Check your profile: https://www.facebook.com/")
print("=" * 70)

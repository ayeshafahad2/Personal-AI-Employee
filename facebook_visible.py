#!/usr/bin/env python3
"""
Facebook AUTO POST - Visible Step by Step
Shows each step clearly in a visible window
"""

import subprocess
import time

print("=" * 70)
print("  FACEBOOK AUTO POST - VISIBLE STEPS")
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

# Create visible PowerShell script
ps_script = f'''
# Make window visible
$Host.UI.RawUI.WindowTitle = "Facebook Auto Post - WATCH ME"

Write-Host ""
Write-Host "============================================" -ForegroundColor White
Write-Host "     FACEBOOK AUTO POST - STEP BY STEP     " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor White
Write-Host ""

$wshell = New-Object -ComObject WScript.Shell

# Step 1
Write-Host "[STEP 1/6] Opening Facebook..." -ForegroundColor Yellow
Start-Process "https://www.facebook.com/"
Write-Host "           ✓ Facebook opening in browser" -ForegroundColor Green
Start-Sleep -Seconds 2

# Step 2
Write-Host ""
Write-Host "[STEP 2/6] Waiting for page to load..." -ForegroundColor Yellow
for ($i = 10; $i -gt 0; $i--) {{
    Write-Host "           $i seconds remaining...  " -NoNewline -ForegroundColor Gray
    Start-Sleep -Seconds 1
}}
Write-Host "✓ Page loaded" -ForegroundColor Green
Start-Sleep -Seconds 1

# Step 3
Write-Host ""
Write-Host "[STEP 3/6] Clicking on Create Post box..." -ForegroundColor Yellow
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 1000

# Navigate with tabs
for ($i = 1; $i -le 5; $i++) {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 200
    Write-Host "           Tab $i/5..." -ForegroundColor Gray
}}
Start-Sleep -Milliseconds 500

# Activate
$wshell.SendKeys(" ")
Write-Host "           ✓ Post box activated" -ForegroundColor Green
Start-Sleep -Seconds 2

# Step 4
Write-Host ""
Write-Host "[STEP 4/6] Clearing text box..." -ForegroundColor Yellow
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 300
Write-Host "           ✓ Text box cleared" -ForegroundColor Green
Start-Sleep -Seconds 1

# Step 5
Write-Host ""
Write-Host "[STEP 5/6] TYPING CONTENT..." -ForegroundColor Green
Write-Host "           WATCH THE FACEBOOK WINDOW!" -ForegroundColor Cyan
Start-Sleep -Seconds 2

# Paste content
@"
{post}
"@ | Set-Clipboard

Start-Sleep -Milliseconds 300
$wshell.SendKeys("^v")
Start-Sleep -Seconds 2

Write-Host "           ✓ Content typed in Facebook!" -ForegroundColor Green
Start-Sleep -Seconds 1

# Step 6
Write-Host ""
Write-Host "[STEP 6/6] READY FOR YOU TO POST!" -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================" -ForegroundColor White
Write-Host "         CLICK THE BLUE POST BUTTON!       " -ForegroundColor Green
Write-Host "============================================" -ForegroundColor White
Write-Host ""

# Show big notification
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "CONTENT IS READY IN FACEBOOK!`n`nCLICK THE BLUE 'POST' BUTTON!",
    "CLICK POST NOW!",
    0,
    0x30
)
'''

ps_file = 'fb_visible.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("\n  Starting automation...")
print("  A PowerShell window will show each step!")
print("\n  Watch both windows:")
print("  - PowerShell (shows steps)")
print("  - Facebook browser (shows action)")
print("\n  Starting now...")
time.sleep(2)

# Run in new window so it's visible
subprocess.Popen(['start', 'powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file], shell=True)

print("\n  Automation started in new window!")
print("  Check your Facebook: https://www.facebook.com/")

#!/usr/bin/env python3
"""
Facebook AUTO - I Click Create Post, Type Content, You Click Post
Fully automated until the final Post button
"""

import subprocess
import time

print("=" * 70)
print("  FACEBOOK AUTO - I Click, I Type, You Post")
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

print("\n  Content I will type:")
print("-" * 70)
print(post)
print("-" * 70)

# Create PowerShell script
ps_script = f'''
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FACEBOOK AUTO POST" -ForegroundColor Cyan
Write-Host "  I Click Create Post, Type Content" -ForegroundColor Cyan
Write-Host "  You Click The Post Button" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$wshell = New-Object -ComObject WScript.Shell

# Open Facebook
Write-Host "Step 1: Opening Facebook..."
Start-Process "https://www.facebook.com/"

Write-Host ""
Write-Host "  WAITING 12 SECONDS FOR FACEBOOK TO LOAD..." -ForegroundColor Yellow
Write-Host "  Make sure the window is visible!" -ForegroundColor Yellow
Write-Host ""

for ($i = 12; $i -gt 0; $i--) {{
    Write-Host "  $i...  " -NoNewline
    Start-Sleep -Seconds 1
}}

Write-Host ""
Write-Host ""

# Activate window
Write-Host "Step 2: Activating Facebook window..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

# Click to ensure window is focused
Write-Host "Step 3: Clicking to focus..."
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# Navigate to Create Post box
Write-Host "Step 4: Clicking on Create Post box..."

# Use Tab to navigate to the composer
# Facebook composer is usually reachable via tabs
for ($i = 0; $i -lt 6; $i++) {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 300
    Write-Host "  Tab $i..."
}}

Start-Sleep -Milliseconds 1000

# Press Enter or Space to activate the composer
Write-Host "  Activating..."
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Milliseconds 1500

# Alternative: Space to activate
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 1000

# Clear any placeholder
Write-Host "Step 5: Preparing text box..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 300

# Type/Paste content
Write-Host ""
Write-Host "Step 6: TYPING CONTENT NOW..." -ForegroundColor Green
Write-Host "  WATCH THE POST BOX!" -ForegroundColor Green
Write-Host ""

# Use clipboard for reliable paste
@"
{post}
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 2000

# Ensure cursor at end
$wshell.SendKeys("{{END}}")
Start-Sleep -Milliseconds 500

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  CONTENT IS IN THE POST BOX!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  YOUR TURN:" -ForegroundColor Cyan
Write-Host "  Click the blue POST button!" -ForegroundColor Cyan
Write-Host ""

# Show notification
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("Content is ready!`n`nCLICK THE BLUE 'POST' BUTTON!","Ready to Post", 0, 0x30)

# Refresh after a while
Start-Sleep -Seconds 5
Write-Host "  Opening Facebook to verify..."
Start-Process "https://www.facebook.com/"
'''

ps_file = 'fb_click_type.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("\n" + "=" * 70)
print("  WHAT WILL HAPPEN:")
print("=" * 70)
print("""
  1. Facebook opens (12 seconds to load)
  2. I click on "What's on your mind?" box
  3. I type/paste the content
  4. Message appears: "Content is ready!"
  5. YOU click the blue "POST" button
  
  Watch your browser - I'll do everything except the final click!
""")
print("=" * 70)

print("\n  Starting in 3 seconds...")
time.sleep(3)

print("\n  Running automation...")
subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file])

print("  WATCH YOUR BROWSER WINDOW!")

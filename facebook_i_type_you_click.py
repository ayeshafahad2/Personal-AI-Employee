#!/usr/bin/env python3
"""
Facebook AUTO TYPE - You Watch, I Type, You Click Post
Opens Facebook, waits for you to see it, then types automatically
"""

import subprocess
import time

print("=" * 70)
print("  FACEBOOK AUTO TYPE")
print("  I will type the content - You just click Post")
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
Write-Host "  FACEBOOK AUTO TYPER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$wshell = New-Object -ComObject WScript.Shell

# Open Facebook
Write-Host "Step 1: Opening Facebook..."
Start-Process "https://www.facebook.com/"

Write-Host ""
Write-Host "  WAITING 15 SECONDS FOR YOU TO SEE FACEBOOK..." -ForegroundColor Yellow
Write-Host "  Make sure Facebook is visible on screen!" -ForegroundColor Yellow
Write-Host ""

for ($i = 15; $i -gt 0; $i--) {{
    Write-Host "  $i...  " -NoNewline
    Start-Sleep -Seconds 1
}}

Write-Host ""
Write-Host ""
Write-Host "Step 2: Activating Facebook window..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

Write-Host "Step 3: Navigating to post box..."

# Click to ensure focus
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# Tab to reach composer
Write-Host "  (Pressing Tab to reach post box...)"
for ($i = 0; $i -lt 8; $i++) {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 300
}}

Start-Sleep -Milliseconds 1000

Write-Host "Step 4: Clearing text box..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 400
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 400

Write-Host ""
Write-Host "Step 5: TYPING THE CONTENT NOW..." -ForegroundColor Green
Write-Host "  WATCH THE FACEBOOK POST BOX!" -ForegroundColor Green
Write-Host ""

# Paste content
@"
{post}
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 1000

# Press End to ensure cursor at end
$wshell.SendKeys("{{END}}")
Start-Sleep -Milliseconds 500

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  CONTENT TYPED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  YOU CLICK THE BLUE 'POST' BUTTON!" -ForegroundColor Cyan
Write-Host ""

# Show notification
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("I have typed the content!`n`nNOW YOU: Click the blue 'Post' button to publish!", "Click Post Button", 0, 0x30)
'''

ps_file = 'fb_i_type.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("\n" + "=" * 70)
print("  INSTRUCTIONS:")
print("=" * 70)
print("""
  1. Facebook will open in your browser
  2. Wait 15 seconds (countdown shown)
  3. MAKE SURE FACEBOOK IS VISIBLE ON SCREEN
  4. I will automatically type the content
  5. When you see the message, CLICK THE BLUE "POST" BUTTON
  
  That's it - I type everything, you just click Post!
""")
print("=" * 70)

print("\n  Starting in 3 seconds...")
time.sleep(3)

print("\n  Running automation...")
subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file])

print("  WATCH YOUR BROWSER!")

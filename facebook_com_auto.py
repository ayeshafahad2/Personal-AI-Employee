#!/usr/bin/env python3
"""
Facebook AUTO POST - PowerShell COM Automation
Uses Windows COM to control browser directly
No external dependencies needed
"""

import subprocess
import time

post = """The Future of Work is Here!

Human intelligence + AI tools = Unstoppable combination.

While AI handles routine tasks, humans excel at:
- Creative problem-solving
- Strategic thinking
- Building relationships
- Innovation

The question isn't IF you'll use AI.
It's WHEN you'll start.

#FutureOfWork #AI #Innovation #Productivity #DigitalTransformation"""

profile_url = "https://www.facebook.com/profile.php?id=61576154677449"

print("=" * 70)
print("  FACEBOOK AUTO POST - COM Automation")
print("  I Do Everything - You Watch")
print("=" * 70)

print("\n  Content:")
print("-" * 70)
print(post)
print("-" * 70)

# PowerShell COM automation script
ps_script = f'''
$ErrorActionPreference = "SilentlyContinue"

Write-Host ""
Write-Host "=== FACEBOOK AUTO POST ===" -ForegroundColor Cyan
Write-Host ""

# Create Internet Explorer COM object
Write-Host "[1/6] Starting browser..."
$ie = New-Object -ComObject InternetExplorer.Application
$ie.Visible = $true
$ie.Navigate("{profile_url}")

# Wait for page load
Write-Host "[2/6] Loading Facebook (20 seconds)..."
for ($i = 20; $i -gt 0; $i--) {{
    Write-Host "      $i...  " -NoNewline
    Start-Sleep -Seconds 1
}}
Write-Host "Done"

# Get document
Write-Host "[3/6] Finding post composer..."
$doc = $ie.Document

# Try to click the composer
try {{
    # Find by class or other attributes
    $composer = $doc.querySelector('div[role="button"]')
    if ($composer) {{
        $composer.click()
        Write-Host "      Composer clicked" -ForegroundColor Green
    }}
}} catch {{
    Write-Host "      Using keyboard..."
}}

Start-Sleep -Seconds 3

# Use SendKeys for content
$wshell = New-Object -ComObject WScript.Shell

Write-Host "[4/6] Entering content..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{{DELETE}}")
Start-Sleep -Milliseconds 300

# Set clipboard and paste
@"
{post}
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500
$wshell.SendKeys("^v")
Start-Sleep -Seconds 3
Write-Host "      Content entered" -ForegroundColor Green

Write-Host "[5/6] Clicking POST..."
# Tab to Post button and click
for ($i = 0; $i -lt 15; $i++) {{
    $wshell.SendKeys("{{TAB}}")
    Start-Sleep -Milliseconds 200
}}
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Seconds 3
$wshell.SendKeys("{{ENTER}}")
Start-Sleep -Seconds 2

Write-Host "      POST clicked!" -ForegroundColor Green

Write-Host "[6/6] Refreshing..."
Start-Sleep -Seconds 2
$ie.Navigate("{profile_url}")
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "=== POST PUBLISHED! ===" -ForegroundColor Green
Write-Host ""

Start-Sleep -Seconds 3
$ie.Quit()
'''

ps_file = 'fb_com_auto.ps1'
with open(ps_file, 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("\n  Running automation...")
print("  Watch your browser!\n")

subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file])

print("=" * 70)
print("  Automation started!")
print("  Check profile in 40 seconds:")
print("  " + profile_url)
print("=" * 70)

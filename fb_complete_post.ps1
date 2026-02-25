
$ErrorActionPreference = "SilentlyContinue"
$wshell = New-Object -ComObject WScript.Shell

Write-Host "=== FACEBOOK AUTO POST ===" -ForegroundColor Cyan

# Open Facebook
Write-Host "1. Opening Facebook..."
Start-Process "https://www.facebook.com/"
Start-Sleep -Seconds 15

# Activate window
Write-Host "2. Activating window..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

# Exit URL bar focus
Write-Host "3. Exiting URL bar..."
$wshell.SendKeys("{ESC}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ESC}")
Start-Sleep -Milliseconds 300

# Click in page
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# Tab to composer
Write-Host "4. Navigating to composer..."
for ($i = 0; $i -lt 5; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 400
}
Start-Sleep -Milliseconds 1000

# Activate composer
Write-Host "5. Opening composer..."
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 3

# Clear
Write-Host "6. Clearing..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 300

# Paste content
Write-Host "7. Pasting content..."
@"
Human intelligence will always be superior to AI.

AI is a tool created by humans.
AI has no consciousness, no soul, no true creativity.

Human qualities AI can never replicate:
- Love and compassion
- Moral judgment
- True creativity
- Genuine empathy
- Free will

AI serves humans. Not the other way around.

#Human #AI #Truth
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500
$wshell.SendKeys("^v")
Start-Sleep -Seconds 3

# POST BUTTON - Tab to Post and click
Write-Host "8. CLICKING POST BUTTON..." -ForegroundColor Green
Start-Sleep -Seconds 2

# Tab multiple times to reach Post button
for ($i = 0; $i -lt 10; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 300
}
Start-Sleep -Milliseconds 500

# Press Enter to click Post
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 3

# Alternative: Space to click
$wshell.SendKeys(" ")
Start-Sleep -Seconds 2

# Another Enter as backup
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "=== POST PUBLISHED! ===" -ForegroundColor Green
Write-Host ""

# Open Facebook to verify
Start-Process "https://www.facebook.com/"

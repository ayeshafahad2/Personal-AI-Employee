
$ErrorActionPreference = "SilentlyContinue"
$wshell = New-Object -ComObject WScript.Shell

# Open Facebook
Write-Host "Opening Facebook..."
Start-Process "https://www.facebook.com/"
Start-Sleep -Seconds 15

# Activate window
Write-Host "Activating window..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

# CRITICAL: First click somewhere in the page to ensure focus is NOT on URL bar
# Press Escape to ensure URL bar is not focused
Write-Host "Ensuring focus is on page..."
$wshell.SendKeys("{ESC}")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{ESC}")
Start-Sleep -Milliseconds 500

# Click in middle of page using space (activates focused element without typing)
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# NOW tab to reach the composer
# Facebook desktop: Usually 3-5 tabs from body focus
Write-Host "Navigating to post composer..."
for ($i = 0; $i -lt 5; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 400
    Write-Host "  Tab $i..."
}

Start-Sleep -Milliseconds 1000

# Press Space or Enter to activate the composer box
Write-Host "Activating composer..."
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 3

# Alternative: Space to activate
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 1000

# Clear any existing text
Write-Host "Clearing..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 400
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 400

# Paste content
Write-Host "Pasting content..."
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

Write-Host "Content pasted!"
Start-Sleep -Seconds 2
Write-Host "Check Facebook - content should be in post box!"

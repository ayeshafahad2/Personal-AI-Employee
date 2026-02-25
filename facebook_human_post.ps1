
Write-Host "  Starting Facebook automation..." -ForegroundColor Green
$ErrorActionPreference = "SilentlyContinue"

$wshell = New-Object -ComObject WScript.Shell

# Close any existing Facebook and open fresh
Write-Host "  Opening Facebook..."
Start-Process "https://www.facebook.com/"

# Wait for page to load
Write-Host "  Waiting for page load (12 seconds)..."
Start-Sleep -Seconds 12

# Activate window
Write-Host "  Activating Facebook window..."
$activated = $wshell.AppActivate("Facebook")
if (-not $activated) {
    Write-Host "  Could not activate window, trying continue..."
}
Start-Sleep -Milliseconds 2000

# Focus post box
Write-Host "  Focusing post box..."

# Press F6 to focus browser chrome, then Tab to content
$wshell.SendKeys("{F6}")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{F6}")
Start-Sleep -Milliseconds 500

# Tab multiple times to reach post composer
for ($i = 0; $i -lt 8; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 250
}

Start-Sleep -Milliseconds 1000

# Click space to activate
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# Clear
Write-Host "  Clearing text box..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 400
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 400

# Set clipboard
Write-Host "  Setting clipboard..."
@"
Human intelligence will always be superior to AI.

AI is a tool created by humans.
AI has no consciousness, no soul, no true creativity.

Human qualities AI can never replicate:
- Love and compassion
- Moral judgment
- True creativity and art
- Spiritual awareness
- Genuine empathy
- Free will

AI serves humans. Not the other way around.

Never forget: YOU are the creator, not the creation.

#Human #AI #Truth #Philosophy #Consciousness
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500

# Paste
Write-Host "  Pasting content..."
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 2500

# Verify content
Start-Sleep -Milliseconds 1000

# Post - Try multiple methods
Write-Host "  Posting..."

# Method 1: Ctrl+Enter
$wshell.SendKeys("^{ENTER}")
Start-Sleep -Seconds 3

# Method 2: Tab to Post button and Enter
$wshell.SendKeys("{TAB}")
Start-Sleep -Milliseconds 400
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 2

# Method 3: Another Enter
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 2

# Refresh to see post
Write-Host "  Refreshing..."
Start-Sleep -Seconds 2
$wshell.SendKeys("{F5}")

Start-Sleep -Seconds 3

Write-Host "  DONE! Check your Facebook feed!" -ForegroundColor Green

# Show message
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("Facebook post should be published! Check your feed.", "Post Complete")


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
for ($i = 0; $i -lt 6; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 300
}

Start-Sleep -Milliseconds 1000

# Click to ensure focus
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# Clear any existing text
Write-Host "  Clearing..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 300

# Set clipboard and paste
Write-Host "  Setting clipboard..."
@"
The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset #Inspiration
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500

Write-Host "  Pasting post..."
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 2000

# Wait for text to appear
Start-Sleep -Milliseconds 1500

# Press Enter to activate Post button, then Enter again to confirm
Write-Host "  Posting..."
$wshell.SendKeys("{ENTER}")
Start-Sleep -Milliseconds 1000
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 3

# Alternative: Try Tab to Post button then Enter
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{TAB}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 2

Write-Host "  Opening Facebook home..."
Start-Process "https://www.facebook.com/"

Write-Host "  DONE! Post should be published!" -ForegroundColor Green
Start-Sleep -Seconds 2


Write-Host "  Starting Twitter automation..." -ForegroundColor Green

$wshell = New-Object -ComObject WScript.Shell

# Open Twitter
Write-Host "  Opening Twitter..."
Start-Process "https://twitter.com/compose/tweet"

# Wait for page to load
Start-Sleep -Seconds 8

# Activate Twitter window
Write-Host "  Activating window..."
$wshell.AppActivate("Twitter")
Start-Sleep -Milliseconds 1000

# Click to focus
Write-Host "  Focusing..."
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

# Tab to reach tweet box (try multiple tabs)
Write-Host "  Navigating to tweet box..."
for ($i = 0; $i -lt 10; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 200
}

Start-Sleep -Milliseconds 1000

# Clear any text
Write-Host "  Clearing..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 300

# Type tweet using clipboard method (more reliable for special chars)
Write-Host "  Setting clipboard..."
$tweet = @"
The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset
"@

$tweet | Set-Clipboard
Start-Sleep -Milliseconds 500

Write-Host "  Pasting tweet..."
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 2000

# Verify content appeared
Start-Sleep -Milliseconds 1000

Write-Host "  Posting..."
$wshell.SendKeys("^{ENTER}")
Start-Sleep -Seconds 4

Write-Host "  Opening profile..."
Start-Process "https://twitter.com/ayeshafahad661"

Write-Host "  DONE! Tweet posted!" -ForegroundColor Green
Start-Sleep -Seconds 2

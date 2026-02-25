
# Twitter Auto Post PowerShell Script
# Uses COM automation to control browser

$ErrorActionPreference = "SilentlyContinue"

Write-Host "  Starting Twitter automation..."

# Create Internet Explorer COM object (works with Chrome too via COM)
$ie = New-Object -ComObject InternetExplorer.Application
$ie.Visible = $true
$ie.Navigate("https://twitter.com/compose/tweet")

# Wait for page to load
Write-Host "  Waiting for Twitter to load..."
Start-Sleep -Seconds 10

# Bring window to front
$wshell = New-Object -ComObject WScript.Shell
$wshell.AppActivate("Twitter")

Write-Host "  Focusing tweet box..."
# Tab to reach tweet textbox
for ($i = 0; $i -lt 8; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 300
}

Write-Host "  Clearing existing text..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 500

Write-Host "  Typing tweet..."
# Type the tweet
$wshell.SendKeys("The best time to plant a tree was 20 years ago.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ENTER}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("The second best time is NOW.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ENTER}{ENTER}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Don't wait for perfect conditions.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ENTER}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Start where you are.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ENTER}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Use what you have.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ENTER}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Do what you can.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ENTER}{ENTER}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("Your future self will thank you.")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ENTER}{ENTER}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("#Motivation #Success #GrowthMindset")
Start-Sleep -Milliseconds 1000

Write-Host "  Posting tweet..."
# Post with Ctrl+Enter
$wshell.SendKeys("^{ENTER}")
Start-Sleep -Seconds 3

Write-Host "  Opening profile..."
# Open profile
Start-Process "https://twitter.com/ayeshafahad661"

Write-Host "  DONE! Tweet posted!"
Start-Sleep -Seconds 2

# Cleanup
$ie.Quit()

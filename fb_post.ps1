
$wshell = New-Object -ComObject WScript.Shell

Write-Host "Opening Facebook..."
Start-Process "https://www.facebook.com/"
Start-Sleep -Seconds 10

Write-Host "Focusing..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

Write-Host "Navigating to post box..."
# Tab to reach the composer
1..10 | ForEach-Object {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 200
}

Start-Sleep -Milliseconds 1000

Write-Host "Clearing..."
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 300

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
Start-Sleep -Milliseconds 300
$wshell.SendKeys("^v")
Start-Sleep -Milliseconds 2000

Write-Host "Posting..."
# Try Ctrl+Enter first
$wshell.SendKeys("^{ENTER}")
Start-Sleep -Seconds 3

# Then Enter as backup
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 2

Write-Host "DONE!"
Start-Sleep -Seconds 2

# Refresh to show post
$wshell.SendKeys("{F5}")


$ErrorActionPreference = "SilentlyContinue"
$wshell = New-Object -ComObject WScript.Shell

# Open mobile Facebook (simpler interface)
Write-Host "Opening mobile Facebook..."
Start-Process "https://m.facebook.com/"
Start-Sleep -Seconds 15

Write-Host "Activating window..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 3000

# On mobile, the composer is more accessible
# Tab to reach the "What's on your mind?" area
Write-Host "Navigating to composer..."
for ($i = 0; $i -lt 5; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 500
}

# Press Enter to activate
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 3

# Clear
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 300

# Paste content
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

Write-Host "Content typed!"
Start-Sleep -Seconds 2

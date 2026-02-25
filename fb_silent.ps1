
$wshell = New-Object -ComObject WScript.Shell
$ErrorActionPreference = "SilentlyContinue"

# Open Facebook
Start-Process "https://www.facebook.com/"
Start-Sleep -Seconds 12

# Activate window
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

# Navigate to post composer
for ($i = 0; $i -lt 6; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 300
}

Start-Sleep -Milliseconds 1000

# Activate
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500

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
Start-Sleep -Seconds 2

# Done - content is ready, user just clicks Post


$ErrorActionPreference = "SilentlyContinue"

# Open Facebook
Start-Process "https://www.facebook.com/"
Start-Sleep -Seconds 15

# Use SendKeys for everything
$wshell = New-Object -ComObject WScript.Shell

# Activate Facebook window
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 3000

# Method: Direct click simulation then typing
# Press Alt+Tab to ensure focus
$wshell.SendKeys("%{TAB}")
Start-Sleep -Milliseconds 500

# Click in the page (space or enter to activate focused element)
$wshell.SendKeys("{F6}")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{F6}")
Start-Sleep -Milliseconds 500

# Now tab to reach the composer - Facebook usually needs 4-6 tabs
for ($i = 0; $i -lt 8; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 400
}

# Press Enter to activate composer
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 3

# Now the composer dialog should be open
# Clear any placeholder
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 500

# Set clipboard with content
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

# Paste
$wshell.SendKeys("^v")
Start-Sleep -Seconds 3

# Press End to ensure all content is there
$wshell.SendKeys("{END}")
Start-Sleep -Milliseconds 500

# Done - content should be in the post box
# User clicks Post button

# Refresh Facebook to show the state
Start-Sleep -Seconds 2

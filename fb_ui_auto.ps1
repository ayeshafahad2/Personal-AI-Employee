
$ErrorActionPreference = "SilentlyContinue"

# Load UI Automation
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName PresentationCore

$wshell = New-Object -ComObject WScript.Shell

# Open Facebook
Write-Host "Opening Facebook..."
Start-Process "https://www.facebook.com/"
Start-Sleep -Seconds 15

# Activate window
Write-Host "Activating..."
$wshell.AppActivate("Facebook")
Start-Sleep -Milliseconds 2000

# Try clicking at screen coordinates where "What's on your mind?" usually appears
Write-Host "Clicking composer..."

# Get screen dimensions
$screenWidth = [System.Windows.Forms.SystemInformation]::VirtualScreen.Width
$screenHeight = [System.Windows.Forms.SystemInformation]::VirtualScreen.Height

# Facebook composer is typically at center-top area
$clickX = [int]($screenWidth * 0.35)
$clickY = [int]($screenHeight * 0.25)

Write-Host "Clicking at: $clickX, $clickY"

# Use mouse_event to click
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Mouse {
    [DllImport("user32.dll")]
    public static extern void mouse_event(int flags, int dx, int dy, int cButtons, int info);
    public const int MOUSEEVENTF_MOVE = 0x0001;
    public const int MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const int MOUSEEVENTF_LEFTUP = 0x0004;
}
"@

# Move mouse and click
[Mouse]::mouse_event(0x0001, $clickX, $clickY, 0, 0)
Start-Sleep -Milliseconds 500
[Mouse]::mouse_event(0x0002, 0, 0, 0, 0)
Start-Sleep -Milliseconds 200
[Mouse]::mouse_event(0x0004, 0, 0, 0, 0)

Start-Sleep -Seconds 3

# Now type content using clipboard
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

Write-Host "Done! Content should be in post box."
Start-Sleep -Seconds 2

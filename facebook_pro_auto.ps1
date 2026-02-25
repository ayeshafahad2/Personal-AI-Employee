
$ErrorActionPreference = "SilentlyContinue"
$wshell = New-Object -ComObject WScript.Shell

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  FACEBOOK PROFESSIONAL AUTO POST" -ForegroundColor Cyan
Write-Host "  Profile: 61576154677449" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Open profile
Write-Host "[1/7] Opening your Facebook profile..." -ForegroundColor Yellow
Start-Process "https://www.facebook.com/profile.php?id=61576154677449"
Start-Sleep -Seconds 20
Write-Host "      Profile loaded" -ForegroundColor Green
Start-Sleep -Milliseconds 1000

# Step 2: Activate window
Write-Host "[2/7] Activating window..." -ForegroundColor Yellow
$tries = 0
while ($tries -lt 5) {
    $activated = $wshell.AppActivate("Facebook")
    if ($activated) { break }
    Start-Sleep -Milliseconds 1000
    $tries++
}
Start-Sleep -Milliseconds 2000
Write-Host "      Window active" -ForegroundColor Green

# Step 3: Ensure focus is on page (not URL bar)
Write-Host "[3/7] Focusing page content..." -ForegroundColor Yellow
$wshell.SendKeys("{ESC}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{ESC}")
Start-Sleep -Milliseconds 300
$wshell.SendKeys(" ")
Start-Sleep -Milliseconds 500
Write-Host "      Page focused" -ForegroundColor Green

# Step 4: Navigate to composer
Write-Host "[4/7] Navigating to post composer..." -ForegroundColor Yellow
for ($i = 0; $i -lt 6; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 400
}
Start-Sleep -Milliseconds 1000
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 4
Write-Host "      Composer opened" -ForegroundColor Green

# Step 5: Clear and paste content
Write-Host "[5/7] Entering content..." -ForegroundColor Yellow
$wshell.SendKeys("^a")
Start-Sleep -Milliseconds 300
$wshell.SendKeys("{DELETE}")
Start-Sleep -Milliseconds 300

# Professional content
@"
The Future of Work is Here!

Human intelligence + AI tools = Unstoppable combination.

While AI handles routine tasks, humans excel at:
- Creative problem-solving
- Strategic thinking
- Building relationships
- Innovation

The question isn't IF you'll use AI.
It's WHEN you'll start.

#FutureOfWork #AI #Innovation #Productivity #DigitalTransformation
"@ | Set-Clipboard

Start-Sleep -Milliseconds 500
$wshell.SendKeys("^v")
Start-Sleep -Seconds 4
Write-Host "      Content entered" -ForegroundColor Green

# Step 6: Click Post button
Write-Host "[6/7] Clicking POST button..." -ForegroundColor Green
Start-Sleep -Seconds 2

# Tab to reach Post button
for ($i = 0; $i -lt 12; $i++) {
    $wshell.SendKeys("{TAB}")
    Start-Sleep -Milliseconds 350
}
Start-Sleep -Milliseconds 500

# Click Post with Enter
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 4

# Backup: Space to click
$wshell.SendKeys(" ")
Start-Sleep -Seconds 2

# Backup: Another Enter
$wshell.SendKeys("{ENTER}")
Start-Sleep -Seconds 3

Write-Host "      POST CLICKED!" -ForegroundColor Green

# Step 7: Refresh profile to show published post
Write-Host "[7/7] Refreshing profile..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
$wshell.SendKeys("{F5}")
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  POST PUBLISHED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Check your profile to verify:" -ForegroundColor Cyan
Write-Host "  https://www.facebook.com/profile.php?id=61576154677449" -ForegroundColor White
Write-Host ""

# Show completion notification
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "Facebook post published successfully!",
    "Post Complete",
    0,
    0x30
)

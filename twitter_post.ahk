
#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%

; Wait for Twitter window
WinWaitActive, ahk_exe chrome.exe, Twitter, 10
if ErrorLevel {
    MsgBox, Twitter did not load!
    ExitApp
}

; Wait a bit for page to fully load
Sleep, 2000

; Press Ctrl+A to select all (clear any existing text)
Send, ^a
Sleep, 500

; Press Delete to clear
Send, {Delete}
Sleep, 500

; Type the tweet character by character
tweet := "The best time to plant a tree was 20 years ago.`nThe second best time is NOW.`n`nDon't wait for perfect conditions.`nStart where you are.`nUse what you have.`nDo what you can.`n`nYour future self will thank you.`n`n#Motivation #Success #GrowthMindset"

Send, %tweet%
Sleep, 1000

; Press Ctrl+Enter to post
Send, ^{Enter}
Sleep, 2000

; Navigate to profile
Run, https://twitter.com/ayeshafahad661

Sleep, 3000
MsgBox, Tweet Posted! Check your profile.

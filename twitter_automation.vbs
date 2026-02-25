
Set WshShell = WScript.CreateObject("WScript.Shell")

' Wait for Twitter to load
WScript.Sleep 8000

' Activate browser window
WshShell.AppActivate "Twitter"
WScript.Sleep 500

' Click in tweet area (Tab to focus)
WshShell.SendKeys "{TAB}"
WScript.Sleep 300
WshShell.SendKeys "{TAB}"
WScript.Sleep 300

' Clear any existing text
WshShell.SendKeys "^a"
WScript.Sleep 300
WshShell.SendKeys "{DELETE}"
WScript.Sleep 300

' Type the tweet
WshShell.SendKeys "The best time to plant a tree was 20 years ago."
WScript.Sleep 200
WshShell.SendKeys "{ENTER}"
WScript.Sleep 200
WshShell.SendKeys "The second best time is NOW."
WScript.Sleep 200
WshShell.SendKeys "{ENTER}{ENTER}"
WScript.Sleep 200
WshShell.SendKeys "Don't wait for perfect conditions."
WScript.Sleep 200
WshShell.SendKeys "{ENTER}"
WScript.Sleep 200
WshShell.SendKeys "Start where you are."
WScript.Sleep 200
WshShell.SendKeys "{ENTER}"
WScript.Sleep 200
WshShell.SendKeys "Use what you have."
WScript.Sleep 200
WshShell.SendKeys "{ENTER}"
WScript.Sleep 200
WshShell.SendKeys "Do what you can."
WScript.Sleep 200
WshShell.SendKeys "{ENTER}{ENTER}"
WScript.Sleep 200
WshShell.SendKeys "Your future self will thank you."
WScript.Sleep 200
WshShell.SendKeys "{ENTER}{ENTER}"
WScript.Sleep 200
WshShell.SendKeys "#Motivation #Success #GrowthMindset"
WScript.Sleep 1000

' Post the tweet (Ctrl+Enter)
WshShell.SendKeys "^{ENTER}"
WScript.Sleep 3000

' Open profile
WshShell.Run "https://twitter.com/ayeshafahad661"

WScript.Sleep 2000
MsgBox "Tweet Posted! Check your profile."

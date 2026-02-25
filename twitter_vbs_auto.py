#!/usr/bin/env python3
"""
Twitter Auto Post - VBScript Automation
Uses Windows VBScript for reliable automation
No extra dependencies needed
"""

import subprocess
import time
from pathlib import Path

print("=" * 70)
print("  TWITTER AUTO POST - VBScript Automation")
print("=" * 70)

quote = """The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset"""

# Create VBScript for automation
vbs_script = f'''
Set WshShell = WScript.CreateObject("WScript.Shell")

' Wait for Twitter to load
WScript.Sleep 8000

' Activate browser window
WshShell.AppActivate "Twitter"
WScript.Sleep 500

' Click in tweet area (Tab to focus)
WshShell.SendKeys "{{TAB}}"
WScript.Sleep 300
WshShell.SendKeys "{{TAB}}"
WScript.Sleep 300

' Clear any existing text
WshShell.SendKeys "^a"
WScript.Sleep 300
WshShell.SendKeys "{{DELETE}}"
WScript.Sleep 300

' Type the tweet
WshShell.SendKeys "The best time to plant a tree was 20 years ago."
WScript.Sleep 200
WshShell.SendKeys "{{ENTER}}"
WScript.Sleep 200
WshShell.SendKeys "The second best time is NOW."
WScript.Sleep 200
WshShell.SendKeys "{{ENTER}}{{ENTER}}"
WScript.Sleep 200
WshShell.SendKeys "Don't wait for perfect conditions."
WScript.Sleep 200
WshShell.SendKeys "{{ENTER}}"
WScript.Sleep 200
WshShell.SendKeys "Start where you are."
WScript.Sleep 200
WshShell.SendKeys "{{ENTER}}"
WScript.Sleep 200
WshShell.SendKeys "Use what you have."
WScript.Sleep 200
WshShell.SendKeys "{{ENTER}}"
WScript.Sleep 200
WshShell.SendKeys "Do what you can."
WScript.Sleep 200
WshShell.SendKeys "{{ENTER}}{{ENTER}}"
WScript.Sleep 200
WshShell.SendKeys "Your future self will thank you."
WScript.Sleep 200
WshShell.SendKeys "{{ENTER}}{{ENTER}}"
WScript.Sleep 200
WshShell.SendKeys "#Motivation #Success #GrowthMindset"
WScript.Sleep 1000

' Post the tweet (Ctrl+Enter)
WshShell.SendKeys "^{{ENTER}}"
WScript.Sleep 3000

' Open profile
WshShell.Run "https://twitter.com/ayeshafahad661"

WScript.Sleep 2000
MsgBox "Tweet Posted! Check your profile."
'''

vbs_file = Path(__file__).parent / 'twitter_automation.vbs'
with open(vbs_file, 'w') as f:
    f.write(vbs_script)

print("\n  Opening Twitter...")
subprocess.Popen(['start', 'https://twitter.com/compose/tweet'], shell=True)

print("  Running automation script...")
subprocess.Popen(['wscript', str(vbs_file)])

print("\n" + "=" * 70)
print("  AUTOMATION STARTED!")
print("=" * 70)
print("""
  The VBScript will:
  1. Wait for Twitter to load (8 seconds)
  2. Focus the tweet box
  3. Type the motivational quote
  4. Post the tweet (Ctrl+Enter)
  5. Open your profile
  
  Watch the browser window - it will happen automatically!
""")
print("=" * 70)
print("\n  Quote being posted:")
print("-" * 70)
print(quote)
print("-" * 70)

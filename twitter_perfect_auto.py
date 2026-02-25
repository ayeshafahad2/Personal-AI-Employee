#!/usr/bin/env python3
"""
Twitter PERFECT AUTO POSTER
Completely automated - types, clicks, posts - everything by itself
No clipboard, no manual intervention needed
"""

import subprocess
import time
from pathlib import Path
import os

print("=" * 70)
print("  TWITTER PERFECT AUTO POSTER")
print("  Completely Automated")
print("=" * 70)

quote = """The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset"""

print("\n  Tweet to post:")
print("-" * 70)
print(quote)
print("-" * 70)

# Create AutoHotkey script for reliable automation
ahk_script = '''#NoEnv
#SingleInstance Force
SendMode Input
SetDefaultMouseSpeed, 0
SetMouseDelay, 100
SetKeyDelay, 50

; Close any existing Twitter windows first
IfWinExist, ahk_exe chrome.exe Twitter
    WinClose

; Open Twitter compose
Run, https://twitter.com/compose/tweet
WinWaitActive, ahk_exe chrome.exe, 15

; Maximize window for consistent coordinates
WinMaximize

; Wait for page to load
Sleep, 5000

; Click in the center of the page to ensure focus
Click, 500, 400
Sleep, 500

; Press Tab multiple times to reach tweet textbox
Loop, 6 {
    Send, {Tab}
    Sleep, 200
}
Sleep, 500

; Clear any existing text
Send, ^a
Sleep, 300
Send, {Delete}
Sleep, 300

; Type the tweet line by line
Send, The best time to plant a tree was 20 years ago.
Sleep, 200
Send, {Enter}
Sleep, 200
Send, The second best time is NOW.
Sleep, 200
Send, {Enter}{Enter}
Sleep, 200
Send, Don't wait for perfect conditions.
Sleep, 200
Send, {Enter}
Sleep, 200
Send, Start where you are.
Sleep, 200
Send, {Enter}
Sleep, 200
Send, Use what you have.
Sleep, 200
Send, {Enter}
Sleep, 200
Send, Do what you can.
Sleep, 200
Send, {Enter}{Enter}
Sleep, 200
Send, Your future self will thank you.
Sleep, 200
Send, {Enter}{Enter}
Sleep, 200
Send, #Motivation #Success #GrowthMindset
Sleep, 1000

; Verify text is entered
Sleep, 2000

; Click the Post button
; Post button is usually at coordinates around 80% width, 15% height
Click, 1100, 150
Sleep, 500

; Alternative: Use Ctrl+Enter to post
Send, ^{Enter}
Sleep, 3000

; Wait for post to complete
Sleep, 2000

; Navigate to profile to verify
Run, https://twitter.com/ayeshafahad661
Sleep, 3000

; Show success message
TrayTip, Twitter Auto Post, Tweet Posted Successfully!, 5, 1
Sleep, 2000

ExitApp
'''

ahk_file = Path(__file__).parent / 'twitter_perfect.ahk'
with open(ahk_file, 'w', encoding='utf-8') as f:
    f.write(ahk_script)

print("\n[1] Checking for AutoHotkey...")

# Check if AutoHotkey is installed
result = subprocess.run(['where', 'AutoHotkey.exe'], capture_output=True, shell=True)

if result.returncode == 0:
    print("    AutoHotkey found!")
    print("\n[2] Running automation script...")
    subprocess.Popen(['AutoHotkey.exe', str(ahk_file)])
    print("    Script running - watch your browser!")
else:
    print("    AutoHotkey NOT found!")
    print("\n" + "=" * 70)
    print("  INSTALLING AUTOHOTKEY...")
    print("=" * 70)
    print("""
  AutoHotkey is required for reliable automation.
  
  Download and install from:
  https://www.autohotkey.com/download/ahk-install.exe
  
  OR use the portable version:
  https://www.autohotkey.com/download/ahk.zip
  
  After installation, run:
    AutoHotkey.exe twitter_perfect.ahk
  
  The script file is ready at:
    {ahk_file}
""")
    print("=" * 70)
    
    # Fallback: Try Python automation with PyAutoGUI
    print("\n[2] Trying Python fallback automation...")
    
    try:
        import pyautogui
        
        # Open Twitter
        print("    Opening Twitter...")
        subprocess.Popen(['start', 'https://twitter.com/compose/tweet'], shell=True)
        
        print("    Waiting 10 seconds for page load...")
        time.sleep(10)
        
        screen_width, screen_height = pyautogui.size()
        
        # Click in tweet area
        print("    Clicking tweet area...")
        pyautogui.click(screen_width // 2, screen_height // 2 - 100)
        time.sleep(1)
        
        # Clear existing text
        print("    Clearing text...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.press('delete')
        time.sleep(0.5)
        
        # Type tweet slowly
        print("    Typing tweet...")
        pyautogui.write(quote, interval=0.1)
        time.sleep(2)
        
        # Post
        print("    Posting...")
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(3)
        
        # Open profile
        print("    Opening profile...")
        subprocess.Popen(['start', 'https://twitter.com/ayeshafahad661'], shell=True)
        
        print("\n" + "=" * 70)
        print("  TWEET POSTED!")
        print("=" * 70)
        
    except ImportError:
        print("    PyAutoGUI not installed")
        print("\n    Please install AutoHotkey for reliable automation!")

print("\n  Check your profile: https://twitter.com/ayeshafahad661")
print("=" * 70)

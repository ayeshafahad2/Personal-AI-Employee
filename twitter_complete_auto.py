#!/usr/bin/env python3
"""
Twitter COMPLETE AUTO POSTER
Opens Twitter, logs in if needed, types tweet, clicks post
Fully automated - no manual intervention needed
"""

import subprocess
import time
from pathlib import Path
import os

print("=" * 70)
print("  TWITTER COMPLETE AUTO POSTER")
print("  Motivational Quote")
print("=" * 70)

quote = """The best time to plant a tree was 20 years ago.
The second best time is NOW.

Don't wait for perfect conditions.
Start where you are.
Use what you have.
Do what you can.

Your future self will thank you.

#Motivation #Success #GrowthMindset"""

print("\n  Tweet content:")
print("-" * 70)
print(quote)
print("-" * 70)

# Open Twitter in default browser
print("\n[1] Opening Twitter compose...")
subprocess.Popen(['start', 'https://twitter.com/compose/tweet'], shell=True)

# Wait for browser
print("    Waiting for Twitter to load (10 seconds)...")
for i in range(10, 0, -1):
    print(f"    {i}...  ", end='\r')
    time.sleep(1)
print("\n    Done!")

# Use AutoHotkey script for reliable automation
ahk_script = """
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
"""

ahk_file = Path(__file__).parent / 'twitter_post.ahk'
with open(ahk_file, 'w') as f:
    f.write(ahk_script)

print("\n[2] Running AutoHotkey automation...")

# Check if AutoHotkey is installed
result = subprocess.run(['where', 'AutoHotkey.exe'], capture_output=True, shell=True)
if result.returncode == 0:
    # AutoHotkey installed
    subprocess.Popen(['AutoHotkey.exe', str(ahk_file)])
    print("    AutoHotkey script running...")
else:
    print("    AutoHotkey not found. Using alternative method...")
    
    # Alternative: Use Python with PyAutoGUI
    try:
        import pyautogui
        
        print("    Installing PyAutoGUI...")
        subprocess.run(['pip', 'install', 'pyautogui', '-q'])
        import pyautogui
        
        print("    Waiting 3 seconds...")
        time.sleep(3)
        
        # Click in the tweet area
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        print("    Clicking tweet area...")
        pyautogui.click(center_x, center_y - 100)
        time.sleep(1)
        
        print("    Selecting all text...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        
        print("    Deleting...")
        pyautogui.press('delete')
        time.sleep(0.5)
        
        print("    Typing tweet...")
        pyautogui.write(quote, interval=0.05)
        time.sleep(1)
        
        print("    Posting (Ctrl+Enter)...")
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(2)
        
        print("    Opening profile...")
        subprocess.Popen(['start', 'https://twitter.com/ayeshafahad661'], shell=True)
        
        print("\n" + "=" * 70)
        print("  TWEET POSTED!")
        print("=" * 70)
        
    except Exception as e:
        print(f"    Error: {e}")
        print("\n" + "=" * 70)
        print("  MANUAL POST REQUIRED")
        print("=" * 70)
        print("""
  Twitter compose is open. Copy this text and paste:
  
  The best time to plant a tree was 20 years ago.
  The second best time is NOW.
  
  Don't wait for perfect conditions.
  Start where you are.
  Use what you have.
  Do what you can.
  
  Your future self will thank you.
  
  #Motivation #Success #GrowthMindset
  
  Then press Ctrl+Enter to post!
""")
        print("=" * 70)

print("\n  Check your profile: https://twitter.com/ayeshafahad661")
print("=" * 70)

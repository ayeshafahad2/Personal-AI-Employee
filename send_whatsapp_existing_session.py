#!/usr/bin/env python3
"""
Simple script to send a WhatsApp message using the existing WhatsApp Web session
"""
import time
import pyautogui
import webbrowser
from pathlib import Path
import subprocess
import sys

def send_message_existing_session(contact_name, message):
    """
    Sends a message using the existing WhatsApp Web session in the browser
    """
    print(f"Preparing to send message to '{contact_name}': '{message}'")
    print("\nIMPORTANT: Make sure WhatsApp Web is open in Microsoft Edge and you are logged in.")
    print("Switch to the Microsoft Edge window with WhatsApp Web after pressing Enter.")
    input("Press Enter when ready to proceed...")
    
    # Give user 5 seconds to switch to the correct window
    print("Switch to the Microsoft Edge window with WhatsApp Web now...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Step 1: Press Ctrl+L to focus on the address bar, then type the WhatsApp Web URL
    # This ensures we're on the right page
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    pyautogui.typewrite('https://web.whatsapp.com')
    pyautogui.press('enter')
    time.sleep(5)  # Wait for page to load
    
    # Step 2: Use the search box to find the contact
    # The search box in WhatsApp Web typically has a placeholder like "Search or start new chat"
    # We'll use keyboard shortcuts to navigate
    pyautogui.hotkey('ctrl', 'shift', '/')  # This shortcut focuses the search box in WhatsApp Web
    time.sleep(1)
    
    # If the above shortcut doesn't work, try pressing the search icon position
    # Typically, the search icon is on the left side of the screen
    # Let's try typing the contact name directly
    pyautogui.typewrite(contact_name)
    time.sleep(2)
    
    # Step 3: Select the contact from the search results
    # Usually the first result is selected by default, press Enter to select
    pyautogui.press('enter')
    time.sleep(2)
    
    # Step 4: Type the message in the message box
    pyautogui.typewrite(message)
    
    # Step 5: Press Enter to send the message
    pyautogui.press('enter')
    
    print(f"Message '{message}' sent to {contact_name}!")

def open_whatsapp_web():
    """
    Opens WhatsApp Web in Microsoft Edge
    """
    import os
    
    # Define possible Edge executable paths
    edge_paths = [
        "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",  # Windows x86
        "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",       # Windows x64
    ]
    
    # Check if any Edge executable exists
    edge_executable = None
    for path in edge_paths:
        if os.path.exists(path):
            edge_executable = path
            break
    
    if edge_executable:
        # Open with Microsoft Edge
        subprocess.run([
            "start", "msedge", "https://web.whatsapp.com"
        ], shell=True)
    else:
        # Fallback to default browser
        webbrowser.open('https://web.whatsapp.com')

if __name__ == "__main__":
    # Default values
    contact_name = "Zahra Ji"
    message = "hello"
    
    # Allow command-line arguments to override defaults
    if len(sys.argv) >= 2:
        contact_name = sys.argv[1]
    if len(sys.argv) >= 3:
        message = sys.argv[2]
    
    # Check if pyautogui is installed
    try:
        import pyautogui
    except ImportError:
        print("pyautogui is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
        import pyautogui
    
    # Inform user about the process
    print("This script will send a message using your existing WhatsApp Web session.")
    print("Make sure Microsoft Edge with WhatsApp Web is accessible.")
    
    # Ask if WhatsApp Web is already open
    whatsapp_open = input("Is WhatsApp Web already open in Microsoft Edge? (y/n): ").lower() == 'y'
    
    if not whatsapp_open:
        print("Opening WhatsApp Web in Microsoft Edge...")
        open_whatsapp_web()
        input("Please log in to WhatsApp Web if needed, then press Enter to continue...")
    
    # Send the message
    send_message_existing_session(contact_name, message)
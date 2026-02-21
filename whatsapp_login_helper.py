#!/usr/bin/env python3
"""
Helper script to initiate WhatsApp Web login process
"""
import webbrowser
import time
from pathlib import Path

def initiate_login():
    print("Opening WhatsApp Web in your default browser...")
    print("Please follow these steps to log in:")
    print("1. When the page opens, you'll see a QR code")
    print("2. Open WhatsApp on your phone")
    print("3. Tap on 'Settings' > 'Linked Devices' or 'WhatsApp Web/Desktop'")
    print("4. Point your phone camera at the QR code on screen")
    print("5. Once scanned, you'll be logged in to WhatsApp Web")
    print("6. Come back here and press Enter after successful login")
    
    # Open WhatsApp Web
    webbrowser.open('https://web.whatsapp.com')
    
    input("\nPress Enter after you've successfully logged in to WhatsApp Web...")

    print("\nYou're now ready to use the WhatsApp messaging features!")
    print("The session will be remembered for future use.")
    print("\nYou can now run:")
    print("python send_whatsapp_message.py 'contact name' 'message'")

if __name__ == "__main__":
    initiate_login()
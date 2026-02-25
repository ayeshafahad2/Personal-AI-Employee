#!/usr/bin/env python3
"""
Send WhatsApp to Fahad - Quick Sender
Opens WhatsApp with pre-filled message for Fahad
"""

import urllib.parse
import webbrowser

# Fahad's number
FAHAD_NUMBER = "923298374240"

print("=" * 70)
print("  SEND WHATSAPP TO FAHAD")
print("=" * 70)

message = input("\n  Your message to Fahad: ").strip()

if not message:
    print("\n  No message entered.")
    exit(1)

# Create WhatsApp URL
encoded_message = urllib.parse.quote(message)
whatsapp_url = f"https://wa.me/{FAHAD_NUMBER}?text={encoded_message}"

print(f"\n  Opening WhatsApp with message...")
print(f"  To: +{FAHAD_NUMBER}")
print(f"  Message: {message}")

# Open in Chrome
webbrowser.open(whatsapp_url)

print("\n" + "=" * 70)
print("  WHATSAPP OPENED")
print("=" * 70)
print("""
  INSTRUCTIONS:
  
  1. WhatsApp Web will open with Fahad's chat (or search for him)
  2. Your message is pre-filled in the text box
  3. Click the send button (paper plane icon)
  4. Message sent to Fahad!
  
  If this is your first time:
  - Scan QR code with your phone
  - WhatsApp will connect
  - Then send message
  
""")
print("=" * 70)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Send WhatsApp Message to Fahad about LinkedIn Post
Opens WhatsApp Web with pre-filled message
"""

import sys
import codecs
import webbrowser
import pyperclip
import time

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("  📱 WHATSAPP - MESSAGE TO FAHAD")
print("=" * 70)

# Message content about LinkedIn post
MESSAGE = """Assalamu Alaikum Fahad! 🌙

I've just posted on LinkedIn about the blessed month of Ramadan.

📝 Post: "Embracing the Blessed Month: A Time for Reflection & Renewal"

The post shares key lessons from Ramadan:
✨ Mindful Awareness
✨ Self-Discipline  
✨ Empathy & Gratitude
✨ Community Bond
✨ Digital Detox

🔗 LinkedIn Post Link:
https://www.linkedin.com/feed/

Please check it out when you get a chance!

Ramadan Mubarak! 🌙
#Ramadan #Ramadan2026 #SpiritualGrowth #Mindfulness"""

# Copy message to clipboard
print("\n📋 Copying message to clipboard...")
pyperclip.copy(MESSAGE)
print("   ✓ Message copied!")

# Fahad's number (from your .env: +923298374240)
fahad_number = "923298374240"

# WhatsApp Web URL with Fahad's number
whatsapp_url = f"https://web.whatsapp.com/send?phone={fahad_number}"

print(f"\n📱 Opening WhatsApp Web for Fahad ({fahad_number})...")
webbrowser.open(whatsapp_url)

print("\n" + "=" * 70)
print("  ✅ WHATSAPP IS OPEN!")
print("=" * 70)
print("""
  The message to Fahad is IN YOUR CLIPBOARD!
  
  Steps:
  1. WhatsApp Web is opening
  2. Wait for chat with Fahad to load
  3. Press Ctrl+V (paste the message)
  4. Press Enter to send
  
  The message includes:
  - Greeting
  - LinkedIn post announcement
  - Post summary
  - LinkedIn link
  - Ramadan wishes
""")
print("=" * 70)

# Keep browser open for 5 minutes
print("\n⏰ Browser stays open for 5 minutes (300 seconds)...")
print("   Take your time to send the message!\n")

for i in range(300, 0, -10):
    if i % 60 == 0:
        print(f"   ⏱️  {i//60} minute(s) remaining...")
    time.sleep(10)

print("\n\n✓ Done!")
print("\n🌙 Ramadan Mubarak!")

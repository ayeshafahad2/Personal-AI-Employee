#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facebook Post - Simple Clipboard Method
Opens Facebook and copies content to clipboard
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
print("  📘 FACEBOOK POST - RAMADAN MESSAGE")
print("=" * 70)

# Same content as LinkedIn
RAMADAN_POST = """🌙 Embracing the Blessed Month: A Time for Reflection & Renewal

As we welcome the holy month of Ramadan, millions around the world embark on a profound journey of spiritual growth, self-discipline, and community connection.

This sacred month teaches us powerful lessons that extend far beyond fasting:

✨ Mindful Awareness - Conscious eating and drinking reminds us to be intentional in all aspects of life

✨ Self-Discipline - The daily practice of restraint builds mental strength and willpower

✨ Empathy & Gratitude - Experiencing hunger fosters compassion for those less fortunate

✨ Community Bond - Breaking fast together strengthens family and community ties

✨ Digital Detox - A natural opportunity to reduce screen time and focus on what truly matters

In our hyper-connected world, Ramadan offers a unique pause—a chance to reset our priorities, purify your intentions, and reconnect with our core values.

Whether you're observing or simply supporting those who are, may this month bring:
🕊️ Peace to your heart
🤝 Unity to your community
💡 Clarity to your mind
🌟 Blessings to your life

Ramadan Mubarak to all who are celebrating! 🌙

#Ramadan #Ramadan2026 #SpiritualGrowth #Mindfulness #Community #Gratitude #SelfDiscipline #Reflection #BlessedMonth #RamadanKareem #PeaceAndUnity #DigitalWellbeing"""

# Copy to clipboard
print("\n📋 Copying post content to clipboard...")
pyperclip.copy(RAMADAN_POST)
print("   ✓ Content copied to clipboard!")

# Save to file as backup
with open('facebook_post_content.txt', 'w', encoding='utf-8') as f:
    f.write(RAMADAN_POST)
print("   ✓ Also saved to: facebook_post_content.txt")

# Open Facebook
print("\n🌐 Opening Facebook...")
webbrowser.open('https://www.facebook.com/')

print("\n" + "=" * 70)
print("  ✅ READY TO POST ON FACEBOOK!")
print("=" * 70)
print("""
  The Ramadan post is IN YOUR CLIPBOARD!
  
  Simple Steps:
  1. Facebook is opening in your browser
  2. Login if needed
  3. Click "What's on your mind?" at the top
  4. Press Ctrl+V (paste)
  5. Click "Post"
  
  Same content as LinkedIn! ✨
""")
print("=" * 70)
print("\n📄 Or open file: facebook_post_content.txt")
print("   Copy all, paste to Facebook, and post!")
print("\n🌙 Ramadan Mubarak!")

# Keep script running
print("\n⏰ Keeping this window open for 5 minutes...")
print("   (Content stays in clipboard)\n")

for i in range(300, 0, -10):
    if i % 60 == 0:
        print(f"   ⏱️  {i//60} minute(s) remaining...")
    time.sleep(10)

print("\n✓ Done!")

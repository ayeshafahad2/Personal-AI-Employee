#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Auto-Poster with 5 Minute Browser Session
Copies content to clipboard and keeps LinkedIn open for 5 minutes
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
print("  🌙 LINKEDIN RAMADAN POST - 5 MINUTE SESSION")
print("=" * 70)

# Ramadan post content
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

# Open LinkedIn
print("\n🌐 Opening LinkedIn...")
webbrowser.open('https://www.linkedin.com/feed/')

print("\n" + "=" * 70)
print("  ✅ BROWSER WILL STAY OPEN FOR 5 MINUTES")
print("=" * 70)
print("""
  The Ramadan post is NOW IN YOUR CLIPBOARD!
  
  You have 5 minutes to:
  1. Login to LinkedIn (if needed)
  2. Click "Start a post"
  3. Press Ctrl+V (paste the content)
  4. Review the post
  5. Click "Post" button
  
  Take your time - browser stays open for 5 minutes! ⏰
""")
print("=" * 70)

# Keep script running for 5 minutes (300 seconds)
print("\n⏰ Timer started: 5 minutes (300 seconds)")
print("   Browser will remain accessible...")

for i in range(300, 0, -10):
    if i % 60 == 0:
        print(f"   ⏱️  {i//60} minute(s) remaining...")
    time.sleep(10)

print("\n\n" + "=" * 70)
print("  ⏰ Time's up!")
print("=" * 70)
print("\n  If you haven't posted yet:")
print("  1. Run: python linkedin_post_clipboard.py")
print("  2. Or manually copy from: ramadan_post_ready.txt")
print("\n🌙 Ramadan Mubarak!")

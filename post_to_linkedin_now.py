#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick LinkedIn Post Opener
Opens LinkedIn and displays post content for easy copy-paste
"""

import webbrowser
import sys
import codecs

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("  LINKEDIN POST - RAMADAN BLESSED MONTH")
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

In our hyper-connected world, Ramadan offers a unique pause—a chance to reset our priorities, purify our intentions, and reconnect with our core values.

Whether you're observing or simply supporting those who are, may this month bring:
🕊️ Peace to your heart
🤝 Unity to your community
💡 Clarity to your mind
🌟 Blessings to your life

Ramadan Mubarak to all who are celebrating! 🌙

#Ramadan #Ramadan2026 #SpiritualGrowth #Mindfulness #Community #Gratitude #SelfDiscipline #Reflection #BlessedMonth #RamadanKareem #PeaceAndUnity #DigitalWellbeing"""

# Open LinkedIn feed
print("\n[1/3] Opening LinkedIn...")
webbrowser.open('https://www.linkedin.com/feed/')

# Open LinkedIn post composer in new tab
print("[2/3] Opening post composer...")
webbrowser.open('https://www.linkedin.com/feed/?shareActive=true')

# Save post to clipboard file
import pathlib
post_file = pathlib.Path('ramadan_post_content.txt')
with open(post_file, 'w', encoding='utf-8') as f:
    f.write(RAMADAN_POST)

print("[3/3] Post content saved to: ramadan_post_content.txt")

print("\n" + "=" * 70)
print("  ✅ LINKEDIN IS NOW OPEN!")
print("=" * 70)
print("\n  Two tabs opened:")
print("  1. LinkedIn Feed")
print("  2. LinkedIn Post Composer")
print("\n" + "=" * 70)
print("  TO POST:")
print("=" * 70)
print("""
  1. Switch to the LinkedIn tab
  2. Click "Start a post" (if not already open)
  3. Copy the text below (or from ramadan_post_content.txt)
  4. Paste into LinkedIn
  5. Click "Post"

""")

print("=" * 70)
print("  POST CONTENT (COPY THIS):")
print("=" * 70)
print(RAMADAN_POST)
print("=" * 70)

print("\n  ✨ Or simply open: ramadan_post_content.txt")
print("  Copy all, paste to LinkedIn, and post!")
print("\n  🌙 Ramadan Mubarak!")

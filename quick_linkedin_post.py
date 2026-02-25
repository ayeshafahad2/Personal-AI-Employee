#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple LinkedIn Post Helper
Opens LinkedIn with post content ready to paste
"""

import webbrowser
import sys
import codecs

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("  🌙 LINKEDIN RAMADAN POST - QUICK POSTER")
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

# Save post to a simple text file
with open('ramadan_post_ready.txt', 'w', encoding='utf-8') as f:
    f.write(RAMADAN_POST)

print("\n✅ Post content saved to: ramadan_post_ready.txt")

# Open LinkedIn
print("\n🌐 Opening LinkedIn...")
webbrowser.open('https://www.linkedin.com/feed/')

# Open the text file
print("📄 Opening post content file...")
webbrowser.open('ramadan_post_ready.txt')

print("\n" + "=" * 70)
print("  ✨ READY TO POST IN 3 SIMPLE STEPS")
print("=" * 70)
print("""
  1. In the text file window: Press Ctrl+A, then Ctrl+C (copy all)
  
  2. In LinkedIn: Click "Start a post", then Ctrl+V (paste)
  
  3. Click the blue "Post" button
  
  That's it! 🎉
""")

print("=" * 70)
print("  OR use this direct link:")
print("  https://www.linkedin.com/feed/?shareActive=true")
print("=" * 70)

print("\n🌙 Ramadan Mubarak! May your message inspire many!")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open LinkedIn for Posting Ramadan Message
"""

import webbrowser
import sys
import codecs

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# LinkedIn post URL
LINKEDIN_FEED = "https://www.linkedin.com/feed/"

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

print("=" * 70)
print("  🌙 OPENING LINKEDIN FOR RAMADAN POST")
print("=" * 70)

# Open LinkedIn in browser
print(f"\nOpening: {LINKEDIN_FEED}")
webbrowser.open(LINKEDIN_FEED)

print("\n✅ LinkedIn opened in your browser!")
print("\n" + "=" * 70)
print("  NEXT STEPS:")
print("=" * 70)
print("""
1. LinkedIn should now be open in your browser
2. Click "Start a post" at the top of your feed
3. Copy the post content below
4. Paste it into LinkedIn
5. Click "Post"

""")

print("=" * 70)
print("  COPY THIS POST CONTENT:")
print("=" * 70)
print(RAMADAN_POST)
print("=" * 70)

print("\n💡 Tip: The post content is also saved in:")
print("   - LINKEDIN_RAMADAN_POST_READY.md")
print("   - ramadan_linkedin_post.md")
print("\n🌙 Ramadan Mubarak!")

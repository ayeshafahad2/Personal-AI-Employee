#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Send Email about LinkedIn Post with Sehri & Iftar Update
Opens Gmail with pre-filled email to ayeshafahad661@gmail.com
"""

import sys
import codecs
import webbrowser
import pyperclip
import time
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("  📧 GMAIL - EMAIL ABOUT LINKEDIN POST")
print("=" * 70)

# Get today's date
today = datetime.now().strftime("%B %d, %Y")

# Email content
SUBJECT = f"🌙 Ramadan Mubarak! LinkedIn Post + Sehri & Iftar Time Update"

EMAIL_BODY = f"""Assalamu Alaikum! 🌙

Ramadan Mubarak to you and your family!

I wanted to share that I've posted on LinkedIn about the blessed month of Ramadan.

📝 LINKEDIN POST:
"Embracing the Blessed Month: A Time for Reflection & Renewal"

The post highlights key lessons from Ramadan:
✨ Mindful Awareness
✨ Self-Discipline
✨ Empathy & Gratitude
✨ Community Bond
✨ Digital Detox

🔗 View the post here:
https://www.linkedin.com/feed/

---

⏰ IMPORTANT UPDATE - SEHRI & IFTAR TIMES:

Please note that Sehri and Iftar times will be 10 minutes EARLIER starting tomorrow.

🌅 SEHRI: Ends 10 minutes earlier than previous schedule
🌇 IFTAR: Begins 10 minutes earlier than previous schedule

Please adjust your schedules accordingly and ensure you're prepared for the updated timings.

---

May this blessed month bring peace, happiness, and prosperity to you and your loved ones.

Ramadan Kareem! 🌙

Best regards,
Your AI Employee

---
Sent on: {today}
"""

# Copy email content to clipboard
print("\n📋 Copying email content to clipboard...")
pyperclip.copy(EMAIL_BODY)
print("   ✓ Email content copied!")

# Copy subject to clipboard (separate)
pyperclip.copy(SUBJECT)
print("   ✓ Email subject copied!")

# Open Gmail compose with recipient
recipient = "ayeshafahad661@gmail.com"
gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient}&su={SUBJECT.replace(' ', '%20')}"

print(f"\n📧 Opening Gmail compose to: {recipient}")
webbrowser.open(gmail_url)

print("\n" + "=" * 70)
print("  ✅ GMAIL IS OPEN!")
print("=" * 70)
print("""
  Email content is IN YOUR CLIPBOARD!
  
  Steps:
  1. Gmail compose window is opening
  2. To: ayeshafahad661@gmail.com (already filled)
  3. Subject: Ramadan Mubarak! LinkedIn Post + Sehri & Iftar Update
  4. Press Ctrl+V to paste the email body
  5. Click "Send"
  
  Email includes:
  ✓ Ramadan greeting
  ✓ LinkedIn post announcement
  ✓ Post link
  ✓ Sehri & Iftar time update (10 mins earlier)
  ✓ Ramadan wishes
""")
print("=" * 70)

# Keep browser open for 5 minutes
print("\n⏰ Browser stays open for 5 minutes (300 seconds)...")
print("   Take your time to review and send!\n")

for i in range(300, 0, -10):
    if i % 60 == 0:
        print(f"   ⏱️  {i//60} minute(s) remaining...")
    time.sleep(10)

print("\n\n✓ Done!")
print("\n🌙 Ramadan Mubarak!")

#!/usr/bin/env python3
"""
Facebook AUTO POST - Simple Selenium
Uses your existing Chrome profile where you're logged in
"""

import sys
import io
import time
import os
from pathlib import Path

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

print("=" * 70)
print("  FACEBOOK AUTO POST - Simple Selenium")
print("=" * 70)

post = """The Future of Work is Here!

Human intelligence + AI tools = Unstoppable combination.

While AI handles routine tasks, humans excel at:
- Creative problem-solving
- Strategic thinking
- Building relationships
- Innovation

The question isn't IF you'll use AI.
It's WHEN you'll start.

#FutureOfWork #AI #Innovation #Productivity #DigitalTransformation"""

profile_url = "https://www.facebook.com/profile.php?id=61576154677449"

print("\n  Posting to Facebook:")
print("-" * 70)
print(post)
print("-" * 70)

# Use your existing Chrome profile
chrome_data_path = str(Path.home() / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data')

print("\n[1/4] Starting Chrome with your profile...")
options = webdriver.ChromeOptions()
options.add_argument(f'--user-data-dir={chrome_data_path}')
options.add_argument('--profile-directory=Default')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    driver = webdriver.Chrome(options=options)
    print("      Chrome started!")
except Exception as e:
    print(f"      Error: {e}")
    print("      Make sure Chrome is not running, or close it first")
    sys.exit(1)

driver.maximize_window()

print("[2/4] Opening your Facebook profile...")
driver.get(profile_url)
print("      Waiting 15 seconds for page load...")
time.sleep(15)

print("[3/4] Entering post content...")
try:
    # Find body and navigate to composer
    body = driver.find_element(By.TAG_NAME, 'body')
    
    # Press Escape to ensure not in URL bar
    body.send_keys(Keys.ESCAPE)
    time.sleep(1)
    
    # Tab to reach composer
    for i in range(6):
        body.send_keys(Keys.TAB)
        time.sleep(0.3)
    
    # Press Enter to activate
    body.send_keys(Keys.ENTER)
    time.sleep(3)
    
    # Clear and type
    body.send_keys(Keys.CONTROL + "a")
    time.sleep(0.5)
    body.send_keys(Keys.DELETE)
    time.sleep(0.5)
    
    # Type post slowly
    for char in post:
        body.send_keys(char)
        time.sleep(0.02)
    
    print("      Content entered!")
    time.sleep(3)
    
except Exception as e:
    print(f"      Error: {e}")

print("[4/4] Clicking POST...")
try:
    body = driver.find_element(By.TAG_NAME, 'body')
    
    # Tab to Post button
    for i in range(15):
        body.send_keys(Keys.TAB)
        time.sleep(0.2)
    
    # Press Enter to click Post
    body.send_keys(Keys.ENTER)
    print("      POST clicked!")
    time.sleep(5)
    
except Exception as e:
    print(f"      Error: {e}")

print("\n" + "=" * 70)
print("  COMPLETE!")
print("=" * 70)
print("\n  Check your profile:")
print("  https://www.facebook.com/profile.php?id=61576154677449")
print("\n  Browser stays open for you to verify.")
print("=" * 70)

time.sleep(10)

#!/usr/bin/env python3
"""
Facebook PROFESSIONAL AUTO POST - Selenium WebDriver
Reliable automation using proper browser interaction
Posts to your profile: https://www.facebook.com/profile.php?id=61576154677449
"""

import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("  FACEBOOK AUTO POST - Selenium WebDriver")
print("  Professional & Reliable Automation")
print("=" * 70)

# Professional post content
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

print("\n  Content to post:")
print("-" * 70)
print(post)
print("-" * 70)

print("\n[1/5] Starting Chrome browser...")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

print("[2/5] Opening Facebook profile...")
driver.get(profile_url)
print("      Waiting for page to load (20 seconds)...")
time.sleep(20)

print("[3/5] Finding post composer...")
try:
    # Try multiple selectors for the post composer
    composer = None
    selectors = [
        '[aria-label*="What"]',
        'div[role="button"]',
        '[data-testid="create_post"]',
        'button',
    ]
    
    for selector in selectors:
        try:
            composer = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            print(f"      Found with selector: {selector}")
            break
        except:
            continue
    
    if composer:
        composer.click()
        print("      Composer clicked!")
    else:
        print("      Using keyboard navigation...")
        driver.find_element(By.TAG_NAME, 'body').click()
        for _ in range(5):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ENTER)
    
    time.sleep(3)
    
except Exception as e:
    print(f"      Error: {e}")
    print("      Trying alternative method...")
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB * 5)
    time.sleep(2)

print("[4/5] Entering content...")
try:
    # Find the textarea or input field
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.CONTROL + "a")
    time.sleep(0.5)
    body.send_keys(Keys.DELETE)
    time.sleep(0.5)
    body.send_keys(post)
    print("      Content entered!")
    time.sleep(3)
except Exception as e:
    print(f"      Error entering content: {e}")

print("[5/5] Clicking POST button...")
try:
    # Try to find and click the Post button
    post_selectors = [
        '[aria-label="Post"]',
        'button[type="submit"]',
        '[data-testid="react-composer-post-button"]',
        'div[role="button"]',
    ]
    
    for selector in post_selectors:
        try:
            post_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            post_btn.click()
            print("      POST CLICKED!")
            break
        except:
            continue
    else:
        # Fallback: Use keyboard
        print("      Using keyboard to post...")
        body.send_keys(Keys.TAB * 10)
        time.sleep(1)
        body.send_keys(Keys.ENTER)
        
except Exception as e:
    print(f"      Error clicking post: {e}")

print("\n" + "=" * 70)
print("  COMPLETE!")
print("=" * 70)
print("""
  Check your profile to verify the post:
  https://www.facebook.com/profile.php?id=61576154677449
  
  The browser will stay open for you to verify.
""")
print("=" * 70)

# Keep browser open
time.sleep(10)

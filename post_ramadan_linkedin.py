#!/usr/bin/env python3
"""
Post Ramadan Message to LinkedIn

Professional post about the blessed month of Ramadan
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment variables
load_dotenv()

# Ramadan post content
RAMADAN_POST = """
🌙 Embracing the Blessed Month: A Time for Reflection & Renewal

As we welcome the holy month of Ramadan, millions around the world embark on a profound journey of spiritual growth, self-discipline, and community connection.

This sacred month teaches us powerful lessons that extend far beyond fasting:

✨ **Mindful Awareness** - Conscious eating and drinking reminds us to be intentional in all aspects of life

✨ **Self-Discipline** - The daily practice of restraint builds mental strength and willpower

✨ **Empathy & Gratitude** - Experiencing hunger fosters compassion for those less fortunate

✨ **Community Bond** - Breaking fast together strengthens family and community ties

✨ **Digital Detox** - A natural opportunity to reduce screen time and focus on what truly matters

In our hyper-connected world, Ramadan offers a unique pause—a chance to reset our priorities, purify our intentions, and reconnect with our core values.

Whether you're observing or simply supporting those who are, may this month bring:
🕊️ Peace to your heart
🤝 Unity to your community
💡 Clarity to your mind
🌟 Blessings to your life

Ramadan Mubarak to all who are celebrating! 🌙

#Ramadan #Ramadan2026 #SpiritualGrowth #Mindfulness #Community #Gratitude #SelfDiscipline #Reflection #BlessedMonth #RamadanKareem #PeaceAndUnity #DigitalWellbeing
"""


class LinkedInPoster:
    """Post to LinkedIn using API"""
    
    def __init__(self):
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        
        if not self.access_token:
            raise ValueError("LINKEDIN_ACCESS_TOKEN not found in .env")
        
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
    
    def get_person_urn(self):
        """Get the person URN for authenticated user"""
        try:
            response = requests.get(
                f"{self.base_url}/me",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            person_urn = data.get('id')
            print(f"✓ Person URN: {person_urn}")
            return person_urn
        except Exception as e:
            print(f"✗ Error getting person URN: {e}")
            return None
    
    def post_to_linkedin(self, text: str):
        """Publish post to LinkedIn"""
        person_urn = self.get_person_urn()
        
        if not person_urn:
            print("✗ Could not get person URN. Posting failed.")
            return False
        
        # Prepare payload
        payload = {
            "author": f"urn:li:person:{person_urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text.strip()
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            print("\n📤 Posting to LinkedIn...")
            print(f"   Post length: {len(text)} characters")
            
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            
            # Get post ID from response
            post_id = response.json().get('id', 'Unknown')
            
            print("\n✅ SUCCESS! Post published to LinkedIn")
            print(f"   Post ID: {post_id}")
            print(f"   URL: https://www.linkedin.com/feed/update/{post_id}")
            print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Log the post
            self.log_post(text, post_id)
            
            return True
            
        except requests.exceptions.HTTPError as e:
            print(f"\n✗ HTTP Error: {e}")
            print(f"   Status Code: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
            return False
        except Exception as e:
            print(f"\n✗ Error posting to LinkedIn: {e}")
            return False
    
    def log_post(self, content: str, post_id: str):
        """Log post to vault"""
        log_dir = Path("AI_Employee_Vault/Social_Media/LinkedIn")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": "LinkedIn",
            "post_id": post_id,
            "content": content,
            "status": "published",
            "topic": "Ramadan"
        }
        
        # Append to log file
        log_file = log_dir / "ramadan_posts.json"
        
        import json
        posts = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    posts = json.load(f)
            except:
                posts = []
        
        posts.append(log_entry)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        
        print(f"\n📝 Post logged to: {log_file}")


def main():
    """Main function"""
    print("=" * 60)
    print("🌙 LinkedIn Post: Blessed Month of Ramadan")
    print("=" * 60)
    print()
    
    # Show post preview
    print("📝 Post Preview:")
    print("-" * 60)
    print(RAMADAN_POST.strip()[:500] + "...")
    print("-" * 60)
    print()
    
    # Auto-confirm for non-interactive mode
    print("\n🚀 Posting to LinkedIn automatically...")
    
    # Post to LinkedIn
    poster = LinkedInPoster()
    success = poster.post_to_linkedin(RAMADAN_POST)
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Ramadan post successfully published to LinkedIn!")
        print("   May your message reach many hearts. 🌙")
    else:
        print("✗ Posting failed. Please check credentials and try again.")
    print("=" * 60)


if __name__ == "__main__":
    main()

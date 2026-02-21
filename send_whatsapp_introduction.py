#!/usr/bin/env python3
"""
Send a WhatsApp message to a contact
"""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.whatsapp_watcher import WhatsAppWatcher

def send_introduction_message(contact_name: str = "haanz"):
    # Use a test vault path
    vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'
    
    # Initialize the WhatsApp watcher
    watcher = WhatsAppWatcher(str(vault_path))
    
    # Introduction message
    message = """Hello! 👋

I'm your Personal AI Employee - an intelligent digital assistant that works 24/7 to help manage your communications and tasks.

I'm powered by Claude Code and can:
✅ Monitor your Gmail, WhatsApp, and LinkedIn for important messages
✅ Automatically process routine communications
✅ Create action items and plans for you
✅ Generate weekly CEO briefings with insights
✅ Handle tasks autonomously within your defined rules

I just completed my WhatsApp setup and I'm ready to assist you! Feel free to send me any urgent or important messages, and I'll make sure they get the attention they deserve.

How can I help you today? 🚀"""

    print(f"Sending message to {contact_name}...")
    success = watcher.send_message(contact_name, message)
    
    if success:
        print(f"\n[OK] Message sent successfully to {contact_name}!")
        print("\nMessage content:")
        print("-" * 60)
        print(message)
        print("-" * 60)
    else:
        print(f"\n[ERROR] Failed to send message to {contact_name}")
        print("\nPossible reasons:")
        print("1. Contact 'haanz' not found in your WhatsApp contacts")
        print("2. WhatsApp Web session not properly logged in")
        print("3. Network connectivity issues")
        print("\nPlease ensure:")
        print("- You're logged in to WhatsApp Web")
        print("- The contact name matches exactly as it appears in WhatsApp")
        print("- You have a stable internet connection")
    
    return success

if __name__ == "__main__":
    contact = sys.argv[1] if len(sys.argv) > 1 else "haanz"
    success = send_introduction_message(contact)
    sys.exit(0 if success else 1)

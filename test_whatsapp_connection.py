#!/usr/bin/env python3
"""
Test script to verify WhatsApp connection and watcher functionality
"""
import sys
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.whatsapp_watcher import WhatsAppWatcher

def test_whatsapp_connection():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    # Use a test vault path
    vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault_Test'
    
    # Create the vault directory if it doesn't exist
    vault_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize the WhatsApp watcher
    watcher = WhatsAppWatcher(str(vault_path))
    
    logger.info("Testing WhatsApp connection...")
    logger.info("Please make sure you're logged in to WhatsApp Web in the browser that will open.")
    logger.info("If you're not logged in, scan the QR code when prompted.")
    
    try:
        # Perform a single check
        messages = watcher.check_for_updates()
        logger.info(f"Found {len(messages)} important messages")
        
        for message in messages:
            logger.info(f"Message from {message['sender']} in {message['chat_name']}: {message['text'][:50]}...")
            
            # Create action file for each message
            action_file = watcher.create_action_file(message)
            logger.info(f"Created action file: {action_file}")
        
        logger.info("WhatsApp connection test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error during WhatsApp connection test: {e}")
        return False

if __name__ == "__main__":
    success = test_whatsapp_connection()
    if success:
        print("\nWhatsApp connection test completed successfully!")
        print("The watcher is ready to monitor WhatsApp for important messages.")
    else:
        print("\nWhatsApp connection test failed!")
        print("Please ensure:")
        print("1. Playwright is properly installed")
        print("2. You are logged in to WhatsApp Web")
        print("3. Your browser is not blocking automated access")
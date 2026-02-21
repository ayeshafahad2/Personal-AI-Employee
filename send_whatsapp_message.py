#!/usr/bin/env python3
"""
Script to send a WhatsApp message to a specific contact
"""
import sys
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.whatsapp_watcher import WhatsAppWatcher

def send_whatsapp_message(contact_name, message, vault_path=None):
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    # Use provided vault path or default
    if vault_path is None:
        vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'
    
    # Create the vault directory if it doesn't exist
    vault_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize the WhatsApp watcher
    watcher = WhatsAppWatcher(str(vault_path))
    
    logger.info(f"Attempting to send message to {contact_name}: {message}")
    logger.info("Please make sure you're logged in to WhatsApp Web in the browser that will open.")
    logger.info("If you're not logged in, scan the QR code when prompted.")
    
    # Send the message
    success = watcher.send_message(contact_name, message)
    
    if success:
        logger.info(f"Message sent successfully to {contact_name}!")
        return True
    else:
        logger.error(f"Failed to send message to {contact_name}")
        return False

if __name__ == "__main__":
    # Default values
    contact_name = "zahra ji"
    message = "hello"
    
    # Allow command-line arguments to override defaults
    if len(sys.argv) >= 2:
        contact_name = sys.argv[1]
    if len(sys.argv) >= 3:
        message = sys.argv[2]
    
    # Use default vault path or from command line
    vault_path = None
    if len(sys.argv) >= 4:
        vault_path = Path(sys.argv[3])
    
    success = send_whatsapp_message(contact_name, message, vault_path)
    
    if success:
        print(f"\n[SUCCESS] Successfully sent message to {contact_name}: '{message}'")
    else:
        print(f"\n[ERROR] Failed to send message to {contact_name}")
        print("Please ensure:")
        print("1. Playwright is properly installed")
        print("2. You are logged in to WhatsApp Web")
        print("3. The contact name matches exactly as it appears in your contacts")
        print("4. Your browser is not blocking automated access")
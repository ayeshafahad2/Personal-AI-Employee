#!/usr/bin/env python3
"""
Script to run the WhatsApp Watcher in continuous mode
"""
import sys
from pathlib import Path
import logging

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.watchers.whatsapp_watcher import WhatsAppWatcher

def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    # Get vault path from command line argument or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        # Default vault path - adjust as needed
        vault_path = Path.home() / 'Documents' / 'AI_Employee_Vault'
        
    logger.info(f"Starting WhatsApp Watcher with vault path: {vault_path}")
    
    # Create the vault directory if it doesn't exist
    vault_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize the WhatsApp watcher
    watcher = WhatsAppWatcher(str(vault_path))
    
    logger.info("WhatsApp Watcher initialized. Starting in watcher mode...")
    logger.info("Please make sure you're logged in to WhatsApp Web in the browser that will open.")
    logger.info("If you're not logged in, scan the QR code when prompted.")
    
    try:
        # Run the watcher continuously
        watcher.run()
    except KeyboardInterrupt:
        logger.info("WhatsApp Watcher stopped by user.")
    except Exception as e:
        logger.error(f"Error running WhatsApp Watcher: {e}")
        raise

if __name__ == "__main__":
    main()
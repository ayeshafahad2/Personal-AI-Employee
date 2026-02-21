"""
Main Orchestrator for the Personal AI Employee
Coordinates between watchers, Claude Code, and MCP servers
"""
import time
import logging
import threading
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.watchers.gmail_watcher import GmailWatcher
from src.watchers.whatsapp_watcher import WhatsAppWatcher
from src.watchers.linkedin_watcher import LinkedInWatcher
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Orchestrator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action_dir = self.vault_path / 'Needs_Action'
        self.plans_dir = self.vault_path / 'Plans'
        self.done_dir = self.vault_path / 'Done'
        self.logs_dir = self.vault_path / 'Logs'
        self.pending_approval_dir = self.vault_path / 'Pending_Approval'
        
        # Create directories if they don't exist
        for directory in [self.needs_action_dir, self.plans_dir, self.done_dir, self.logs_dir, self.pending_approval_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs_dir / 'orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize watchers
        self.gmail_watcher = GmailWatcher(vault_path)

        # Conditionally initialize WhatsApp watcher based on Playwright availability
        try:
            from src.watchers.whatsapp_watcher import PLAYWRIGHT_AVAILABLE
            if PLAYWRIGHT_AVAILABLE:
                self.whatsapp_watcher = WhatsAppWatcher(vault_path)
            else:
                self.logger.warning("WhatsApp watcher is disabled due to missing Playwright dependency.")
                self.whatsapp_watcher = None
        except ImportError:
            self.logger.error("Could not import WhatsApp watcher.")
            self.whatsapp_watcher = None

        # Initialize LinkedIn watcher
        try:
            self.linkedin_watcher = LinkedInWatcher(vault_path)
        except Exception as e:
            self.logger.error(f"LinkedIn watcher failed to initialize: {e}")
            self.linkedin_watcher = None
        
        # Thread management
        self.threads = []
        self.running = True
    
    def monitor_needs_action(self):
        """Monitor the Needs_Action folder for new files"""
        self.logger.info("Starting Needs_Action folder monitoring...")
        
        while self.running:
            try:
                # Look for new files in Needs_Action folder
                for file_path in self.needs_action_dir.glob("*.md"):
                    if file_path.suffix == '.md':
                        self.process_new_file(file_path)
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Error monitoring Needs_Action folder: {e}")
                time.sleep(60)  # Wait longer if there's an error
    
    def process_new_file(self, file_path: Path):
        """Process a new file in the Needs_Action folder"""
        try:
            self.logger.info(f"Processing new file: {file_path.name}")
            
            # Move file to Plans directory to indicate it's being processed
            plan_file = self.plans_dir / file_path.name
            file_path.rename(plan_file)
            
            # Create a plan file that Claude will process
            with open(plan_file, 'r+', encoding='utf-8') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(f"# PLAN FOR: {file_path.stem}\n\n")
                f.write("## Task\n")
                f.write("Read the original request above and create a plan to address it.\n\n")
                f.write("## Steps\n")
                f.write("- [ ] Analyze the request\n")
                f.write("- [ ] Determine appropriate action\n")
                f.write("- [ ] Execute action or create approval request\n")
                f.write("- [ ] Update status\n\n")
                f.write("---\n\n")
                f.write(content)
            
            self.logger.info(f"Created plan for: {file_path.name}")
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path.name}: {e}")
    
    def start_watchers(self):
        """Start the watcher threads"""
        # Start Gmail watcher in a separate thread
        gmail_thread = threading.Thread(target=self.gmail_watcher.run, daemon=True)
        self.threads.append(gmail_thread)
        gmail_thread.start()

        # Start WhatsApp watcher in a separate thread (if available)
        if self.whatsapp_watcher is not None:
            whatsapp_thread = threading.Thread(target=self.whatsapp_watcher.run, daemon=True)
            self.threads.append(whatsapp_thread)
            whatsapp_thread.start()
        else:
            self.logger.warning("WhatsApp watcher not started due to missing dependency.")

        # Start LinkedIn watcher in a separate thread (if available)
        if self.linkedin_watcher is not None:
            linkedin_thread = threading.Thread(target=self.linkedin_watcher.run, daemon=True)
            self.threads.append(linkedin_thread)
            linkedin_thread.start()
        else:
            self.logger.warning("LinkedIn watcher not started.")

        # Start Needs_Action monitor in a separate thread
        monitor_thread = threading.Thread(target=self.monitor_needs_action, daemon=True)
        self.threads.append(monitor_thread)
        monitor_thread.start()

        self.logger.info("Available watchers started successfully")
    
    def run(self):
        """Main execution loop"""
        self.logger.info("Starting Personal AI Employee Orchestrator...")
        
        # Start all watchers
        self.start_watchers()
        
        try:
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Shutting down orchestrator...")
            self.running = False
        
        # Wait for all threads to finish
        for thread in self.threads:
            thread.join(timeout=5)
        
        self.logger.info("Orchestrator shutdown complete")


if __name__ == "__main__":
    # Example usage
    # Use the project's AI_Employee_Vault directory
    vault_path = Path(__file__).parent.parent.parent / 'AI_Employee_Vault'
    orchestrator = Orchestrator(str(vault_path))

    # Run the orchestrator
    orchestrator.run()
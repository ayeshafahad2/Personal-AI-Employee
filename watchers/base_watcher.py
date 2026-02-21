"""
Base Watcher Class - Foundation for all watcher scripts

All watchers follow this pattern to monitor inputs and create actionable files
for Claude Code to process.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
import json


class BaseWatcher(ABC):
    """Abstract base class for all watcher scripts"""
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize base watcher
        
        Args:
            vault_path: Path to Obsidian vault
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.in_progress = self.vault_path / 'In_Progress'
        self.logs_dir = self.vault_path / 'Logs'
        self.check_interval = check_interval
        
        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.in_progress.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Track processed items to avoid duplicates
        self.processed_ids = set()
        self._load_processed_ids()
    
    def _setup_logging(self):
        """Setup logging to file and console"""
        log_file = self.logs_dir / f'watcher_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _load_processed_ids(self):
        """Load previously processed IDs from state file"""
        state_file = self.logs_dir / f'{self.__class__.__name__}_state.json'
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    self.processed_ids = set(state.get('processed_ids', []))
            except Exception as e:
                self.logger.warning(f'Could not load state file: {e}')
    
    def _save_processed_ids(self):
        """Save processed IDs to state file"""
        state_file = self.logs_dir / f'{self.__class__.__name__}_state.json'
        try:
            with open(state_file, 'w') as f:
                json.dump({'processed_ids': list(self.processed_ids)}, f)
        except Exception as e:
            self.logger.error(f'Could not save state file: {e}')
    
    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process
        
        Returns:
            List of new items (each item should be a dict with relevant data)
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create a .md action file in Needs_Action folder
        
        Args:
            item: Item data from check_for_updates
            
        Returns:
            Path to created file
        """
        pass
    
    def run(self):
        """Main run loop - continuously monitor and create action files"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        
        while True:
            try:
                items = self.check_for_updates()
                
                if items:
                    self.logger.info(f'Found {len(items)} new item(s)')
                    
                for item in items:
                    try:
                        filepath = self.create_action_file(item)
                        self.logger.info(f'Created action file: {filepath.name}')
                    except Exception as e:
                        self.logger.error(f'Error creating action file: {e}')
                
                # Save state after each check
                self._save_processed_ids()
                
            except Exception as e:
                self.logger.error(f'Error in main loop: {e}')
            
            time.sleep(self.check_interval)
    
    def claim_item(self, item_id: str, agent_name: str) -> bool:
        """
        Claim an item for processing (move to In_Progress/<agent>/)
        
        Args:
            item_id: ID of item to claim
            agent_name: Name of agent claiming
            
        Returns:
            True if successfully claimed
        """
        agent_dir = self.in_progress / agent_name
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        # Find the file in Needs_Action
        for file in self.needs_action.glob(f'*{item_id}*'):
            dest = agent_dir / file.name
            try:
                file.rename(dest)
                self.logger.info(f'Claimed {file.name} for {agent_name}')
                return True
            except Exception as e:
                self.logger.error(f'Could not claim {file.name}: {e}')
                return False
        
        return False

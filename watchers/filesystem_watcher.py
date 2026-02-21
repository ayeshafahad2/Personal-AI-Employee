#!/usr/bin/env python3
"""
File System Watcher - Monitor a drop folder for new files

When files are added to the Inbox folder, creates action files
in Obsidian vault's /Needs_Action folder for Claude Code to process.

Uses watchdog library for efficient file system monitoring.
"""

import os
import sys
import time
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from watchers.base_watcher import BaseWatcher

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False
    print("WARNING: watchdog not installed. Run: pip install watchdog")

load_dotenv()


class DropFolderHandler(FileSystemEventHandler):
    """Handle file system events for the drop folder"""
    
    def __init__(self, watcher_instance):
        self.watcher = watcher_instance
        self.logger = watcher_instance.logger
    
    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return
        
        source_path = Path(event.src_path)
        
        # Skip hidden files and temp files
        if source_path.name.startswith('.') or source_path.suffix in ['.tmp', '.part', '.crdownload']:
            return
        
        # Wait a moment for file to finish writing
        time.sleep(0.5)
        
        self.logger.info(f"New file detected: {source_path.name}")
        self.watcher.process_new_file(source_path)


class FileSystemWatcher(BaseWatcher):
    """Watch a folder for new files and create action items"""
    
    def __init__(self, vault_path: str, inbox_path: str = None, check_interval: int = 5):
        """
        Initialize File System Watcher
        
        Args:
            vault_path: Path to Obsidian vault
            inbox_path: Path to inbox/drop folder (default: vault/Inbox)
            check_interval: Not used with watchdog (event-driven)
        """
        super().__init__(vault_path, check_interval=1)  # 1s, but watchdog is event-driven
        
        self.inbox_path = Path(inbox_path) if inbox_path else self.vault_path / 'Inbox'
        self.inbox_path.mkdir(parents=True, exist_ok=True)
        
        self.observer = None
        self.handler = None
        
        # File size threshold for processing (skip very large files)
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        
        # File types to prioritize
        self.priority_extensions = ['.pdf', '.doc', '.docx', '.txt', '.md', '.csv', '.xlsx']
    
    def start(self):
        """Start the file system observer"""
        if not HAS_WATCHDOG:
            self.logger.error("watchdog library not available")
            return False
        
        self.handler = DropFolderHandler(self)
        self.observer = Observer()
        self.observer.schedule(
            self.handler, 
            str(self.inbox_path), 
            recursive=False
        )
        
        try:
            self.observer.start()
            self.logger.info(f"Watching folder: {self.inbox_path}")
            return True
        except Exception as e:
            self.logger.error(f"Could not start observer: {e}")
            return False
    
    def stop(self):
        """Stop the file system observer"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.logger.info("File system watcher stopped")
    
    def process_new_file(self, source_path: Path):
        """
        Process a newly detected file
        
        Args:
            source_path: Path to the new file
        """
        try:
            # Check file size
            file_size = source_path.stat().st_size
            if file_size > self.max_file_size:
                self.logger.warning(f"File too large, skipping: {source_path.name} ({file_size} bytes)")
                return
            
            # Generate file hash for deduplication
            file_hash = self._calculate_hash(source_path)
            
            # Check if already processed
            if file_hash in self.processed_ids:
                self.logger.info(f"File already processed: {source_path.name}")
                return
            
            # Create action file
            action_file_path = self.create_action_file({
                'source_path': source_path,
                'file_hash': file_hash,
                'file_size': file_size
            })
            
            # Mark as processed
            self.processed_ids.add(file_hash)
            
            self.logger.info(f"Created action file: {action_file_path.name}")
            
        except Exception as e:
            self.logger.error(f"Error processing file {source_path.name}: {e}")
    
    def check_for_updates(self) -> list:
        """
        Check for new files (used by base class, but we use event-driven approach)
        
        This is called by the base run() method but we override it to return empty
        since we use event-driven monitoring.
        """
        return []
    
    def create_action_file(self, item) -> Path:
        """
        Create action file for a dropped file
        
        Args:
            item: Dict with source_path, file_hash, file_size
            
        Returns:
            Path to created file
        """
        source_path = item['source_path']
        file_hash = item['file_hash']
        file_size = item['file_size']
        
        # Determine priority
        is_priority = source_path.suffix.lower() in self.priority_extensions
        
        # Create action file content
        content = f'''---
type: file_drop
original_name: {source_path.name}
file_hash: {file_hash}
size: {self._format_size(file_size)}
size_bytes: {file_size}
received: {datetime.now().isoformat()}
priority: {"high" if is_priority else "normal"}
status: pending
---

## File Information

**Original Name:** {source_path.name}
**Size:** {self._format_size(file_size)}
**Location:** {source_path.absolute()}
**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


## File Content Preview

'''
        
        # Try to read text content for preview
        try:
            if source_path.suffix.lower() in ['.txt', '.md', '.csv', '.json', '.py', '.js']:
                with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                    preview = f.read(1000)  # First 1000 chars
                    content += f"```\n{preview}\n{'...' if len(preview) >= 1000 else ''}\n```\n\n"
            else:
                content += "_Binary file - cannot preview content_\n\n"
        except Exception as e:
            content += f"_Could not read file: {e}_\n\n"
        
        content += f'''
## Suggested Actions

- [ ] Review file content
- [ ] Process and take action
- [ ] Move to appropriate folder
- [ ] Archive after processing


## Processing Notes

_Add your notes here_


## Actions Taken

- [ ] File reviewed
- [ ] Action completed
- [ ] Moved to /Done folder
'''
        
        # Create filename
        safe_name = self._sanitize_filename(source_path.stem)
        filename = f'FILE_{file_hash[:8]}_{safe_name[:40]}.md'
        filepath = self.needs_action / filename
        
        # Write file
        filepath.write_text(content, encoding='utf-8')
        
        return filepath
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def _sanitize_filename(self, text) -> str:
        """Sanitize text for use in filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '_')
        return text.strip()
    
    def run(self):
        """Override run to use watchdog observer"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Inbox folder: {self.inbox_path}')
        
        if not self.start():
            self.logger.error("Failed to start watcher")
            return
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
            raise


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='File System Watcher for AI Employee')
    parser.add_argument('--vault', type=str, default='AI_Employee_Vault', help='Path to Obsidian vault')
    parser.add_argument('--inbox', type=str, help='Path to inbox folder (default: vault/Inbox)')
    
    args = parser.parse_args()
    
    vault_path = Path(args.vault).absolute()
    
    if not vault_path.exists():
        print(f"ERROR: Vault not found: {vault_path}")
        return
    
    inbox_path = Path(args.inbox).absolute() if args.inbox else vault_path / 'Inbox'
    
    print(f"Starting File System Watcher...")
    print(f"Vault: {vault_path}")
    print(f"Inbox: {inbox_path}")
    print("-" * 50)
    print(f"Drop files into: {inbox_path}")
    print("Press Ctrl+C to stop")
    
    if not HAS_WATCHDOG:
        print("\n⚠️  watchdog not installed. Run: pip install watchdog")
        return
    
    watcher = FileSystemWatcher(str(vault_path), str(inbox_path))
    
    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n\nStopping File System Watcher...")
        watcher.stop()


if __name__ == '__main__':
    main()

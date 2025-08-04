"""
File scanning module for FlagHunter
"""

import os
import mimetypes
from pathlib import Path

class FileScanner:
    def __init__(self, config):
        self.config = config
        
    def is_text_file(self, filepath):
        """Check if file is text-based"""
        try:
            mime_type, _ = mimetypes.guess_type(filepath)
            if mime_type and mime_type.startswith('text'):
                return True
                
            # Check by extension
            ext = Path(filepath).suffix.lower()
            return ext in self.config['file_extensions']
        except:
            return False
    
    def get_file_size(self, filepath):
        """Get file size"""
        try:
            return os.path.getsize(filepath)
        except:
            return 0
    
    def should_scan_file(self, filepath):
        """Determine if file should be scanned"""
        if not self.is_text_file(filepath):
            return False
            
        size = self.get_file_size(filepath)
        max_size = self.config.get('max_file_size', 10485760)  # 10MB default
        
        return size <= max_size

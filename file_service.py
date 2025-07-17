import os
import glob
from pathlib import Path
from typing import Optional
from config import config
from schemas import TechnicalSpec

class FileService:
    def __init__(self):
        self.specs_directory = Path(config.SPECS_DIRECTORY)
    
    def find_technical_spec(self, part_number: str) -> Optional[TechnicalSpec]:
        """
        Find technical specification file for a given part number.
        Returns TechnicalSpec object if found, None otherwise.
        """
        if not self.specs_directory.exists():
            return None
        
        # Search for files containing the part number
        search_pattern = f"*{part_number}*"
        matching_files = list(self.specs_directory.glob(search_pattern))
        
        if not matching_files:
            return None
        
        # Get the first matching file
        file_path = matching_files[0]
        
        # Get file information
        file_size = file_path.stat().st_size
        file_type = file_path.suffix.lower()
        
        # Create download URL (relative to API base) - URL encode the filename
        from urllib.parse import quote
        encoded_filename = quote(file_path.name)
        download_url = f"/api/files/download/{encoded_filename}"
        
        return TechnicalSpec(
            filename=file_path.name,
            file_path=str(file_path),
            file_size=file_size,
            file_type=file_type,
            download_url=download_url
        )
    
    def get_file_path(self, filename: str) -> Optional[Path]:
        """
        Get the full file path for a given filename.
        """
        file_path = self.specs_directory / filename
        
        if not file_path.exists() or not file_path.is_file():
            return None
        
        return file_path
    
    def get_file_content(self, filename: str) -> Optional[bytes]:
        """
        Get file content as bytes for download.
        """
        file_path = self.get_file_path(filename)
        
        if not file_path:
            return None
        
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return None
    
    def list_available_parts(self) -> list[str]:
        """
        List all available part numbers based on files in SPECS directory.
        """
        if not self.specs_directory.exists():
            return []
        
        parts = []
        for file_path in self.specs_directory.iterdir():
            if file_path.is_file():
                # Extract part number from filename
                filename = file_path.name
                # Look for PA-XXXXX pattern
                if 'PA-' in filename:
                    # Extract the part number
                    parts.append(filename)
        
        return parts 
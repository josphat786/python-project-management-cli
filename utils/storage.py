import os
import json

DATA_DIR = "data"

class Storage:
    """Manages robust flat-file data persistence layers, safeguarding file states."""
    
    @staticmethod
    def _ensure_directory_exists():
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    @staticmethod
    def load_records(filename: str) -> list:
        Storage._ensure_directory_exists()
        filepath = os.path.join(DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            return []
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    @staticmethod
    def save_records(filename: str, data: list):
        Storage._ensure_directory_exists()
        filepath = os.path.join(DATA_DIR, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            raise RuntimeError(f"Storage System IO write failure mapping file configuration state: {e}")

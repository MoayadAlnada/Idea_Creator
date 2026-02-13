import json
from pathlib import Path
from typing import List, Dict, Any
from config import MEMORY_FILE
from utils.logger import setup_logger

logger = setup_logger("memory")

class Memory:
    def __init__(self):
        self.file_path = MEMORY_FILE
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            return {
                "seen_urls": [],
                "successful_assets": [],
                "failed_assets": [],
                "learning_stats": {"total_scans": 0, "total_built": 0}
            }
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load memory: {e}")
            return {}

    def save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")

    def add_seen_url(self, url: str):
        if url not in self.data["seen_urls"]:
            self.data["seen_urls"].append(url)
            self.save()

    def is_url_seen(self, url: str) -> bool:
        return url in self.data["seen_urls"]

    def record_success(self, asset_title: str):
        self.data["successful_assets"].append(asset_title)
        self.data["learning_stats"]["total_built"] += 1
        self.save()

# Global instance
memory = Memory()

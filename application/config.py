from typing import List, Dict
import json
import os
from pathlib import Path

class Config:
    DEFAULT_CONFIG = {
        "topics": {
            "tech": [
                "Python Programming Tips",
                "Web Development Best Practices",
                "Data Science Fundamentals",
                "Machine Learning Basics",
                "Software Development Lifecycle",
                "Cloud Computing Essentials",
                "DevOps Practices",
                "Cybersecurity Basics",
                "AI and Ethics",
                "Tech Industry Trends"
            ],
            "productivity": [
                "Time Management Techniques",
                "Remote Work Best Practices",
                "Team Collaboration Tools",
                "Project Management Tips",
                "Work-Life Balance Strategies"
            ]
        },
        "tags": {
            "tech": ["programming", "technology", "development", "coding", "software"],
            "productivity": ["productivity", "work", "life", "balance", "management"]
        },
        "scheduling": {
            "daily": {
                "default_time": "09:00",
                "timezone": "UTC"
            },
            "weekly": {
                "default_day": "monday",
                "default_time": "10:00",
                "timezone": "UTC"
            }
        },
        "content": {
            "min_length": 1000,
            "max_length": 2000,
            "include_images": True,
            "seo_optimization": True
        }
    }

    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "config.json")
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from file or create default if not exists."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                self._save_config(self.DEFAULT_CONFIG)
                return self.DEFAULT_CONFIG
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.DEFAULT_CONFIG

    def _save_config(self, config: Dict):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_topics(self, category: str = None) -> List[str]:
        """Get topics for a specific category or all topics."""
        if category and category in self.config["topics"]:
            return self.config["topics"][category]
        return [topic for topics in self.config["topics"].values() for topic in topics]

    def get_tags(self, category: str = None) -> List[str]:
        """Get tags for a specific category or all tags."""
        if category and category in self.config["tags"]:
            return self.config["tags"][category]
        return [tag for tags in self.config["tags"].values() for tag in tags]

    def get_schedule_config(self, schedule_type: str) -> Dict:
        """Get scheduling configuration for a specific type."""
        return self.config["scheduling"].get(schedule_type, {})

    def get_content_config(self) -> Dict:
        """Get content generation configuration."""
        return self.config["content"]

    def add_topic(self, category: str, topic: str):
        """Add a new topic to a category."""
        if category not in self.config["topics"]:
            self.config["topics"][category] = []
        if topic not in self.config["topics"][category]:
            self.config["topics"][category].append(topic)
            self._save_config(self.config)

    def add_tag(self, category: str, tag: str):
        """Add a new tag to a category."""
        if category not in self.config["tags"]:
            self.config["tags"][category] = []
        if tag not in self.config["tags"][category]:
            self.config["tags"][category].append(tag)
            self._save_config(self.config) 
import schedule
import time
from datetime import datetime
import random
from typing import List, Optional, Dict
import logging
import re

from application.api.huggingface_client import HuggingFaceClient
from application.api.dev_client import DevtoClient
from application.models.content_gen import ContentGenerator
from application.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentQualityChecker:
    @staticmethod
    def check_content(content: str, config: Dict) -> bool:
        """Check if content meets quality standards."""
        # Check length
        content_length = len(content)
        if content_length < config["min_length"] or content_length > config["max_length"]:
            logger.warning(f"Content length {content_length} is outside allowed range")
            return False

        # Check for basic structure
        if not re.search(r'#\s+.+', content):  # Check for at least one heading
            logger.warning("Content missing headings")
            return False

        if not re.search(r'\n\n', content):  # Check for paragraphs
            logger.warning("Content missing proper paragraph structure")
            return False

        # Check for minimum number of sections
        sections = len(re.findall(r'#{2,3}\s+.+', content))
        if sections < 3:
            logger.warning("Content has insufficient sections")
            return False

        return True

class BlogScheduler:
    def __init__(self, hf_client: HuggingFaceClient, devto_client: DevtoClient):
        self.hf_client = hf_client
        self.devto_client = devto_client
        self.config = Config()
        self.quality_checker = ContentQualityChecker()

    def generate_and_publish(self, topic: Optional[str] = None, category: str = None) -> str:
        """Generate and publish a blog post."""
        try:
            if not topic:
                topics = self.config.get_topics(category)
                topic = random.choice(topics)
            
            logger.info(f"Generating blog post for topic: {topic}")
            prompt = ContentGenerator.build_prompt(topic)
            blog_content = self.hf_client.generate_blog_content(prompt)
            
            # Quality check
            content_config = self.config.get_content_config()
            if not self.quality_checker.check_content(blog_content, content_config):
                logger.error("Content quality check failed")
                raise ValueError("Generated content did not meet quality standards")
            
            # Get appropriate tags
            tags = self.config.get_tags(category or "tech")
            selected_tags = random.sample(tags, min(5, len(tags)))
            
            logger.info("Publishing to DEV.to...")
            url = self.devto_client.publish_post(
                title=topic,
                body_markdown=blog_content,
                tags=selected_tags
            )
            logger.info(f"✅ Blog posted successfully! 🔗 URL: {url}")
            return url
        except Exception as e:
            logger.error(f"Error in generate_and_publish: {str(e)}")
            raise

    def schedule_daily_post(self, hour: int = 9, minute: int = 0, category: str = None):
        """Schedule a daily blog post."""
        schedule_config = self.config.get_schedule_config("daily")
        if not hour and not minute:
            time_str = schedule_config["default_time"]
            hour, minute = map(int, time_str.split(":"))
        
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(
            self.generate_and_publish, category=category
        )
        logger.info(f"Scheduled daily post at {hour:02d}:{minute:02d}")

    def schedule_weekly_post(self, day: str = "monday", hour: int = 10, minute: int = 0, category: str = None):
        """Schedule a weekly blog post."""
        schedule_config = self.config.get_schedule_config("weekly")
        if not day:
            day = schedule_config["default_day"]
        if not hour and not minute:
            time_str = schedule_config["default_time"]
            hour, minute = map(int, time_str.split(":"))
        
        getattr(schedule.every(), day).at(f"{hour:02d}:{minute:02d}").do(
            self.generate_and_publish, category=category
        )
        logger.info(f"Scheduled weekly post every {day} at {hour:02d}:{minute:02d}")

    def run_scheduler(self):
        """Run the scheduler continuously."""
        logger.info("Starting blog scheduler...")
        while True:
            schedule.run_pending()
            time.sleep(60)

def create_scheduler(hf_client: HuggingFaceClient, devto_client: DevtoClient) -> BlogScheduler:
    """Factory function to create a BlogScheduler instance."""
    return BlogScheduler(hf_client, devto_client) 
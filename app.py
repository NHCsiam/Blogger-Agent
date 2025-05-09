import argparse
from application.api.huggingface_client import HuggingFaceClient
from application.api.dev_client import DevtoClient
from application.models.content_gen import ContentGenerator
from application.factory import create_app
from application.automation.scheduler import create_scheduler
from application.config import Config
import random

def manual_mode(topic: str, category: str = None):
    """Run in manual mode with a specific topic."""
    hf_client, devto_client = create_app()
    config = Config()
    
    prompt = ContentGenerator.build_prompt(topic)
    print("Generating blog content...")
    blog_content = hf_client.generate_blog_content(prompt)
    
    # Get appropriate tags
    tags = config.get_tags(category or "tech")
    selected_tags = random.sample(tags, min(5, len(tags)))
    
    print("Blog content generated. Publishing to DEV.to...")
    url = devto_client.publish_post(
        title=topic,
        body_markdown=blog_content,
        tags=selected_tags
    )
    print(f"✅ Blog posted successfully! 🔗 URL: {url}")

def automated_mode(schedule_type: str, time: str = None, day: str = None, category: str = None):
    """Run in automated mode with scheduling."""
    hf_client, devto_client = create_app()
    scheduler = create_scheduler(hf_client, devto_client)
    
    if schedule_type == "daily":
        hour, minute = map(int, time.split(":")) if time else (9, 0)
        scheduler.schedule_daily_post(hour=hour, minute=minute, category=category)
    elif schedule_type == "weekly":
        day = day or "monday"
        hour, minute = map(int, time.split(":")) if time else (10, 0)
        scheduler.schedule_weekly_post(day=day, hour=hour, minute=minute, category=category)
    
    print(f"Starting automated blog generation in {schedule_type} mode...")
    scheduler.run_scheduler()

def list_categories():
    """List all available categories and their topics."""
    config = Config()
    print("\nAvailable Categories and Topics:")
    print("================================")
    for category, topics in config.config["topics"].items():
        print(f"\n{category.upper()}:")
        for topic in topics:
            print(f"  - {topic}")

def main():
    parser = argparse.ArgumentParser(description="Blog Generation Tool")
    parser.add_argument("--mode", choices=["manual", "automated", "list"], default="manual",
                      help="Run in manual, automated, or list mode")
    parser.add_argument("--topic", help="Blog topic for manual mode")
    parser.add_argument("--category", help="Category for blog posts")
    parser.add_argument("--schedule", choices=["daily", "weekly"], help="Schedule type for automated mode")
    parser.add_argument("--time", help="Time for scheduled posts (HH:MM)")
    parser.add_argument("--day", help="Day for weekly posts (e.g., monday)")

    args = parser.parse_args()

    if args.mode == "list":
        list_categories()
        return

    if args.mode == "manual":
        if not args.topic:
            topic = input("Enter your blog topic: ").strip()
            if not topic:
                print("Topic cannot be empty.")
                return
            args.topic = topic
        manual_mode(args.topic, args.category)
    else:
        if not args.schedule:
            print("Please specify a schedule type (daily/weekly)")
            return
        automated_mode(args.schedule, args.time, args.day, args.category)

if __name__ == "__main__":
    main()

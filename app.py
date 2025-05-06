from application.factory import create_app
from application.models.content_generator import ContentGenerator

def main():
    topic = input("Enter your blog topic: ").strip()
    if not topic:
        print("Topic cannot be empty.")
        return

    hf_client, medium_client = create_app()
    prompt = ContentGenerator.build_prompt(topic)
    print("Generating blog content...")
    blog_content = hf_client.generate_blog_content(prompt)
    print("Blog content generated. Publishing to Medium...")

    user_id = medium_client.get_user_id()
    url = medium_client.publish_post(user_id, topic, blog_content, tags=["focus", "study", "productivity"])
    print(f"✅ Blog posted successfully! 🔗 URL: {url}")

if __name__ == "__main__":
    main()

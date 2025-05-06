from application.api.huggingface_client import HuggingFaceClient
from application.api.dev_client import DevtoClient
from application.models.content_gen import ContentGenerator
from application.factory import create_app
def main():
    topic = input("Enter your blog topic: ").strip()
    if not topic:
        print("Topic cannot be empty.")
        return

    hf_client, devto_client = create_app()
    prompt = ContentGenerator.build_prompt(topic)
    print("Generating blog content...")
    blog_content = hf_client.generate_blog_content(prompt)
    print("Blog content generated. Publishing to DEV.to...")

    url = devto_client.publish_post(
        title=topic,
        body_markdown=blog_content,
        tags=["focus", "study", "productivity"]
    )
    print(f"✅ Blog posted successfully! 🔗 URL: {url}")

if __name__ == "__main__":
    main()

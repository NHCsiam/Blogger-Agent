class ContentGenerator:
    @staticmethod
    def build_prompt(topic):
        return (
            f"Write a long, detailed, SEO-friendly blog post in Markdown about: {topic}.\n"
            "Include ## headings, bullet points, and actionable tips."
        )
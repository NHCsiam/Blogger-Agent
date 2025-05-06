class ContentGenerator:
    @staticmethod
    def build_prompt(topic):
        return f"""<s>[INST] Write an engaging, SEO-optimized blog post about "{topic}" in a clear and conversational tone. 
        Include:
        - A catchy title and meta description (under 160 characters),
        - An introduction, well-structured headings (H2, H3),
        - Bullet points and a conclusion,
        - Natural use of relevant keywords,
        - 5 FAQs and 5 internal linking suggestions.
        
        Format everything in Markdown. Make it informative, easy to read, and enjoyable. [/INST]"""
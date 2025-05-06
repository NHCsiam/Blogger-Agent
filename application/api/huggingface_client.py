import os
import requests

class HuggingFaceClient:
    def __init__(self, token):
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def generate_blog_content(self, prompt, max_new_tokens=1500):
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
                "repetition_penalty": 1.2
            }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()  # Raises HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            raise Exception(f"Hugging Face request failed: {e}")

        result = response.json()

        # Safely extract generated text
        if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
            return result[0]['generated_text']
        else:
            raise Exception("Unexpected response format from Hugging Face API.")

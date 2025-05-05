import os
import requests

class HuggingFaceClient:
    def __init__(self, token):
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
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
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Hugging Face Error: {response.status_code} {response.text}")
        return response.json()[0]['generated_text']

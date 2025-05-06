import os
from dotenv import load_dotenv
from application.api.huggingface_client import HuggingFaceClient
from application.api.medium_client import MediumClient
from application.models.content_generator import ContentGenerator

def create_app():
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    medium_token = os.getenv("MEDIUM_TOKEN")
    if not hf_token or not medium_token:
        raise Exception("API tokens not found in environment variables!")

    hf_client = HuggingFaceClient(hf_token)
    medium_client = MediumClient(medium_token)
    return hf_client, medium_client

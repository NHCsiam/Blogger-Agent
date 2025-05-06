import os
from dotenv import load_dotenv
from application.api.huggingface_client import HuggingFaceClient
from application.api.dev_client import DevtoClient
from application.models.content_gen import ContentGenerator

def create_app():
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    devto_token = os.getenv("DEVTO_TOKEN")
    if not hf_token or not devto_token:
        raise Exception("API tokens not found in environment variables!")

    hf_client = HuggingFaceClient(hf_token)
    devto_client = DevtoClient(devto_token)
    return hf_client, devto_client

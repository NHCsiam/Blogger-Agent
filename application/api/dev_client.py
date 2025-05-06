import requests

class DevtoClient:
    def __init__(self, token):
        self.headers = {
            "api-key": token,
            "Content-Type": "application/json"
        }
        self.base_url = "https://dev.to/api"

    def publish_post(self, title, body_markdown, tags=None, published=True):
        data = {
            "article": {
                "title": title,
                "published": published,
                "body_markdown": body_markdown,
                "tags": tags or ["ai", "productivity", "blogging"]
            }
        }
        response = requests.post(f"{self.base_url}/articles", headers=self.headers, json=data)
        if response.status_code in (201, 200):
            return response.json().get("url")
        else:
            raise Exception(f"Failed to post: {response.status_code} {response.text}")

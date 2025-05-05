import requests

class MediumClient:
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.base_url = "https://api.medium.com/v1"

    def get_user_id(self):
        response = requests.get(f"{self.base_url}/me", headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Medium Error: {response.status_code} {response.text}")
        return response.json()['data']['id']

    def publish_post(self, user_id, title, content, tags=None):
        post_data = {
            "title": title,
            "contentFormat": "markdown",
            "content": content,
            "publishStatus": "public",
            "tags": tags or []
        }
        post_url = f"{self.base_url}/users/{user_id}/posts"
        response = requests.post(post_url, headers=self.headers, json=post_data)
        if response.status_code == 201:
            return response.json()['data']['url']
        else:
            raise Exception(f"Failed to post: {response.status_code} {response.text}")

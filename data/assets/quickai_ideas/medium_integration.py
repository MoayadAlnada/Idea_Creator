import requests
import json
from typing import Dict, Optional


class MediumIntegration:
    def __init__(self, access_token: str):
        """
        Initializes the MediumIntegration class with the necessary authentication details.

        Args:
        - access_token (str): Medium API access token for authenticating API requests.
        """
        self.base_url = "https://api.medium.com/v1"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_user_details(self) -> Dict:
        """
        Fetches the authenticated user's details from Medium.

        Returns:
        - A dictionary containing the user's details.
        """
        endpoint = "/me"
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        return response.json()

    def create_post(self, user_id: str, title: str, content: str, content_format: str = "html", tags: Optional[list] = None, publish_status: str = "draft") -> Dict:
        """
        Creates a new post on Medium for the authenticated user.

        Args:
        - user_id (str): The Medium user ID for which the post is being created.
        - title (str): The title of the post.
        - content (str): The body content of the post (in HTML or Markdown).
        - content_format (str): Format of the content ('html' or 'markdown'). Default is 'html'.
        - tags (list): A list of tags to associate with the post. Optional.
        - publish_status (str): The publish status of the post. Options: 'public', 'draft', 'unlisted'. Default is 'draft'.

        Returns:
        - A dictionary containing data of the created post.
        """
        if tags is None:
            tags = []
        data = {
            "title": title,
            "contentFormat": content_format,
            "content": content,
            "tags": tags,
            "publishStatus": publish_status,
        }
        endpoint = f"/users/{user_id}/posts"
        response = requests.post(f"{self.base_url}{endpoint}", headers=self.headers, json=data)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        return response.json()

    def publish_ai_generated_content(self, title: str, content: str, tags: Optional[list] = None):
        """
        Convenience method to directly publish AI-generated content to the authenticated user's Medium blog.

        This method fetches the user's ID, then creates and publishes a new post.

        Args:
        - title (str): The title of the AI-generated content.
        - content (str): The AI-generated content body (in HTML).
        - tags (list): A list of tags related to the AI-generated content. Optional.

        Returns:
        - A dictionary confirming the publication of the post.
        """
        user_details = self.get_user_details()
        user_id = user_details['data']['id']
        return self.create_post(user_id=user_id, title=title, content=content, tags=tags, publish_status='public')
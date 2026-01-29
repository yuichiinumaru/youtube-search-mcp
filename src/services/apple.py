import requests
from typing import List, Dict, Any, Optional
import os
from src.common.logger import get_logger

logger = get_logger(__name__)

class AppleMusicService:
    def __init__(self):
        self.developer_token = os.getenv("APPLE_MUSIC_DEVELOPER_TOKEN")
        self.user_token = os.getenv("APPLE_MUSIC_USER_TOKEN")
        self.base_url = "https://api.music.apple.com/v1"

    def _get_headers(self, include_user_token: bool = False) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.developer_token}"
        }
        if include_user_token and self.user_token:
            headers["Music-User-Token"] = self.user_token
        return headers

    def search_catalog(self, term: str, types: List[str] = ["songs"], storefront: str = "us", limit: int = 10) -> Dict[str, Any]:
        if not self.developer_token:
            return {"error": "Apple Music Developer Token not configured"}

        url = f"{self.base_url}/catalog/{storefront}/search"
        params = {
            "term": term.replace(" ", "+"),
            "types": ",".join(types),
            "limit": limit
        }
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Apple Music search error: {e}")
            return {"error": str(e)}

    def get_charts(self, types: List[str] = ["songs"], storefront: str = "us", limit: int = 10) -> Dict[str, Any]:
        url = f"{self.base_url}/catalog/{storefront}/charts"
        params = {
            "types": ",".join(types),
            "limit": limit
        }
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Apple Music charts error: {e}")
            return {"error": str(e)}

    def get_library_playlists(self, limit: int = 25) -> Dict[str, Any]:
        if not self.user_token:
            return {"error": "Apple Music User Token not configured"}

        url = f"{self.base_url}/me/library/playlists"
        params = {"limit": limit}
        try:
            response = requests.get(url, headers=self._get_headers(include_user_token=True), params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Apple Music library playlists error: {e}")
            return {"error": str(e)}

class ApplePodcastsService:
    def __init__(self):
        self.base_url = "https://itunes.apple.com"

    def search(self, term: str, entity: str = "podcast", country: str = "us", limit: int = 10) -> Dict[str, Any]:
        url = f"{self.base_url}/search"
        params = {
            "term": term,
            "entity": entity,
            "country": country,
            "limit": limit
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Apple Podcasts search error: {e}")
            return {"error": str(e)}

    def lookup(self, id: str, entity: str = "podcast") -> Dict[str, Any]:
        url = f"{self.base_url}/lookup"
        params = {
            "id": id,
            "entity": entity
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Apple Podcasts lookup error: {e}")
            return {"error": str(e)}

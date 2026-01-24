from typing import Any, Dict, List, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.common.config import config
from src.common.logger import get_logger
from src.common.utils import parse_iso8601_duration_to_seconds, chunked

logger = get_logger(__name__)

class YouTubeAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.YOUTUBE_API_KEY
        self.client = None
        if self.api_key:
            try:
                self.client = build('youtube', 'v3', developerKey=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize YouTube API client: {e}")

    def is_available(self) -> bool:
        return self.client is not None

    def search(self, query: str, max_results: int = 10, search_type: str = "video") -> List[Dict[str, Any]]:
        """
        Search for resources on YouTube.
        search_type: 'video', 'channel', 'playlist'
        """
        if not self.is_available():
            logger.warning("YouTube API not available.")
            return []

        try:
            request = self.client.search().list(
                q=query,
                part="snippet",
                maxResults=max_results,
                type=search_type
            )
            response = request.execute()

            results = []
            for item in response.get("items", []):
                res = {
                    "id": item["id"].get("videoId") or item["id"].get("channelId") or item["id"].get("playlistId"),
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                    "channelTitle": item["snippet"].get("channelTitle"),
                    "publishTime": item["snippet"]["publishedAt"]
                }
                results.append(res)
            return results

        except HttpError as e:
            logger.error(f"YouTube API Search error: {e}")
            return []

    def get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        if not self.is_available():
            return []

        results = []
        # API allows max 50 ids per call
        for batch in chunked(video_ids, 50):
            try:
                request = self.client.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=",".join(batch)
                )
                response = request.execute()

                for item in response.get("items", []):
                    details = {
                        "id": item["id"],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "channelTitle": item["snippet"]["channelTitle"],
                        "channelId": item["snippet"]["channelId"],
                        "tags": item["snippet"].get("tags", []),
                        "publishedAt": item["snippet"]["publishedAt"],
                        "viewCount": int(item["statistics"].get("viewCount", 0)),
                        "likeCount": int(item["statistics"].get("likeCount", 0)),
                        "commentCount": int(item["statistics"].get("commentCount", 0)),
                        "duration": item["contentDetails"]["duration"],
                        "durationSeconds": parse_iso8601_duration_to_seconds(item["contentDetails"]["duration"])
                    }
                    results.append(details)
            except HttpError as e:
                logger.error(f"YouTube API Video Details error: {e}")

        return results

    def get_channel_details(self, channel_ids: List[str]) -> List[Dict[str, Any]]:
        if not self.is_available():
            return []

        results = []
        for batch in chunked(channel_ids, 50):
            try:
                request = self.client.channels().list(
                    part="snippet,statistics,contentDetails",
                    id=",".join(batch)
                )
                response = request.execute()

                for item in response.get("items", []):
                    details = {
                        "id": item["id"],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "subscriberCount": int(item["statistics"].get("subscriberCount", 0)),
                        "videoCount": int(item["statistics"].get("videoCount", 0)),
                        "viewCount": int(item["statistics"].get("viewCount", 0)),
                        "uploadsPlaylist": item["contentDetails"]["relatedPlaylists"]["uploads"]
                    }
                    results.append(details)
            except HttpError as e:
                logger.error(f"YouTube API Channel Details error: {e}")

        return results

    def get_playlist_items(self, playlist_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        if not self.is_available():
            return []

        try:
            # We might need pagination for > 50, but keeping it simple for now
            request = self.client.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=min(max_results, 50)
            )
            response = request.execute()

            results = []
            for item in response.get("items", []):
                results.append({
                    "id": item["contentDetails"]["videoId"],
                    "title": item["snippet"]["title"],
                    "publishedAt": item["snippet"]["publishedAt"],
                    "channelTitle": item["snippet"]["channelTitle"]
                })
            return results
        except HttpError as e:
            logger.error(f"YouTube API Playlist Items error: {e}")
            return []

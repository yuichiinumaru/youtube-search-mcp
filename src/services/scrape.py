from typing import Any, Dict, List
from youtubesearchpython import VideosSearch, ChannelsSearch, PlaylistsSearch
import requests
import xml.etree.ElementTree as ET
from src.common.logger import get_logger

logger = get_logger(__name__)

class YouTubeScraper:
    def search_videos(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        try:
            videos_search = VideosSearch(query, limit=max_results)
            results = videos_search.result()

            output = []
            for item in results.get("result", []):
                output.append({
                    "id": item["id"],
                    "title": item["title"],
                    "description": "".join([d.get("text", "") for d in item.get("descriptionSnippet", [])]),
                    "duration": item["duration"],
                    "viewCount": item["viewCount"]["short"],
                    "channelTitle": item["channel"]["name"],
                    "channelId": item["channel"]["id"],
                    "publishedAt": item["publishedTime"],
                    "thumbnail": item["thumbnails"][0]["url"] if item.get("thumbnails") else None,
                    "link": item["link"]
                })
            return output
        except Exception as e:
            logger.error(f"Scraper Video Search error: {e}")
            return []

    def search_channels(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        try:
            channels_search = ChannelsSearch(query, limit=max_results)
            results = channels_search.result()

            output = []
            for item in results.get("result", []):
                output.append({
                    "id": item["id"],
                    "title": item["title"],
                    "description": "".join([d.get("text", "") for d in item.get("descriptionSnippet", [])]),
                    "videoCount": item["videoCount"],
                    "subscriberCount": item["subscribers"],
                    "thumbnail": item["thumbnails"][0]["url"] if item.get("thumbnails") else None,
                    "link": item["link"]
                })
            return output
        except Exception as e:
            logger.error(f"Scraper Channel Search error: {e}")
            return []

    def get_latest_videos_rss(self, channel_id: str) -> List[Dict[str, Any]]:
        """
        Get latest videos from a channel using RSS feed (No API Key required).
        """
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        try:
            response = requests.get(rss_url, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Failed to fetch RSS feed for channel {channel_id}: {response.status_code}")
                return []

            root = ET.fromstring(response.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}

            videos = []
            for entry in root.findall('atom:entry', ns):
                video_id = entry.find('yt:videoId', ns).text
                title = entry.find('atom:title', ns).text
                link = entry.find('atom:link', ns).attrib['href']
                published = entry.find('atom:published', ns).text

                videos.append({
                    "id": video_id,
                    "title": title,
                    "link": link,
                    "publishedAt": published,
                    "source": "rss"
                })
            return videos

        except Exception as e:
            logger.error(f"RSS Feed error: {e}")
            return []

    def get_trending_videos(self) -> List[Dict[str, Any]]:
        """
        Get trending videos using youtube-search-python.
        Note: The library doesn't seem to export Trending class directly in this version.
        Falling back to a search query for 'trending' which is a reasonable approximation.
        """
        try:
            # Fallback strategy since Trending is not available
            return self.search_videos("trending", max_results=10)
        except Exception as e:
            logger.error(f"Scraper Trending error: {e}")
            return []

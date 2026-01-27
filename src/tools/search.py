from typing import List, Dict, Any
from src.services.api import YouTubeAPI
from src.services.scrape import YouTubeScraper
from src.common.logger import get_logger

logger = get_logger(__name__)

api = YouTubeAPI()
scraper = YouTubeScraper()

def search_videos(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search for videos on YouTube. Uses Official API if available, falls back to Scraper.
    """
    if api.is_available():
        logger.info(f"Searching using API: {query}")
        return api.search(query, max_results, search_type="video")
    else:
        logger.info(f"Searching using Scraper: {query}")
        return scraper.search_videos(query, max_results)

def get_video_details(video_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a video.
    """
    if api.is_available():
        results = api.get_video_details([video_id])
        if results:
            return results[0]
    return {"error": "API not available or Video not found"}

def get_channel_details(channel_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a channel.
    """
    if api.is_available():
        results = api.get_channel_details([channel_id])
        if results:
            return results[0]
    return {"error": "API not available or Channel not found"}

def search_videos_by_location(query: str, location: str, location_radius: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search for videos by location.
    location: Latitude/Longitude (e.g., "37.42307,-122.08427")
    location_radius: Radius (e.g., "5km")
    """
    if api.is_available():
        return api.search(query, max_results, search_type="video", location=location, locationRadius=location_radius)
    return {"error": "API not available (Required for Geo-Search)"}

def get_trending_videos(region_code: str = "US", category_id: str = None) -> List[Dict[str, Any]]:
    """
    Get trending videos.
    """
    if api.is_available():
        return api.get_trending_videos(region_code, category_id=category_id)
    else:
        logger.info("Fetching trending via scraper (Region code ignored)")
        return scraper.get_trending_videos()

def register(mcp):
    mcp.tool()(search_videos)
    mcp.tool()(get_video_details)
    mcp.tool()(get_channel_details)
    mcp.tool()(search_videos_by_location)
    mcp.tool()(get_trending_videos)

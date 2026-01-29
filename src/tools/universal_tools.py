from typing import List, Dict, Any, Optional
from src.services.api import YouTubeAPI
from src.services.spotify import SpotifyService
from src.services.apple import AppleMusicService, ApplePodcastsService
from src.common.logger import get_logger

logger = get_logger(__name__)
youtube_api = YouTubeAPI()
spotify_service = SpotifyService()
apple_music = AppleMusicService()
apple_podcasts = ApplePodcastsService()

def universal_search(query: str, limit_per_platform: int = 5) -> Dict[str, Any]:
    """
    Search for music and podcasts across YouTube, Spotify, and Apple simultaneously.
    """
    results = {
        "youtube": [],
        "spotify": {},
        "apple_music": {},
        "apple_podcasts": {}
    }

    # YouTube
    if youtube_api.is_available():
        results["youtube"] = youtube_api.search(query, max_results=limit_per_platform)

    # Spotify
    if spotify_service.is_available():
        results["spotify"] = spotify_service.search(query, limit=limit_per_platform)

    # Apple Music
    results["apple_music"] = apple_music.search_catalog(query, limit=limit_per_platform)

    # Apple Podcasts
    results["apple_podcasts"] = apple_podcasts.search(query, limit=limit_per_platform)

    return results

def register(mcp):
    mcp.tool()(universal_search)

from typing import List, Dict, Any, Optional
from src.services.apple import AppleMusicService, ApplePodcastsService
from src.common.logger import get_logger

logger = get_logger(__name__)
music_service = AppleMusicService()
podcasts_service = ApplePodcastsService()

def apple_music_search(term: str, types: List[str] = ["songs"], storefront: str = "us", limit: int = 10) -> Dict[str, Any]:
    """Search the Apple Music catalog for songs, albums, artists, etc."""
    return music_service.search_catalog(term, types, storefront, limit)

def apple_music_get_charts(types: List[str] = ["songs"], storefront: str = "us", limit: int = 10) -> Dict[str, Any]:
    """Retrieve the top songs, albums, or music videos by storefront on Apple Music."""
    return music_service.get_charts(types, storefront, limit)

def apple_podcasts_search(term: str, entity: str = "podcast", country: str = "us", limit: int = 10) -> Dict[str, Any]:
    """Search for podcasts and episodes using the iTunes Search API."""
    return podcasts_service.search(term, entity, country, limit)

def apple_podcasts_lookup(id: str, entity: str = "podcast") -> Dict[str, Any]:
    """Retrieve details for a specific podcast or episode by ID on Apple Podcasts."""
    return podcasts_service.lookup(id, entity)

def register(mcp):
    mcp.tool()(apple_music_search)
    mcp.tool()(apple_music_get_charts)
    mcp.tool()(apple_podcasts_search)
    mcp.tool()(apple_podcasts_lookup)

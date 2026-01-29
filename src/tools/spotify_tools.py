from typing import List, Dict, Any, Optional
from src.services.spotify import SpotifyService
from src.common.logger import get_logger

logger = get_logger(__name__)
spotify_service = SpotifyService()

def spotify_search(query: str, types: List[str] = ["track"], limit: int = 10) -> Dict[str, Any]:
    """
    Search for tracks, artists, albums, playlists, shows, or episodes on Spotify.
    types: List of types to search for (e.g., ["track", "artist"]).
    """
    return spotify_service.search(query, types, limit)

def spotify_get_track_details(track_id: str) -> Dict[str, Any]:
    """Get detailed metadata for a Spotify track."""
    return spotify_service.get_track(track_id)

def spotify_get_artist_details(artist_id: str) -> Dict[str, Any]:
    """Get artist metadata and top tracks on Spotify."""
    return spotify_service.get_artist(artist_id)

def spotify_get_album_tracks(album_id: str) -> Dict[str, Any]:
    """Get all tracks for a given Spotify album."""
    return spotify_service.get_album(album_id)

def spotify_get_recommendations(seed_artists: List[str] = None, seed_genres: List[str] = None, seed_tracks: List[str] = None, limit: int = 10) -> Dict[str, Any]:
    """Generate track recommendations based on seeds (artists, tracks, genres)."""
    return spotify_service.get_recommendations(seed_artists, seed_genres, seed_tracks, limit)

def spotify_playback_control(action: str, device_id: str = None, context_uri: str = None, uris: List[str] = None) -> bool:
    """
    Control Spotify playback.
    action: 'start', 'resume', 'pause'.
    """
    if action in ["start", "resume"]:
        return spotify_service.start_playback(device_id, context_uri, uris)
    elif action == "pause":
        return spotify_service.pause_playback(device_id)
    return False

def register(mcp):
    mcp.tool()(spotify_search)
    mcp.tool()(spotify_get_track_details)
    mcp.tool()(spotify_get_artist_details)
    mcp.tool()(spotify_get_album_tracks)
    mcp.tool()(spotify_get_recommendations)
    mcp.tool()(spotify_playback_control)

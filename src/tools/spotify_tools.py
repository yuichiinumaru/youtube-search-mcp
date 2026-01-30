from typing import List, Dict, Any, Optional
from src.services.spotify import SpotifyService
from src.common.logger import get_logger

logger = get_logger(__name__)
spotify_service = SpotifyService()

def spotify_search(query: str, types: List[str] = ["track"], limit: int = 10) -> Dict[str, Any]:
    """
    Search for tracks, artists, albums, playlists, shows, or episodes on Spotify.
    types: List of types to search for (e.g., ["track", "artist", "album", "playlist"]).
    """
    return spotify_service.search(query, types, limit)

def spotify_play(query: str = None, context_uri: str = None, uris: List[str] = None, device_id: str = None) -> Dict[str, Any]:
    """
    Start or resume playback.
    - query: Search query to find and play a track (e.g. "Bohemian Rhapsody").
    - context_uri: Context to play (album, artist, playlist).
    - uris: List of track URIs to play.
    - device_id: Target device.
    """
    return spotify_service.play(query=query, context_uri=context_uri, uris=uris, device_id=device_id)

def spotify_pause(device_id: str = None) -> Dict[str, Any]:
    """Pause playback on the specified device (or active device)."""
    return spotify_service.pause(device_id)

def spotify_next(device_id: str = None) -> Dict[str, Any]:
    """Skip to the next track."""
    return spotify_service.next_track(device_id)

def spotify_previous(device_id: str = None) -> Dict[str, Any]:
    """Skip to the previous track."""
    return spotify_service.previous_track(device_id)

def spotify_seek(position_ms: int, device_id: str = None) -> Dict[str, Any]:
    """Seek to the given position in the track (in milliseconds)."""
    return spotify_service.seek(position_ms, device_id)

def spotify_volume(volume_percent: int, device_id: str = None) -> Dict[str, Any]:
    """Set the volume (0-100)."""
    return spotify_service.set_volume(volume_percent, device_id)

def spotify_shuffle(state: bool, device_id: str = None) -> Dict[str, Any]:
    """Set shuffle mode (True/False)."""
    return spotify_service.shuffle(state, device_id)

def spotify_repeat(state: str, device_id: str = None) -> Dict[str, Any]:
    """Set repeat mode: 'track', 'context', or 'off'."""
    return spotify_service.repeat(state, device_id)

def spotify_devices() -> Dict[str, Any]:
    """Get a list of available devices."""
    return spotify_service.get_devices()

def spotify_queue_add(uri: str, device_id: str = None) -> Dict[str, Any]:
    """Add an item (track/episode URI) to the playback queue."""
    return spotify_service.add_to_queue(uri, device_id)

def spotify_get_queue() -> Dict[str, Any]:
    """Get the current user's playback queue."""
    return spotify_service.get_queue()

def spotify_get_playlists(limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Get the current user's playlists."""
    return spotify_service.get_my_playlists(limit, offset)

def spotify_create_playlist(name: str, public: bool = True, description: str = "") -> Dict[str, Any]:
    """Create a new playlist for the current user."""
    return spotify_service.create_playlist(name, public, description)

def spotify_add_to_playlist(playlist_id: str, uris: List[str]) -> Dict[str, Any]:
    """Add items (track URIs) to a playlist."""
    return spotify_service.add_to_playlist(playlist_id, uris)

def spotify_get_liked_songs(limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Get tracks from the current user's 'Liked Songs' collection."""
    return spotify_service.get_liked_songs(limit, offset)

    types: List of types to search for (e.g., ["track", "artist"]).
    """
    return spotify_service.search(query, types, limit)

def spotify_get_track_details(track_id: str) -> Dict[str, Any]:
    """Get detailed metadata for a Spotify track."""
    return spotify_service.get_track(track_id)

def spotify_get_artist_details(artist_id: str) -> Dict[str, Any]:
    """Get artist metadata."""
    return spotify_service.get_artist(artist_id)

def spotify_get_album_tracks(album_id: str) -> Dict[str, Any]:
    """Get tracks for a given album."""
    return spotify_service.get_album(album_id)

def spotify_get_recommendations(seed_artists: List[str] = None, seed_genres: List[str] = None, seed_tracks: List[str] = None, limit: int = 10) -> Dict[str, Any]:
    """Get track recommendations based on seeds."""
    return spotify_service.get_recommendations(seed_artists, seed_genres, seed_tracks, limit)

def spotify_audio_features(track_ids: List[str]) -> Dict[str, Any]:
    """Get audio features (danceability, energy, etc.) for a list of tracks."""
    return spotify_service.get_audio_features(track_ids)

def spotify_audio_analysis(track_id: str) -> Dict[str, Any]:
    """Get low-level audio analysis for a track."""
    return spotify_service.get_audio_analysis(track_id)

def register(mcp):
    # Search
    mcp.tool()(spotify_search)

    # Playback
    mcp.tool()(spotify_play)
    mcp.tool()(spotify_pause)
    mcp.tool()(spotify_next)
    mcp.tool()(spotify_previous)
    mcp.tool()(spotify_seek)
    mcp.tool()(spotify_volume)
    mcp.tool()(spotify_shuffle)
    mcp.tool()(spotify_repeat)
    mcp.tool()(spotify_devices)

    # Queue
    mcp.tool()(spotify_queue_add)
    mcp.tool()(spotify_get_queue)

    # Library
    mcp.tool()(spotify_get_playlists)
    mcp.tool()(spotify_create_playlist)
    mcp.tool()(spotify_add_to_playlist)
    mcp.tool()(spotify_get_liked_songs)

    # Discovery
    mcp.tool()(spotify_get_track_details)
    mcp.tool()(spotify_get_artist_details)
    mcp.tool()(spotify_get_album_tracks)
    mcp.tool()(spotify_get_recommendations)
    mcp.tool()(spotify_audio_features)
    mcp.tool()(spotify_audio_analysis)

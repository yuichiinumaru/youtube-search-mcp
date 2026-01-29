import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from typing import List, Dict, Any, Optional
import os
from src.common.logger import get_logger

logger = get_logger(__name__)

class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
        self.sp = None

        if self.client_id and self.client_secret:
            try:
                # Default to Client Credentials for catalog search
                # If user provides a token or we want user-specific actions, we'd use SpotifyOAuth
                auth_manager = SpotifyClientCredentials(
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
                self.sp = spotipy.Spotify(auth_manager=auth_manager)
                logger.info("Spotify service initialized with Client Credentials.")
            except Exception as e:
                logger.error(f"Failed to initialize Spotify service: {e}")

    def is_available(self) -> bool:
        return self.sp is not None

    def search(self, query: str, types: List[str] = ["track"], limit: int = 10) -> Dict[str, Any]:
        if not self.is_available():
            return {}
        try:
            type_str = ",".join(types)
            return self.sp.search(q=query, limit=limit, type=type_str)
        except Exception as e:
            logger.error(f"Spotify search error: {e}")
            return {}

    def get_track(self, track_id: str) -> Dict[str, Any]:
        if not self.is_available():
            return {}
        return self.sp.track(track_id)

    def get_artist(self, artist_id: str) -> Dict[str, Any]:
        if not self.is_available():
            return {}
        return self.sp.artist(artist_id)

    def get_album(self, album_id: str) -> Dict[str, Any]:
        if not self.is_available():
            return {}
        return self.sp.album(album_id)

    def get_recommendations(self, seed_artists: List[str] = None, seed_genres: List[str] = None, seed_tracks: List[str] = None, limit: int = 10) -> Dict[str, Any]:
        if not self.is_available():
            return {}
        return self.sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, limit=limit)

    # User-specific methods (require OAuth token with proper scopes)
    def get_user_playlists(self, limit: int = 50) -> Dict[str, Any]:
        if not self.is_available():
            return {}
        try:
            return self.sp.current_user_playlists(limit=limit)
        except Exception as e:
            logger.error(f"Spotify get_user_playlists error: {e}")
            return {"error": "Requires user authentication"}

    def create_playlist(self, user_id: str, name: str, public: bool = True, description: str = "") -> Dict[str, Any]:
        if not self.is_available():
            return {}
        return self.sp.user_playlist_create(user=user_id, name=name, public=public, description=description)

    def add_to_playlist(self, playlist_id: str, track_uris: List[str]) -> Dict[str, Any]:
        if not self.is_available():
            return {}
        return self.sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)

    def start_playback(self, device_id: str = None, context_uri: str = None, uris: List[str] = None) -> bool:
        if not self.is_available():
            return False
        try:
            self.sp.start_playback(device_id=device_id, context_uri=context_uri, uris=uris)
            return True
        except Exception as e:
            logger.error(f"Spotify start_playback error: {e}")
            return False

    def pause_playback(self, device_id: str = None) -> bool:
        if not self.is_available():
            return False
        try:
            self.sp.pause_playback(device_id=device_id)
            return True
        except Exception as e:
            logger.error(f"Spotify pause_playback error: {e}")
            return False

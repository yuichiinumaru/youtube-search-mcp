import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from typing import List, Dict, Any, Optional
import os
import json
from src.common.logger import get_logger

logger = get_logger(__name__)

class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

        self.sp = None
        self.auth_manager = None

        if not self.client_id or not self.client_secret:
            logger.warning("Spotify credentials not found. Spotify tools will be unavailable.")
            return

        # Scopes required for all advanced features
        self.scopes = [
            "user-read-playback-state",
            "user-modify-playback-state",
            "user-read-currently-playing",
            "user-library-read",
            "user-library-modify",
            "playlist-read-private",
            "playlist-read-collaborative",
            "playlist-modify-public",
            "playlist-modify-private",
            "user-read-private",
            "user-read-email"
        ]

        try:
            # Hybrid Auth Strategy:
            # 1. If we have a refresh token, force User Auth
            # 2. Else if we have Client ID/Secret, try Client Credentials (limited features)

            if self.refresh_token:
                logger.info("Initializing Spotify with User Auth (Refresh Token present)")
                self.auth_manager = SpotifyOAuth(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    redirect_uri=self.redirect_uri,
                    scope=" ".join(self.scopes),
                    open_browser=False
                )
                # Manually refresh to ensure we have a valid token
                self.auth_manager.refresh_access_token(self.refresh_token)
                self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
            else:
                # Fallback to Client Credentials or interactive OAuth
                # Ideally, we default to Client Credentials for stability in headless modes
                # unless explicitly configured otherwise.
                logger.info("Initializing Spotify with Client Credentials (limited functionality)")
                self.auth_manager = SpotifyClientCredentials(
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
                self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

        except Exception as e:
            logger.error(f"Failed to initialize Spotify service: {e}")

    def is_available(self) -> bool:
        return self.sp is not None

    def _ensure_user_auth(self) -> bool:
        """Check if the current session supports user-specific actions."""
        # Check if auth_manager has refresh_access_token method (characteristic of OAuth flow)
        # or if we explicitly initialized it as such.
        return hasattr(self.auth_manager, "refresh_access_token")

    # --- Search ---
    def search(self, query: str, types: List[str] = ["track"], limit: int = 10) -> Dict[str, Any]:
        if not self.is_available(): return {}
        try:
            type_str = ",".join(types)
            return self.sp.search(q=query, limit=limit, type=type_str)
        except Exception as e:
            logger.error(f"Spotify search error: {e}")
            return {"error": str(e)}

    # --- Playback Control ---
    def play(self, context_uri: str = None, uris: List[str] = None, device_id: str = None, query: str = None) -> Dict[str, Any]:
        """
        Smart play function.
        If query provided, searches and plays first result.
        Else uses context_uri or uris.
        """
        if not self.is_available(): return {"error": "Service unavailable"}
        if not self._ensure_user_auth(): return {"error": "User authentication required for playback. Set SPOTIFY_REFRESH_TOKEN."}

        try:
            if query:
                # Search for track
                results = self.search(query, types=["track"], limit=1)
                items = results.get("tracks", {}).get("items", [])
                if not items:
                    return {"error": f"No tracks found for query: {query}"}
                uris = [items[0]["uri"]]

            self.sp.start_playback(device_id=device_id, context_uri=context_uri, uris=uris)
            return {"status": "playing", "device_id": device_id, "uris": uris, "context": context_uri}
        except Exception as e:
            logger.error(f"Play error: {e}")
            return {"error": str(e)}

    def pause(self, device_id: str = None) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        try:
            self.sp.pause_playback(device_id=device_id)
            return {"status": "paused"}
        except Exception as e:
            return {"error": str(e)}

    def next_track(self, device_id: str = None) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        try:
            self.sp.next_track(device_id=device_id)
            return {"status": "skipped_next"}
        except Exception as e:
            return {"error": str(e)}

    def previous_track(self, device_id: str = None) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        try:
            self.sp.previous_track(device_id=device_id)
            return {"status": "skipped_previous"}
        except Exception as e:
            return {"error": str(e)}

    def seek(self, position_ms: int, device_id: str = None) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        try:
            self.sp.seek_track(position_ms, device_id=device_id)
            return {"status": "seeked", "position_ms": position_ms}
        except Exception as e:
            return {"error": str(e)}

    def set_volume(self, volume_percent: int, device_id: str = None) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        try:
            self.sp.volume(volume_percent, device_id=device_id)
            return {"status": "volume_set", "level": volume_percent}
        except Exception as e:
            return {"error": str(e)}

    def shuffle(self, state: bool, device_id: str = None) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        try:
            self.sp.shuffle(state, device_id=device_id)
            return {"status": "shuffle_set", "state": state}
        except Exception as e:
            return {"error": str(e)}

    def repeat(self, state: str, device_id: str = None) -> Dict[str, Any]:
        """state: 'track', 'context', or 'off'"""
        if not self.is_available(): return {"error": "Service unavailable"}
        try:
            self.sp.repeat(state, device_id=device_id)
            return {"status": "repeat_set", "state": state}
        except Exception as e:
            return {"error": str(e)}

    def get_devices(self) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        if not self._ensure_user_auth(): return {"error": "User authentication required"}
        try:
            return self.sp.devices()
        except Exception as e:
            return {"error": str(e)}

    # --- Queue ---
    def add_to_queue(self, uri: str, device_id: str = None) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        if not self._ensure_user_auth(): return {"error": "User authentication required"}
        try:
            self.sp.add_to_queue(uri, device_id=device_id)
            return {"status": "added_to_queue", "uri": uri}
        except Exception as e:
            return {"error": str(e)}

    def get_queue(self) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        if not self._ensure_user_auth(): return {"error": "User authentication required"}
        try:
            return self.sp.queue()
        except Exception as e:
            return {"error": str(e)}

    # --- Library / Playlists ---
    def get_my_playlists(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        if not self._ensure_user_auth(): return {"error": "User authentication required"}
        try:
            return self.sp.current_user_playlists(limit=limit, offset=offset)
        except Exception as e:
            return {"error": str(e)}

    def create_playlist(self, name: str, public: bool = True, description: str = "") -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        if not self._ensure_user_auth(): return {"error": "User authentication required"}
        try:
            user_id = self.sp.me()["id"]
            return self.sp.user_playlist_create(user=user_id, name=name, public=public, description=description)
        except Exception as e:
            return {"error": str(e)}

    def add_to_playlist(self, playlist_id: str, uris: List[str]) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        if not self._ensure_user_auth(): return {"error": "User authentication required"}
        try:
            return self.sp.playlist_add_items(playlist_id=playlist_id, items=uris)
        except Exception as e:
            return {"error": str(e)}

    def get_liked_songs(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        if not self.is_available(): return {"error": "Service unavailable"}
        if not self._ensure_user_auth(): return {"error": "User authentication required"}
        try:
            return self.sp.current_user_saved_tracks(limit=limit, offset=offset)
        except Exception as e:
            return {"error": str(e)}

    # --- Discovery / Details ---
    def get_recommendations(self, seed_artists: List[str] = None, seed_genres: List[str] = None, seed_tracks: List[str] = None, limit: int = 10) -> Dict[str, Any]:
        if not self.is_available(): return {}
        try:
            return self.sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, limit=limit)
        except Exception as e:
            return {"error": str(e)}

    def get_audio_features(self, track_ids: List[str]) -> Dict[str, Any]:
        if not self.is_available(): return {}
        try:
            return {"features": self.sp.audio_features(track_ids)}
        except Exception as e:
            return {"error": str(e)}

    def get_audio_analysis(self, track_id: str) -> Dict[str, Any]:
        if not self.is_available(): return {}
        try:
            return self.sp.audio_analysis(track_id)
        except Exception as e:
            return {"error": str(e)}

    def get_track(self, track_id: str) -> Dict[str, Any]:
        if not self.is_available(): return {}
        return self.sp.track(track_id)

    def get_artist(self, artist_id: str) -> Dict[str, Any]:
        if not self.is_available(): return {}
        return self.sp.artist(artist_id)

    def get_album(self, album_id: str) -> Dict[str, Any]:
        if not self.is_available(): return {}
        return self.sp.album(album_id)

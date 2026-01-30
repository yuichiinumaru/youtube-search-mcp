import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.spotify import SpotifyService
from src.tools import spotify_tools

class TestSpotifyAdvanced(unittest.TestCase):
    @patch('src.services.spotify.SpotifyOAuth')
    @patch('src.services.spotify.spotipy.Spotify')
    @patch.dict(os.environ, {
        "SPOTIFY_CLIENT_ID": "fake_id",
        "SPOTIFY_CLIENT_SECRET": "fake_secret",
        "SPOTIFY_REFRESH_TOKEN": "fake_refresh"
    })
    def setUp(self, mock_spotify, mock_oauth):
        # Mock auth flow
        self.mock_oauth_instance = mock_oauth.return_value
        self.mock_oauth_instance.refresh_access_token.return_value = {"access_token": "valid_token"}

        # Mock spotify client
        self.mock_sp_instance = mock_spotify.return_value

        self.service = SpotifyService()

        # Verify initialization with User Auth
        self.assertTrue(self.service.is_available())
        self.assertTrue(self.service._ensure_user_auth())

    def test_smart_play_query(self):
        # Setup search return
        self.mock_sp_instance.search.return_value = {
            "tracks": {"items": [{"uri": "spotify:track:123"}]}
        }

        result = self.service.play(query="Bohemian Rhapsody")

        self.mock_sp_instance.search.assert_called_with(q="Bohemian Rhapsody", limit=1, type="track")
        self.mock_sp_instance.start_playback.assert_called_with(uris=["spotify:track:123"], device_id=None, context_uri=None)
        self.assertEqual(result["status"], "playing")

    def test_playback_controls(self):
        self.service.pause()
        self.mock_sp_instance.pause_playback.assert_called()

        self.service.next_track()
        self.mock_sp_instance.next_track.assert_called()

        self.service.set_volume(50)
        self.mock_sp_instance.volume.assert_called_with(50, device_id=None)

    def test_queue_add(self):
        self.service.add_to_queue("spotify:track:123")
        self.mock_sp_instance.add_to_queue.assert_called_with("spotify:track:123", device_id=None)

    def test_get_audio_features(self):
        self.mock_sp_instance.audio_features.return_value = [{"danceability": 0.8}]
        result = self.service.get_audio_features(["id1"])
        self.assertEqual(result["features"][0]["danceability"], 0.8)

    def test_tools_wrapper_play(self):
        # Test that the tool wrapper calls the service correctly
        # We need to inject our mock service into the tools module
        original_service = spotify_tools.spotify_service
        spotify_tools.spotify_service = self.service

        try:
            spotify_tools.spotify_play(query="Test Song")
            self.mock_sp_instance.start_playback.assert_called()
        finally:
            spotify_tools.spotify_service = original_service

if __name__ == '__main__':
    unittest.main()

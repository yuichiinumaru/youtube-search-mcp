import unittest
from src.common.utils import extract_video_id, extract_playlist_id, parse_iso8601_duration_to_seconds

class TestUtils(unittest.TestCase):
    def test_extract_video_id(self):
        cases = [
            ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("invalid", None),
        ]
        for inp, expected in cases:
            self.assertEqual(extract_video_id(inp), expected)

    def test_extract_playlist_id(self):
        cases = [
            ("PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxki", "PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxki"),
            ("https://www.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxki", "PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxki"),
            ("invalid", None),
        ]
        for inp, expected in cases:
            self.assertEqual(extract_playlist_id(inp), expected)

    def test_parse_duration(self):
        cases = [
            ("PT1H2M10S", 3730),
            ("PT1M", 60),
            ("P1DT1H", 90000),
            ("invalid", 0),
        ]
        for inp, expected in cases:
            self.assertEqual(parse_iso8601_duration_to_seconds(inp), expected)

if __name__ == "__main__":
    unittest.main()

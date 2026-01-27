import unittest
from src.tools.search import get_trending_videos
from src.services.scrape import YouTubeScraper
import logging

logging.basicConfig(level=logging.DEBUG)

class TestIteration1(unittest.TestCase):
    def test_scraper_trending(self):
        scraper = YouTubeScraper()
        results = scraper.get_trending_videos()
        print(f"DEBUG: Scraper Trending Results: {results[:1]}")
        # Note: Scraper might return empty if structure changes, but function shouldn't crash
        self.assertIsInstance(results, list)

    def test_tool_trending(self):
        # This will use scraper since no API key env var is set in this test environment usually
        results = get_trending_videos()
        self.assertIsInstance(results, list)

if __name__ == "__main__":
    unittest.main()

import unittest
from src.services.scrape import YouTubeScraper
import logging

# Disable logging for tests
logging.disable(logging.CRITICAL)

class TestIntegration(unittest.TestCase):
    def test_scraper_search(self):
        scraper = YouTubeScraper()
        # Search for something very common
        results = scraper.search_videos("python programming", max_results=1)
        self.assertTrue(len(results) > 0)
        video = results[0]
        self.assertIn("title", video)
        self.assertIn("link", video)

    def test_scraper_channel(self):
        scraper = YouTubeScraper()
        # Search for Google Developers channel
        results = scraper.search_channels("Google Developers", max_results=1)
        self.assertTrue(len(results) > 0)
        channel = results[0]
        self.assertIn("title", channel)

if __name__ == "__main__":
    unittest.main()

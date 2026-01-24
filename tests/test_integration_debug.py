import unittest
from src.services.scrape import YouTubeScraper
import logging

logging.basicConfig(level=logging.DEBUG)

class TestIntegration(unittest.TestCase):
    def test_scraper_search(self):
        scraper = YouTubeScraper()
        results = scraper.search_videos("python programming", max_results=1)
        print(f"DEBUG: Results: {results}")
        self.assertTrue(len(results) > 0)

if __name__ == "__main__":
    unittest.main()

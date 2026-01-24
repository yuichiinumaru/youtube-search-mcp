import unittest
from src.services.analytics import AnalyticsService

class TestIteration2(unittest.TestCase):
    def test_sentiment_analysis(self):
        service = AnalyticsService()
        texts = [
            "I love this video, it's amazing!",
            "This is terrible, worst content ever.",
            "This is a video."  # Neutral
        ]
        result = service.analyze_sentiment(texts)

        self.assertEqual(result["sample_size"], 3)
        self.assertGreater(result["sentiment_distribution"]["positive"], 0)
        self.assertGreater(result["sentiment_distribution"]["negative"], 0)
        self.assertGreater(result["sentiment_distribution"]["neutral"], 0)

    def test_engagement_metrics(self):
        service = AnalyticsService()
        stats = {"viewCount": 1000, "likeCount": 100, "commentCount": 50}
        metrics = service.calculate_engagement_metrics(stats)

        self.assertEqual(metrics["like_ratio"], 10.0)
        self.assertEqual(metrics["comment_ratio"], 5.0)
        self.assertEqual(metrics["engagement_rate"], 15.0)

if __name__ == "__main__":
    unittest.main()

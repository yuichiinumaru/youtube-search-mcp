from typing import List, Dict, Any
from textblob import TextBlob
from src.common.logger import get_logger

logger = get_logger(__name__)

class AnalyticsService:
    def analyze_sentiment(self, texts: List[str]) -> Dict[str, Any]:
        """
        Analyze sentiment of a list of texts.
        Returns: {
            "average_polarity": float (-1 to 1),
            "average_subjectivity": float (0 to 1),
            "sentiment_distribution": {"positive": int, "neutral": int, "negative": int}
        }
        """
        if not texts:
            return {
                "average_polarity": 0,
                "average_subjectivity": 0,
                "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0}
            }

        polarities = []
        subjectivities = []
        distribution = {"positive": 0, "neutral": 0, "negative": 0}

        for text in texts:
            blob = TextBlob(text)
            pol = blob.sentiment.polarity
            sub = blob.sentiment.subjectivity
            polarities.append(pol)
            subjectivities.append(sub)

            if pol > 0.1:
                distribution["positive"] += 1
            elif pol < -0.1:
                distribution["negative"] += 1
            else:
                distribution["neutral"] += 1

        avg_pol = sum(polarities) / len(polarities)
        avg_sub = sum(subjectivities) / len(subjectivities)

        return {
            "average_polarity": round(avg_pol, 2),
            "average_subjectivity": round(avg_sub, 2),
            "sentiment_distribution": distribution,
            "sample_size": len(texts)
        }

    def calculate_engagement_metrics(self, stats: Dict[str, int]) -> Dict[str, float]:
        """
        Calculate engagement metrics from raw stats.
        stats: {viewCount, likeCount, commentCount}
        """
        views = stats.get("viewCount", 0)
        likes = stats.get("likeCount", 0)
        comments = stats.get("commentCount", 0)

        if views == 0:
            return {"like_ratio": 0, "comment_ratio": 0, "engagement_rate": 0}

        return {
            "like_ratio": round((likes / views) * 100, 2),
            "comment_ratio": round((comments / views) * 100, 2),
            "engagement_rate": round(((likes + comments) / views) * 100, 2)
        }

from typing import Dict, Any
from src.services.api import YouTubeAPI
from src.services.analytics import AnalyticsService
from src.common.logger import get_logger

logger = get_logger(__name__)

api = YouTubeAPI()
analytics = AnalyticsService()

def get_video_analytics(video_id: str) -> Dict[str, Any]:
    """
    Get comprehensive analytics for a video: metadata, engagement metrics, and comment sentiment.
    """
    if not api.is_available():
        return {"error": "API not available"}

    # 1. Get Details
    details_list = api.get_video_details([video_id])
    if not details_list:
        return {"error": "Video not found"}
    details = details_list[0]

    # 2. Calculate Engagement
    stats = {
        "viewCount": details.get("viewCount", 0),
        "likeCount": details.get("likeCount", 0),
        "commentCount": details.get("commentCount", 0)
    }
    engagement = analytics.calculate_engagement_metrics(stats)

    # 3. Analyze Comments
    comments = api.get_comments(video_id, max_results=50)
    sentiment = analytics.analyze_sentiment(comments)

    return {
        "video_id": video_id,
        "title": details.get("title"),
        "channelTitle": details.get("channelTitle"),
        "stats": stats,
        "engagement_metrics": engagement,
        "sentiment_analysis": sentiment
    }

def get_channel_analytics(channel_id: str) -> Dict[str, Any]:
    """
    Get analytics for a channel.
    """
    if not api.is_available():
        return {"error": "API not available"}

    details_list = api.get_channel_details([channel_id])
    if not details_list:
        return {"error": "Channel not found"}
    details = details_list[0]

    stats = {
        "subscriberCount": details.get("subscriberCount", 0),
        "videoCount": details.get("videoCount", 0),
        "viewCount": details.get("viewCount", 0)
    }

    # Basic derived metrics
    avg_views_per_video = 0
    if stats["videoCount"] > 0:
        avg_views_per_video = round(stats["viewCount"] / stats["videoCount"], 2)

    return {
        "channel_id": channel_id,
        "title": details.get("title"),
        "stats": stats,
        "derived_metrics": {
            "avg_views_per_video": avg_views_per_video
        }
    }

def register(mcp):
    mcp.tool()(get_video_analytics)
    mcp.tool()(get_channel_analytics)

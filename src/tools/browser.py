from src.services.browser import BrowserService
from src.common.logger import get_logger

logger = get_logger(__name__)
browser = BrowserService()

def open_video(video_id: str) -> str:
    """
    Open a YouTube video in the default browser.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    if browser.open_url(url):
        return f"Opened video {video_id} in browser."
    return "Failed to open browser."

def open_channel(channel_id: str) -> str:
    """
    Open a YouTube channel in the default browser.
    """
    url = f"https://www.youtube.com/channel/{channel_id}"
    if browser.open_url(url):
        return f"Opened channel {channel_id} in browser."
    return "Failed to open browser."

def register(mcp):
    mcp.tool()(open_video)
    mcp.tool()(open_channel)

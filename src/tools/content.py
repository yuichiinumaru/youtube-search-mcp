from typing import Dict, Any, Optional
from src.services.transcript import TranscriptService
from src.services.download import DownloadService
from src.common.logger import get_logger

logger = get_logger(__name__)

transcript_service = TranscriptService()
download_service = DownloadService()

def get_transcript(video_id: str) -> str:
    """
    Get the transcript of a video as a single string.
    """
    text = transcript_service.get_transcript_text(video_id)
    if text:
        return text
    return "No transcript found."

def download_video(url: str) -> Dict[str, Any]:
    """
    Download a video from YouTube (or other sites supported by yt-dlp).
    """
    result = download_service.download_video(url)
    if result:
        return result
    return {"error": "Download failed"}

def download_audio(url: str) -> Dict[str, Any]:
    """
    Download audio from a video.
    """
    result = download_service.download_audio(url)
    if result:
        return result
    return {"error": "Download failed"}

def register(mcp):
    mcp.tool()(get_transcript)
    mcp.tool()(download_video)
    mcp.tool()(download_audio)

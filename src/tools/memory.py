from typing import List, Dict, Any
from src.services.rag import RAGService
from src.services.transcript import TranscriptService
from src.services.api import YouTubeAPI
from src.common.logger import get_logger

logger = get_logger(__name__)

rag_service = RAGService()
transcript_service = TranscriptService()
api = YouTubeAPI()

def store_video_memory(video_id: str) -> str:
    """
    Store video transcript and metadata in the vector database for semantic search.
    """
    # 1. Get Transcript (List of items)
    transcript = transcript_service.get_transcript(video_id)
    if not transcript:
        return "Failed to get transcript."

    # 2. Get Metadata
    metadata = {}
    if api.is_available():
        details = api.get_video_details([video_id])
        if details:
            metadata = details[0]

    # 3. Add to RAG
    success = rag_service.add_video(video_id, transcript, metadata)
    if success:
        return f"Successfully stored video {video_id} in memory."
    return "Failed to store video in memory."

def search_memory(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search the vector database for relevant video segments.
    Returns segments with timestamped YouTube URLs.
    """
    results = rag_service.search(query, limit)

    output = []
    for res in results:
        video_id = res.get("video_id")
        start_time = int(res.get("start", 0))
        url = f"https://www.youtube.com/watch?v={video_id}&t={start_time}s"

        output.append({
            "text": res.get("text"),
            "url": url,
            "score": res.get("score"), # LanceDB returns score usually (distance)
            "title": res.get("title")
        })
    return output

def register(mcp):
    mcp.tool()(store_video_memory)
    mcp.tool()(search_memory)

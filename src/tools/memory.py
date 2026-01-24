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
    # 1. Get Transcript
    text = transcript_service.get_transcript_text(video_id)
    if not text:
        return "Failed to get transcript."

    # 2. Get Metadata
    metadata = {}
    if api.is_available():
        details = api.get_video_details([video_id])
        if details:
            metadata = details[0]

    # 3. Add to RAG
    success = rag_service.add_video(video_id, text, metadata)
    if success:
        return f"Successfully stored video {video_id} in memory."
    return "Failed to store video in memory."

def search_memory(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search the vector database for relevant video segments.
    """
    return rag_service.search(query, limit)

def register(mcp):
    mcp.tool()(store_video_memory)
    mcp.tool()(search_memory)

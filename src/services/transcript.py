from typing import List, Dict, Optional, Any
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from src.common.logger import get_logger

logger = get_logger(__name__)

class TranscriptService:
    def get_transcript(self, video_id: str, languages: List[str] = ["en"]) -> Optional[List[Dict[str, Any]]]:
        """
        Fetches transcript using youtube_transcript_api.
        Returns list of {text, start, duration}.
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            return transcript
        except (TranscriptsDisabled, NoTranscriptFound):
            logger.warning(f"No transcript found for video {video_id} in languages {languages}.")
            return None
        except Exception as e:
            logger.error(f"Transcript API error: {e}")
            return None

    def get_transcript_text(self, video_id: str) -> Optional[str]:
        """
        Returns full text of the transcript.
        """
        t = self.get_transcript(video_id)
        if t:
            return " ".join([item['text'] for item in t])
        return None

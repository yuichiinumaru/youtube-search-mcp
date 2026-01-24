import os
from typing import Dict, Any, Optional
import yt_dlp
from src.common.logger import get_logger

logger = get_logger(__name__)

class DownloadService:
    def __init__(self, download_path: str = "./downloads"):
        self.download_path = download_path
        os.makedirs(download_path, exist_ok=True)

    def download_video(self, url: str, format: str = "bestvideo+bestaudio/best") -> Optional[Dict[str, Any]]:
        """
        Downloads video using yt-dlp.
        Returns info dict.
        """
        ydl_opts = {
            'format': format,
            'outtmpl': os.path.join(self.download_path, '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return {
                    "id": info.get("id"),
                    "title": info.get("title"),
                    "filepath": ydl.prepare_filename(info),
                    "duration": info.get("duration")
                }
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None

    def download_audio(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Downloads audio only.
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.download_path, '%(id)s.%(ext)s'),
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # Filename might change due to postprocessing (ext -> mp3)
                filepath = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"
                return {
                    "id": info.get("id"),
                    "title": info.get("title"),
                    "filepath": filepath,
                    "duration": info.get("duration")
                }
        except Exception as e:
            logger.error(f"Audio Download error: {e}")
            return None

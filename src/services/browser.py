import sys
import subprocess
import os
from src.common.logger import get_logger

logger = get_logger(__name__)

class BrowserService:
    def open_url(self, url: str) -> bool:
        """
        Open a URL in the default web browser.
        Returns True if successful, False otherwise.
        """
        try:
            if sys.platform == 'darwin':  # macOS
                subprocess.Popen(['open', url])
            elif sys.platform == 'win32':  # Windows
                os.startfile(url)
            else:  # Linux/Unix
                subprocess.Popen(['xdg-open', url])
            return True
        except Exception as e:
            logger.error(f"Failed to open URL {url}: {e}")
            return False

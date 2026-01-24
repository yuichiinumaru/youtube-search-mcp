import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    LANCEDB_PATH = os.getenv("LANCEDB_PATH", "./data/lancedb")
    # For local embedding model
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # Concurrent fetch limits
    MAX_CONCURRENT_FETCHES = int(os.getenv("MCP_SEARCH_MAX_CONCURRENCY", "6"))

config = Config()

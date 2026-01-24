import lancedb
from sentence_transformers import SentenceTransformer
import pandas as pd
import os
from typing import List, Dict, Any, Optional
import numpy as np
from src.common.config import config
from src.common.logger import get_logger

logger = get_logger(__name__)

class RAGService:
    def __init__(self):
        self.db_path = config.LANCEDB_PATH
        os.makedirs(self.db_path, exist_ok=True)
        self.db = lancedb.connect(self.db_path)
        self.table_name = "videos"
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        self._init_table()

    def _init_table(self):
        # We don't strictly need a schema if we pass pandas df, but it's good practice
        # For simplicity with lancedb python, we can just auto-create from data
        pass

    def embed_text(self, text: str) -> np.ndarray:
        return self.model.encode(text)

    def chunk_transcript(self, transcript: List[Dict[str, Any]], chunk_size: int = 1000) -> List[Dict[str, Any]]:
        """
        Chunk transcript items while preserving timestamps.
        transcript: List of {text, start, duration}
        """
        chunks = []
        current_chunk = []
        current_length = 0
        chunk_start = 0.0

        for item in transcript:
            text = item["text"]
            start = item["start"]
            duration = item["duration"]

            if not current_chunk:
                chunk_start = start

            current_chunk.append(text)
            current_length += len(text)

            if current_length >= chunk_size:
                chunks.append({
                    "text": " ".join(current_chunk),
                    "start": chunk_start,
                    "end": start + duration
                })
                current_chunk = []
                current_length = 0

        if current_chunk:
            chunks.append({
                "text": " ".join(current_chunk),
                "start": chunk_start,
                "end": transcript[-1]["start"] + transcript[-1]["duration"]
            })

        return chunks

    def add_video(self, video_id: str, transcript: List[Dict[str, Any]], metadata: Dict[str, Any]):
        try:
            chunks = self.chunk_transcript(transcript)
            texts = [c["text"] for c in chunks]
            embeddings = self.model.encode(texts)

            data = []
            for i, chunk in enumerate(chunks):
                data.append({
                    "video_id": video_id,
                    "text": chunk["text"],
                    "start": chunk["start"],
                    "end": chunk["end"],
                    "vector": embeddings[i],
                    "chunk_id": i,
                    **metadata
                })

            df = pd.DataFrame(data)

            if self.table_name in self.db.table_names():
                tbl = self.db.open_table(self.table_name)
                tbl.add(df)
            else:
                self.db.create_table(self.table_name, df)

            logger.info(f"Added video {video_id} to RAG with {len(chunks)} chunks.")
            return True
        except Exception as e:
            logger.error(f"RAG Add Video error: {e}")
            return False

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if self.table_name not in self.db.table_names():
            return []

        try:
            query_vec = self.embed_text(query)
            tbl = self.db.open_table(self.table_name)

            results = tbl.search(query_vec).limit(limit).to_pandas()

            output = []
            for _, row in results.iterrows():
                output.append(row.to_dict())
            return output
        except Exception as e:
            logger.error(f"RAG Search error: {e}")
            return []

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

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        # Simple character based chunking for now
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += (chunk_size - overlap)
        return chunks

    def add_video(self, video_id: str, text: str, metadata: Dict[str, Any]):
        try:
            chunks = self.chunk_text(text)
            embeddings = self.model.encode(chunks)

            data = []
            for i, chunk in enumerate(chunks):
                data.append({
                    "video_id": video_id,
                    "text": chunk,
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

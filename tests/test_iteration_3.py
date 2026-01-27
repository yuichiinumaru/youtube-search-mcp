import unittest
from src.services.rag import RAGService

class TestIteration3(unittest.TestCase):
    def test_chunking_with_timestamps(self):
        service = RAGService()
        transcript = [
            {"text": "Hello world.", "start": 0.0, "duration": 2.0},
            {"text": "This is a test.", "start": 2.0, "duration": 2.0},
            {"text": "Another sentence.", "start": 4.0, "duration": 2.0}
        ]

        # Test with small chunk size to force split
        chunks = service.chunk_transcript(transcript, chunk_size=15)

        # "Hello world." (12 chars) -> Chunk 1
        # "This is a test." (15 chars) -> Chunk 2 (or mixed depending on logic)

        self.assertTrue(len(chunks) > 0)
        self.assertIn("start", chunks[0])
        self.assertIn("end", chunks[0])
        self.assertEqual(chunks[0]["start"], 0.0)

if __name__ == "__main__":
    unittest.main()

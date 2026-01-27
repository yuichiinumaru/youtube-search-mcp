# Analysis of Iteration 3: RAG Enhancements

## Goal
Enable searching for specific moments in a video ("Where does he talk about X?") and returning a timestamped link.

## Current Implementation (`src/services/rag.py`)
- Takes raw `text`.
- Chunks by character count.
- Loses timestamp information.

## Strategy
1.  **Input**: Receive `transcript` as `List[Dict]` (from `youtube_transcript_api`).
    - Format: `[{'text': '...', 'start': 0.0, 'duration': 2.0}, ...]`
2.  **Chunking**:
    - Iterate through transcript items.
    - Accumulate text until `chunk_size` (e.g., 1000 chars) is reached.
    - Keep `start` of the first item in the chunk.
    - Keep `end` (`start + duration`) of the last item in the chunk.
3.  **Storage**:
    - Store `start` and `end` in LanceDB metadata.
4.  **Retrieval**:
    - When searching, return `start` time.
    - Generate URL: `https://www.youtube.com/watch?v={video_id}&t={int(start)}s`.

## Refactoring Required
- `TranscriptService` needs to expose `get_transcript` (list) to the tool, not just `get_transcript_text`. (It already does expose `get_transcript`).
- `RAGService.add_video` signature change.

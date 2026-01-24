# Task List

## Preparation
- [x] Create directory structure.
- [x] Analyze reference repositories.
- [ ] Create `pyproject.toml` and install dependencies.

## Core Implementation
- [ ] **Common Utilities**:
    - [ ] `src/common/config.py`: Env vars (YOUTUBE_API_KEY, LANCEDB_PATH).
    - [ ] `src/common/utils.py`: ID extraction, duration parsing (harvested from `aldale`).
- [ ] **Service: Search**:
    - [ ] `src/services/api.py`: `search`, `video_details`, `channel_details` using Google API.
    - [ ] `src/services/scrape.py`: `search` using `youtube-search-python`, `get_latest` using RSS.
- [ ] **Service: Content**:
    - [ ] `src/services/transcript.py`: `get_transcript` (API + Whisper fallback).
    - [ ] `src/services/download.py`: `download_video` using `yt-dlp`.
- [ ] **Service: Memory (RAG)**:
    - [ ] `src/services/rag.py`: LanceDB setup, embedding generation, ingestion, search.
- [ ] **Tools Integration**:
    - [ ] `src/tools/search.py`: FastMCP tools for search (hybrid).
    - [ ] `src/tools/content.py`: Tools for transcripts/downloads.
    - [ ] `src/tools/memory.py`: Tools for RAG.
- [ ] **Server**:
    - [ ] `src/server.py`: Main entry point assembling all tools.

## Validation
- [ ] Unit tests for regex parsers.
- [ ] Integration test for Search (Mocked API).
- [ ] Integration test for RAG (End-to-End).

## Refinement
- [ ] Add "Trending" feature.
- [ ] Add "Geo Search" feature.
- [ ] Documentation (README.md).

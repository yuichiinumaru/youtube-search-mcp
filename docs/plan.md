# Ultimate YouTube MCP - Execution Plan

## Objective
Create the most comprehensive YouTube Model Context Protocol (MCP) server by integrating features, strategies, and code from 50+ analyzed repositories.

## Architecture
The server will be built using `fastmcp` and structured modularly.

```
youtube-ultimate-mcp/
├── src/
│   ├── common/           # Shared utilities (logging, config, helpers)
│   ├── services/         # Core business logic
│   │   ├── api.py        # Google Data API v3 wrapper
│   │   ├── scrape.py     # youtube-search-python & RSS wrapper
│   │   ├── transcript.py # youtube_transcript_api + Whisper
│   │   ├── rag.py        # LanceDB vector store
│   │   └── download.py   # yt-dlp wrapper
│   ├── tools/            # MCP Tool definitions
│   │   ├── search.py
│   │   ├── videos.py
│   │   ├── channels.py
│   │   ├── playlists.py
│   │   └── memory.py
│   └── server.py         # Main entry point
├── tests/
├── pyproject.toml
└── README.md
```

## Implementation Phases

### Phase 1: Foundation & Search
- Set up project with `uv` (or `pip`).
- Implement `api.py` using `googleapiclient`.
- Implement `scrape.py` using `youtube-search-python` and RSS feeds (from `2025_python-mcp-agent`).
- Create `search_videos` tool that attempts API first, then falls back to scraper.

### Phase 2: Content & Transcripts
- Implement `transcript.py`.
- Integrate `youtube_transcript_api`.
- Integrate `content-pipeline` concepts: `yt-dlp` download + `whisper` (optional dependency for local processing).
- Create `get_transcript` tool.

### Phase 3: RAG & Memory
- Implement `rag.py` using `lancedb` (from `Youtube-MCP`).
- Implement `store_video_memory` and `search_memory` tools.
- Use `sentence-transformers` for local embeddings to avoid OpenAI dependency requirement, or make it configurable.

### Phase 4: Advanced Features
- **Geo-Search**: Implement logic from `geo-search-tool`.
- **Analytics**: Add `get_channel_metrics` etc. from `youtube-content-management-mcp`.
- **Browser Control**: Add `open_in_browser` from `mcp-youtube-music`.

## Key "Harvested" Strategies
1.  **Quota Management**: Use RSS feeds for "latest videos" to save API quota.
2.  **Hybrid Search**: API for precision/metadata, Scraper for unlimited/no-key usage.
3.  **Local RAG**: LanceDB is lightweight and perfect for this.
4.  **Robust Parsers**: Use `aldale_yt_mcp`'s regex patterns for IDs and Durations.

## Dependencies
- `fastmcp`
- `google-api-python-client`
- `youtube-search-python`
- `youtube-transcript-api`
- `yt-dlp`
- `lancedb`
- `sentence-transformers` (for local RAG)
- `numpy`
- `tantivy` (for LanceDB FTS if needed)

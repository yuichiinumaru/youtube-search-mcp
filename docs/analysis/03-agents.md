# Analysis of 2025_python-mcp-agent & Agentic-AI

## Overview
These two repositories are analyzed together as they represent "Full Stack" agents that integrate MCP servers with a frontend or agentic framework.

### 2025_python-mcp-agent
- **Tech Stack**: FastAPI, WebSocket, Vanilla JS Frontend.
- **MCP**: Uses `FastMCP`.
- **Key Tools**:
    - `get_youtube_transcript`: Basic wrapper around `youtube_transcript_api`.
    - `search_youtube_videos`: Direct HTTP requests to Google API (no client library).
    - `get_channel_info`: RSS feed parsing for recent videos (clever workaround for quota saving?).

### Agentic-AI
- **Tech Stack**: Google ADK, SerpAPI.
- **Key Features**:
    - **Formatting**: Focuses heavily on how the LLM should present the data (bullet points, bold titles).
    - **SerpAPI**: Uses SerpAPI instead of official Google API. This is a robust alternative but costs money.

## Code Harvesting Opportunities
- **RSS Parsing**: The `get_channel_info` in `2025_python-mcp-agent` uses `https://www.youtube.com/feeds/videos.xml?channel_id=...`. This is a great **quota-free** way to get recent videos. We should implement this.
- **Frontend Integration**: Shows how to expose the MCP via WebSockets, though for our task we are building the MCP server itself.

## Strategic Value
The RSS feed strategy is a hidden gem for monitoring channels without burning API quota.

# Ultimate YouTube MCP Server

The most comprehensive Model Context Protocol (MCP) server for YouTube, integrating features from over 50 analyzed repositories. It combines official API robustness with scraping flexibility, deep content understanding, and local RAG capabilities.

## Features

### 🔍 Advanced Search
- **Hybrid Search**: Automatically switches between official YouTube Data API and Scraping (fallback) to ensure reliability and save quota.
- **Geo-Search**: Find videos by location (latitude, longitude, radius).
- **Trending**: Get trending videos by region and category.
- **Quota Management**: Uses RSS feeds for channel updates to avoid API costs.

### 🧠 Deep Content Understanding
- **Transcripts**: Fetch transcripts for any video (supports auto-generated captions).
- **Local RAG Memory**: Index video content into a local Vector Store (LanceDB) for semantic search.
- **Contextual Retrieval**: Search results return timestamped links (e.g., `&t=120s`) pointing exactly to where the answer is discussed.

### 📊 Analytics & Insights
- **Sentiment Analysis**: Analyze comment sentiment (Positive/Negative/Neutral) using NLP.
- **Engagement Metrics**: Calculate Like/View and Comment/View ratios.
- **Channel Stats**: Detailed subscriber and view statistics.

### ⬇️ Content Management
- **Downloads**: Download videos or audio using `yt-dlp`.
- **Browser Integration**: Open videos or channels directly in your default browser.

## Installation

### Prerequisites
- Python 3.10+
- `ffmpeg` (for audio processing)

### Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install .
   ```
   Or using `uv`:
   ```bash
   uv sync
   ```

3. Create a `.env` file:
   ```bash
   YOUTUBE_API_KEY=your_api_key_here
   LANCEDB_PATH=./data/lancedb
   ```

## Usage

Run the MCP server:

```bash
mcp run src/server.py
# OR if installed as package
python -m src.server
```

## Tools Reference

### Search
- `search_videos(query, max_results)`: Basic search.
- `search_videos_by_location(query, location, location_radius)`: Geo-search.
- `get_trending_videos(region_code, category_id)`: Trending videos.
- `get_video_details(video_id)`: Metadata.
- `get_channel_details(channel_id)`: Channel info.

### Content
- `get_transcript(video_id)`: Get full transcript text.
- `download_video(url)`: Download video to local disk.
- `download_audio(url)`: Download audio only.

### Memory (RAG)
- `store_video_memory(video_id)`: Index a video's transcript into vector DB.
- `search_memory(query)`: Search your indexed videos. Returns timestamped URLs.

### Analytics
- `get_video_analytics(video_id)`: Metrics + Sentiment Analysis.
- `get_channel_analytics(channel_id)`: Channel stats.

### Browser
- `open_video(video_id)`: Open in browser.
- `open_channel(channel_id)`: Open in browser.

## Architecture

- **`src/services/`**: Core logic (API, Scraper, RAG, Analytics).
- **`src/tools/`**: MCP tool definitions.
- **`src/common/`**: Configuration and utilities.

## License
MIT

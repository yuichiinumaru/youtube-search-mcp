# Analysis of Iteration 1: Advanced Search

## Findings from `youtube-trending-mcp`
- **Strategy**: It doesn't actually hit a "Trending" endpoint. Instead, it uses `yt-dlp` to search for keywords like "trending", "viral", "popular". This is a clever but imprecise workaround.
- **yt-dlp usage**: It uses `yt-dlp ytsearch20:query --dump-json` to get results without downloading. This is a very powerful scraping technique.
- **Metadata**: It normalizes `yt-dlp` JSON output nicely.

## Findings from `geo-search-tool`
- **Strategy**: Uses standard YouTube Data API `search.list` parameters: `location` and `locationRadius`.
- **Note**: This *requires* the API. Scrapers usually don't support geo-filtering easily.

## Refined Plan
1.  **API**: Add `get_trending_videos` using the *real* YouTube API `videos().list(chart='mostPopular')`. This is better than the `yt-dlp` workaround.
2.  **Scraper**: Add `get_trending_videos` using `youtube-search-python`'s `Trending` class (if available) or fall back to the `yt-dlp` keyword strategy.
3.  **Geo**: Add `search_by_location` to `api.py`.
4.  **Tools**: Expose these in `src/tools/search.py`.

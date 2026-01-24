# Instructions for AI Agents

## Project Structure
- `src/services/` contains the heavy lifting. If you need to fix a bug in scraping, go to `scrape.py`. If RAG is broken, check `rag.py`.
- `src/tools/` is the interface layer. It should be thin and mostly call services.

## Testing
- Run `pytest` to verify changes.
- `tests/test_integration.py` requires network access.
- `tests/test_utils.py` is pure logic.

## Adding New Features
1. **Service First**: Implement the logic in a Service class.
2. **Tool Second**: Expose it in a `src/tools/` module.
3. **Register**: Add it to `src/server.py`.

## Key Dependencies
- `fastmcp`: The server framework.
- `lancedb`: Vector database.
- `youtube-search-python`: Fallback scraper.

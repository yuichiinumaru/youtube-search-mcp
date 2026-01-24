from fastmcp import FastMCP
from src.tools import search, content, memory
from src.common.logger import get_logger

logger = get_logger("server")

mcp = FastMCP("youtube-ultimate-mcp")

# Register tools
logger.info("Registering search tools...")
search.register(mcp)

logger.info("Registering content tools...")
content.register(mcp)

logger.info("Registering memory tools...")
memory.register(mcp)

def main():
    logger.info("Starting YouTube Ultimate MCP Server...")
    mcp.run()

if __name__ == "__main__":
    main()

"""
MCP Server initialization.
Creates and configures the FastMCP server instance.
"""
import logging
from mcp.server.fastmcp import FastMCP
from tools.display import register_tools

logger = logging.getLogger(__name__)


def create_server() -> FastMCP:
    """
    Create and configure the MCP server instance.
    
    Returns:
        Configured FastMCP server instance with all tools registered
    """
    logger.info("Initializing MCP server...")
    
    # Initialize FastMCP server
    mcp = FastMCP("Pi-Sense-Display")
    
    # Register all tools
    register_tools(mcp)
    
    logger.info("MCP server initialized successfully")
    return mcp


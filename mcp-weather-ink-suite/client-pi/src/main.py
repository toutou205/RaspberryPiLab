#!/usr/bin/env python3
"""
Main entry point for the MCP Server.
Sets up logging and starts the server.
"""
import logging
import sys
import os

# Ensure the current directory (src) is in sys.path so sibling imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.StreamHandler(sys.stdout)
#     ]
# )
# Configure logging
# CRITICAL: ALL logging must go to stderr or file. Stdout is reserved for MCP JSON-RPC messages.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler('/home/alex/mcp_server.log', mode='a', encoding='utf-8')
    ],
    force=True
)
logger = logging.getLogger(__name__)
from server import create_server


def main():
    """Main entry point."""
    try:
        logger.info("Starting Pi-Sense-Display MCP Server...")
        mcp = create_server()
        logger.info("Server created. Attempting to run with transport='stdio'...")
        
        # Explicitly request stdio transport to avoid any auto-detection issues
        mcp.run(transport='stdio')
        
        logger.info("Server run loop exited normally.")
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error in main loop: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

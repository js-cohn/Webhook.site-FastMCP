import os
import sys

# Add src to python path to allow importing webhook_mcp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from webhook_mcp.server import mcp

if __name__ == "__main__":
    mcp.run()

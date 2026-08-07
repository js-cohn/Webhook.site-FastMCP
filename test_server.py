import asyncio
import os
import sys

# Ensure src is in python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from webhooksite_mcp.server import mcp

async def test_mcp_initialization():
    """Verify that FastMCP is properly initialized and all tools are registered."""
    print("Verifying FastMCP server registration...")
    
    assert mcp.name == "Webhook.site", f"Expected server name 'Webhook.site', got '{mcp.name}'"
    
    # Get registered tools
    tools = await mcp.list_tools()
    tool_names = [tool.name for tool in tools]
    print(f"Registered tools: {tool_names}")
    
    expected_tools = [
        "create_token",
        "get_token",
        "update_token",
        "delete_token",
        "list_requests",
        "get_latest_request",
        "delete_requests"
    ]
    
    for tool in expected_tools:
        assert tool in tool_names, f"Expected tool '{tool}' to be registered"
        
    print("Registered resources:")
    resources = await mcp.list_resources()
    resource_uris = [res.uri for res in resources]
    print(resource_uris)
    
    templates = await mcp.list_resource_templates()
    template_uris = [t.uri_template for t in templates]
    print("Registered resource templates:")
    print(template_uris)
    
    assert any("webhooksite://token" in uri for uri in template_uris), "Expected webhooksite resource template to be registered"

    print("All registration checks passed successfully!")

if __name__ == "__main__":
    asyncio.run(test_mcp_initialization())

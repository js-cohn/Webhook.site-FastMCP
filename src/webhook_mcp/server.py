import os
import httpx
from typing import Any, Dict, Optional
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Webhook.site")

BASE_URL = "https://webhook.site"

def _get_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    """Helper to construct headers, optionally adding the Api-Key."""
    key = api_key or os.environ.get("WEBHOOK_SITE_API_KEY")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    if key:
        headers["Api-Key"] = key
    return headers

def _get_token_id(token_id: Optional[str] = None) -> str:
    """Helper to get token ID from argument or environment."""
    tid = token_id or os.environ.get("WEBHOOK_SITE_TOKEN_ID")
    if not tid:
        raise ValueError(
            "token_id is required. Please provide it as an argument or set the "
            "WEBHOOK_SITE_TOKEN_ID environment variable."
        )
    return tid

def _handle_response(response: httpx.Response) -> Dict[str, Any]:
    """Helper to parse response and raise clean exceptions for bad status codes."""
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        # Include response body in error message if available
        try:
            error_body = response.json()
        except ValueError:
            error_body = response.text
        raise RuntimeError(f"API Error ({response.status_code}): {error_body}") from e
    
    if response.status_code == 204:
        return {"success": True, "message": "No content / Action succeeded"}
        
    return response.json()

@mcp.tool()
def create_token(
    api_key: Optional[str] = None,
    default_status: Optional[int] = None,
    default_content: Optional[str] = None,
    default_content_type: Optional[str] = None,
    timeout: Optional[int] = None,
    listen: Optional[int] = None,
    expiry: Optional[int] = None,
    request_limit: Optional[int] = None,
    cors: Optional[bool] = None,
    alias: Optional[str] = None,
    actions: Optional[bool] = None,
    clone_from: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new Webhook.site token (URL / email address container).
    
    Args:
        api_key: Optional Webhook.site API key (or use WEBHOOK_SITE_API_KEY env var)
        default_status: The default HTTP response status returned to requests (200-599)
        default_content: The default response body content
        default_content_type: The default response Content-Type (e.g. 'text/html', 'application/json')
        timeout: Seconds to sleep before returning the response (max: 30)
        listen: Seconds to listen for response from "Set Response" endpoint (max: 10)
        expiry: Seconds until the token auto-expires (max/default: 604800, i.e. 1 week)
        request_limit: Limits request history stored (0 to 10000; default: 10000)
        cors: If true, adds CORS headers to responses
        alias: Sets a custom alias (regex: [a-zA-Z0-9-_]{3,32})
        actions: Enables or disables Custom Actions for the token
        clone_from: Token UUID to clone settings from
    """
    url = f"{BASE_URL}/token"
    headers = _get_headers(api_key)
    
    # Construct request payload only with set parameters
    payload: Dict[str, Any] = {}
    if default_status is not None:
        payload["default_status"] = default_status
    if default_content is not None:
        payload["default_content"] = default_content
    if default_content_type is not None:
        payload["default_content_type"] = default_content_type
    if timeout is not None:
        payload["timeout"] = timeout
    if listen is not None:
        payload["listen"] = listen
    if expiry is not None:
        payload["expiry"] = expiry
    if request_limit is not None:
        payload["request_limit"] = request_limit
    if cors is not None:
        payload["cors"] = cors
    if alias is not None:
        payload["alias"] = alias
    if actions is not None:
        payload["actions"] = actions
    if clone_from is not None:
        payload["clone_from"] = clone_from

    with httpx.Client(timeout=15.0) as client:
        response = client.post(url, json=payload, headers=headers)
        return _handle_response(response)

@mcp.tool()
def get_token(
    token_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Get details and configuration of a Webhook.site token.
    
    Args:
        token_id: The Webhook.site token UUID (or use WEBHOOK_SITE_TOKEN_ID env var)
        api_key: Optional Webhook.site API key (or use WEBHOOK_SITE_API_KEY env var)
    """
    tid = _get_token_id(token_id)
    url = f"{BASE_URL}/token/{tid}"
    headers = _get_headers(api_key)
    
    with httpx.Client(timeout=15.0) as client:
        response = client.get(url, headers=headers)
        return _handle_response(response)

@mcp.tool()
def update_token(
    token_id: Optional[str] = None,
    api_key: Optional[str] = None,
    default_status: Optional[int] = None,
    default_content: Optional[str] = None,
    default_content_type: Optional[str] = None,
    timeout: Optional[int] = None,
    listen: Optional[int] = None,
    expiry: Optional[int] = None,
    request_limit: Optional[int] = None,
    cors: Optional[bool] = None,
    alias: Optional[str] = None,
    actions: Optional[bool] = None
) -> Dict[str, Any]:
    """Update settings of a Webhook.site token.
    
    Args:
        token_id: The Webhook.site token UUID (or use WEBHOOK_SITE_TOKEN_ID env var)
        api_key: Optional Webhook.site API key (or use WEBHOOK_SITE_API_KEY env var)
        default_status: The default HTTP response status returned to requests (200-599)
        default_content: The default response body content
        default_content_type: The default response Content-Type (e.g. 'text/html', 'application/json')
        timeout: Seconds to sleep before returning the response (max: 30)
        listen: Seconds to listen for response from "Set Response" endpoint (max: 10)
        expiry: Seconds until the token auto-expires (max/default: 604800, i.e. 1 week)
        request_limit: Limits request history stored (0 to 10000; default: 10000)
        cors: If true, adds CORS headers to responses
        alias: Sets a custom alias (regex: [a-zA-Z0-9-_]{3,32})
        actions: Enables or disables Custom Actions for the token
    """
    tid = _get_token_id(token_id)
    url = f"{BASE_URL}/token/{tid}"
    headers = _get_headers(api_key)
    
    payload: Dict[str, Any] = {}
    if default_status is not None:
        payload["default_status"] = default_status
    if default_content is not None:
        payload["default_content"] = default_content
    if default_content_type is not None:
        payload["default_content_type"] = default_content_type
    if timeout is not None:
        payload["timeout"] = timeout
    if listen is not None:
        payload["listen"] = listen
    if expiry is not None:
        payload["expiry"] = expiry
    if request_limit is not None:
        payload["request_limit"] = request_limit
    if cors is not None:
        payload["cors"] = cors
    if alias is not None:
        payload["alias"] = alias
    if actions is not None:
        payload["actions"] = actions

    with httpx.Client(timeout=15.0) as client:
        response = client.put(url, json=payload, headers=headers)
        return _handle_response(response)

@mcp.tool()
def delete_token(
    token_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Delete a Webhook.site token/URL completely.
    
    Args:
        token_id: The Webhook.site token UUID (or use WEBHOOK_SITE_TOKEN_ID env var)
        api_key: Optional Webhook.site API key (or use WEBHOOK_SITE_API_KEY env var)
    """
    tid = _get_token_id(token_id)
    url = f"{BASE_URL}/token/{tid}"
    headers = _get_headers(api_key)
    
    with httpx.Client(timeout=15.0) as client:
        response = client.delete(url, headers=headers)
        return _handle_response(response)

@mcp.tool()
def list_requests(
    token_id: Optional[str] = None,
    api_key: Optional[str] = None,
    sorting: str = "newest",
    per_page: int = 50,
    page: int = 1,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    query: Optional[str] = None
) -> Dict[str, Any]:
    """List captured requests, emails, and DNSHooks sent to a token.
    
    Args:
        token_id: The Webhook.site token UUID (or use WEBHOOK_SITE_TOKEN_ID env var)
        api_key: Optional Webhook.site API key (or use WEBHOOK_SITE_API_KEY env var)
        sorting: Sorting order: 'newest' or 'oldest' (default 'newest')
        per_page: Number of requests to return per page (default 50, max 100)
        page: Page number to retrieve (default 1)
        date_from: Filter requests from this date (format 'yyyy-MM-dd HH:mm:ss')
        date_to: Filter requests up to this date (format 'yyyy-MM-dd HH:mm:ss')
        query: Search query to filter requests
    """
    tid = _get_token_id(token_id)
    url = f"{BASE_URL}/token/{tid}/requests"
    headers = _get_headers(api_key)
    
    params: Dict[str, Any] = {
        "sorting": sorting,
        "per_page": per_page,
        "page": page
    }
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    if query:
        params["query"] = query
        
    with httpx.Client(timeout=15.0) as client:
        response = client.get(url, params=params, headers=headers)
        return _handle_response(response)

@mcp.tool()
def get_latest_request(
    token_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """Get the latest raw request body sent to a Webhook.site token.
    
    Args:
        token_id: The Webhook.site token UUID (or use WEBHOOK_SITE_TOKEN_ID env var)
        api_key: Optional Webhook.site API key (or use WEBHOOK_SITE_API_KEY env var)
    """
    tid = _get_token_id(token_id)
    url = f"{BASE_URL}/token/{tid}/request/latest/raw"
    headers = _get_headers(api_key)
    
    with httpx.Client(timeout=15.0) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        return response.text

@mcp.tool()
def delete_requests(
    token_id: Optional[str] = None,
    api_key: Optional[str] = None,
    date_to: Optional[str] = None,
    query: Optional[str] = None
) -> Dict[str, Any]:
    """Delete all or filtered requests from a Webhook.site token.
    
    Args:
        token_id: The Webhook.site token UUID (or use WEBHOOK_SITE_TOKEN_ID env var)
        api_key: Optional Webhook.site API key (or use WEBHOOK_SITE_API_KEY env var)
        date_to: Filter to delete requests up to this date (e.g. 'now-7d' or 'yyyy-MM-dd HH:mm:ss')
        query: Filter to delete requests matching this search query
    """
    tid = _get_token_id(token_id)
    # The delete endpoint uses requests or request. Let's try /requests first, fallback to /request
    url = f"{BASE_URL}/token/{tid}/requests"
    headers = _get_headers(api_key)
    
    params: Dict[str, Any] = {}
    if date_to:
        params["date_to"] = date_to
    if query:
        params["query"] = query
        
    with httpx.Client(timeout=15.0) as client:
        try:
            response = client.delete(url, params=params, headers=headers)
            response.raise_for_status()
            return _handle_response(response)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                # Try fallback /request
                fallback_url = f"{BASE_URL}/token/{tid}/request"
                fallback_resp = client.delete(fallback_url, params=params, headers=headers)
                return _handle_response(fallback_resp)
            raise

# Define an MCP Resource for viewing requests.
@mcp.resource("webhooksite://token/{token_id}/requests")
def get_token_requests_resource(token_id: str) -> str:
    """Gets the list of requests for the token in JSON format as a resource."""
    # Note: Resources don't accept multiple parameters easily, but they can read from env or parameters in the URI.
    # We will get the default API key from the environment.
    headers = _get_headers()
    url = f"{BASE_URL}/token/{token_id}/requests"
    with httpx.Client(timeout=15.0) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        return response.text

if __name__ == "__main__":
    mcp.run()

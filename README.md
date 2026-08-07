# Webhook.site MCP Server

A Model Context Protocol (MCP) server that bridges the [Webhook.site API](https://docs.webhook.site/api/about.html), allowing LLM agents and clients to programmatically create, read, update, and manage webhook tokens and their captured requests.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Setup & Configuration

Configure the following environment variables to authenticate and set defaults:

| Environment Variable | Description |
|---|---|
| `WEBHOOK_SITE_API_KEY` | *(Optional)* Your Webhook.site API key (required for premium accounts, custom actions, and private tokens). |
| `WEBHOOK_SITE_TOKEN_ID` | *(Optional)* A default Webhook.site token UUID to fall back to when not explicitly provided to tools. |

## Running the Server

### Direct Execution (with uv)
```bash
uv run server.py
```

### Installation
You can install this package in editable mode:
```bash
uv pip install -e .
```
This registers the CLI command `webhooksite-mcp`.

## Integrating with MCP Clients

### Claude Desktop
To use this with Claude Desktop, add the following to your `claude_desktop_config.json` (usually located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "webhooksite-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/josh/.config/mcpc/webhooksite-mcp",
        "run",
        "server.py"
      ],
      "env": {
        "WEBHOOK_SITE_API_KEY": "your-api-key-here",
        "WEBHOOK_SITE_TOKEN_ID": "your-default-token-id-here"
      }
    }
  }
}
```

## Available Tools

### 1. `create_token`
Creates a new Webhook.site token (URL / email address container).
- **Arguments**:
  - `api_key` *(string, optional)*: Overrides `WEBHOOK_SITE_API_KEY`.
  - `default_status` *(number, optional)*: Default HTTP status returned to requests (200-599).
  - `default_content` *(string, optional)*: Default response body content.
  - `default_content_type` *(string, optional)*: Default response Content-Type (e.g. `application/json`, `text/html`).
  - `timeout` *(number, optional)*: Seconds to sleep before responding (max 30).
  - `listen` *(number, optional)*: Seconds to wait for "Set Response" endpoint response.
  - `expiry` *(number, optional)*: Seconds until the token auto-expires (default: 604800, 1 week).
  - `request_limit` *(number, optional)*: Limits request history stored (0 to 10000).
  - `cors` *(boolean, optional)*: If `true`, adds CORS headers to responses.
  - `alias` *(string, optional)*: Sets a custom token alias.
  - `actions` *(boolean, optional)*: Enables/disables Custom Actions.
  - `clone_from` *(string, optional)*: Token UUID to clone settings from.

### 2. `get_token`
Get details and configuration of a Webhook.site token.
- **Arguments**:
  - `token_id` *(string, optional)*: Token UUID (defaults to `WEBHOOK_SITE_TOKEN_ID`).
  - `api_key` *(string, optional)*: Overrides `WEBHOOK_SITE_API_KEY`.

### 3. `update_token`
Update settings of an existing Webhook.site token.
- **Arguments**:
  - Same configuration parameters as `create_token` + `token_id`.

### 4. `delete_token`
Delete the Webhook.site token completely.
- **Arguments**:
  - `token_id` *(string, optional)*: Token UUID (defaults to `WEBHOOK_SITE_TOKEN_ID`).
  - `api_key` *(string, optional)*: Overrides `WEBHOOK_SITE_API_KEY`.

### 5. `list_requests`
List captured requests, emails, and DNSHooks sent to a token.
- **Arguments**:
  - `token_id` *(string, optional)*: Token UUID.
  - `api_key` *(string, optional)*: Overrides `WEBHOOK_SITE_API_KEY`.
  - `sorting` *(string, optional)*: Sorting order, either `"newest"` or `"oldest"`.
  - `per_page` *(number, optional)*: Page size (default: 50, max: 100).
  - `page` *(number, optional)*: Page number to retrieve (default: 1).
  - `date_from` *(string, optional)*: Filter requests starting from date (`yyyy-MM-dd HH:mm:ss`).
  - `date_to` *(string, optional)*: Filter requests ending at date (`yyyy-MM-dd HH:mm:ss`).
  - `query` *(string, optional)*: Query string to filter results.

### 6. `get_latest_request`
Get the latest raw request body sent to a Webhook.site token.
- **Arguments**:
  - `token_id` *(string, optional)*: Token UUID.
  - `api_key` *(string, optional)*: Overrides `WEBHOOK_SITE_API_KEY`.

### 7. `delete_requests`
Delete all or filtered requests captured by a Webhook.site token.
- **Arguments**:
  - `token_id` *(string, optional)*: Token UUID.
  - `api_key` *(string, optional)*: Overrides `WEBHOOK_SITE_API_KEY`.
  - `date_to` *(string, optional)*: Filter to delete requests up to this date.
  - `query` *(string, optional)*: Filter to delete requests matching this query.

## Available Resources

### `webhooksite://token/{token_id}/requests`
Allows clients to retrieve the complete list of requests captured by the specified token in raw JSON format.

# VNStock MCP Server (Unofficial)

An **unofficial** MCP (Model Context Protocol) server that provides tools to access Vietnam stock market data. This is a wrapper around the excellent [vnstock](https://github.com/thinh-vu/vnstock) library by [@thinh-vu](https://github.com/thinh-vu).

> **Note**: This is an independent project and is not officially affiliated with the vnstock library or its maintainers.

## About vnstock

This MCP server is built on top of the [vnstock library](https://github.com/thinh-vu/vnstock) - a powerful Python toolkit for Vietnamese stock market analysis created by Thinh Vu. vnstock provides comprehensive access to Vietnam stock market data including:

- Real-time and historical stock prices
- Company financial statements
- Market data and trading statistics
- Mutual fund information
- Gold prices and exchange rates

For more information about the underlying library, visit: https://github.com/thinh-vu/vnstock

## Features

This MCP server exposes vnstock's capabilities through MCP tools, allowing AI assistants and other MCP clients to:

- Access company information and financial data
- Retrieve stock quotes and historical prices
- Get trading statistics and market data
- Query mutual fund information
- Access gold prices and exchange rates
- Retrieve financial statements (income, balance sheet, cash flow)

## Installation

### Install from PyPI (Recommended)
```bash
pip install vnstock-mcp-server
```

### Install from source
```bash
git clone https://github.com/maobui/vnstock-mcp-server.git
cd vnstock-mcp-server
uv sync
```

## Prerequisites
- Python 3.10+
- uv (install with `pip install uv` or see `https://docs.astral.sh/uv/`)

## Quick Start

### Run the MCP server

#### Default mode (stdio)
```bash
# If installed from PyPI
vnstock-mcp-server

# If installed from source with uv
uv run python -m vnstock_mcp.server
```

#### With transport options
```bash
# Use stdio transport (default)
vnstock-mcp-server --transport stdio

# Use Server-Sent Events (SSE) transport for web applications
vnstock-mcp-server --transport sse

# Use SSE with custom mount path
vnstock-mcp-server --transport sse --mount-path /vnstock

# Use HTTP streaming transport
vnstock-mcp-server --transport streamable-http

# Show help with all available options
vnstock-mcp-server --help
```

The server uses `FastMCP` and supports multiple transport protocols:
- **stdio**: Standard input/output (default, for MCP clients like Claude Desktop)
- **sse**: Server-Sent Events (for web applications)
- **streamable-http**: HTTP streaming (for HTTP-based integrations)

## Transport Modes

The VNStock MCP Server supports three different transport protocols to accommodate various use cases:

### stdio (Default)
- **Use case**: Standard MCP clients like Claude Desktop, Cursor, Cline
- **Protocol**: Communication via standard input/output streams
- **Usage**: `vnstock-mcp-server` or `vnstock-mcp-server --transport stdio`
- **Best for**: Desktop applications and traditional MCP integrations

### SSE (Server-Sent Events)
- **Use case**: Web applications that need real-time data streaming
- **Protocol**: HTTP-based server-sent events
- **Usage**: `vnstock-mcp-server --transport sse [--mount-path /path]`
- **Server runs on**: `http://127.0.0.1:8000` (default)
- **Best for**: Web dashboards, browser-based applications

### streamable-http
- **Use case**: HTTP-based integrations and API services
- **Protocol**: HTTP streaming with JSON-RPC over HTTP
- **Usage**: `vnstock-mcp-server --transport streamable-http`
- **Server runs on**: `http://127.0.0.1:8000` (default)
- **Best for**: REST API integrations, microservices architecture

### Command Line Options
```bash
vnstock-mcp-server [OPTIONS]

Options:
  -t, --transport {stdio,sse,streamable-http}
                        Transport protocol to use (default: stdio)
  -m, --mount-path MOUNT_PATH
                        Mount path for SSE transport (optional)
  -v, --version         Show version information
  -h, --help           Show help message
```

## MCP client integration

### Cursor / Cline example
Add a server entry in your MCP configuration:

#### Default stdio transport
```json
{
  "mcpServers": {
    "vnstock": {
      "command": "vnstock-mcp-server"
    }
  }
}
```

#### With specific transport options
```json
{
  "mcpServers": {
    "vnstock-sse": {
      "command": "vnstock-mcp-server",
      "args": ["--transport", "sse", "--mount-path", "/vnstock"]
    },
    "vnstock-http": {
      "command": "vnstock-mcp-server", 
      "args": ["--transport", "streamable-http"]
    }
  }
}
```

If installed from source:
```json
{
  "mcpServers": {
    "vnstock": {
      "command": "uv",
      "args": ["run", "python", "-m", "vnstock_mcp.server"],
      "env": {}
    },
    "vnstock-sse": {
      "command": "uv",
      "args": ["run", "python", "-m", "vnstock_mcp.server", "--transport", "sse"],
      "env": {}
    }
  }
}
```

### Claude Desktop example
In MCP server settings:
- Command: `vnstock-mcp-server`
- Args: (leave empty for stdio, or add transport options like `--transport sse`)

## Available Tools

The MCP server provides the following categories of tools:

### Company Information
- Company overview, news, events
- Shareholders and officers information
- Subsidiaries and insider deals
- Trading statistics and ratios

### Financial Data
- Income statements, balance sheets, cash flows
- Financial ratios and raw reports
- Historical financial data (quarterly/yearly)

### Market Data
- Real-time quotes and historical prices
- Intraday trading data and price depth
- Market price boards for multiple symbols

### Fund Information
- Fund listings and search
- NAV reports and holdings
- Industry and asset allocation

### Miscellaneous
- Gold prices (SJC, BTMC)
- Exchange rates
- Symbol listings by industry/group

## Development

### Install with uv (for development)
```bash
# From the project root
uv sync

# Include dev dependencies (for tests and coverage)
uv sync --group dev
```

### Testing with uv
```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest test/test_company_tools.py

# Run with coverage (HTML)
uv run pytest --cov=src/vnstock_mcp --cov-report=html
# Open report:
#   ./htmlcov/index.html
```

### Building and Publishing

#### Build locally
```bash
# Using the build script
./scripts/build.sh

# Or manually
python -m build
```

#### Create a release
```bash
# Update version in pyproject.toml first, then:
./scripts/release.sh
```

This will:
1. Run tests
2. Create and push a git tag
3. Trigger GitHub Actions to build and publish to PyPI

## Credits

This project is a wrapper around the [vnstock library](https://github.com/thinh-vu/vnstock) created by [@thinh-vu](https://github.com/thinh-vu). All stock market data access functionality is provided by vnstock.

Please consider:
- ⭐ Starring the original [vnstock repository](https://github.com/thinh-vu/vnstock)
- 📖 Reading the [vnstock documentation](https://vnstocks.com/docs)
- 💖 Supporting the vnstock project if you find it valuable

## Disclaimer

This is an unofficial wrapper and is not affiliated with the vnstock library or its maintainers. For issues related to the underlying stock market data or vnstock functionality, please refer to the [vnstock repository](https://github.com/thinh-vu/vnstock).

## Troubleshooting

### Installation Issues
- **Module not found with `uv run`**:
  - Ensure `uv sync` completed successfully in the project root.
  - Verify Python version: `python --version` and `uv python list`.
- **Command `vnstock-mcp-server` not found**:
  - Ensure the package is installed: `pip list | grep vnstock-mcp-server`
  - Try reinstalling: `pip install --upgrade vnstock-mcp-server`

### Connection Issues
- **MCP client cannot connect (stdio mode)**:
  - Confirm the client configuration matches the installation method
  - Check client logs for detailed errors.
  - Ensure no extra arguments are passed for stdio transport
- **Cannot access SSE/HTTP endpoints**:
  - Verify the server is running: check for "Uvicorn running on http://127.0.0.1:8000"
  - Check if port 8000 is available: `netstat -an | grep 8000`
  - Try accessing `http://127.0.0.1:8000` in browser for SSE mode

### Transport Mode Issues
- **SSE transport not working**:
  - Ensure mount-path is correctly specified if needed
  - Check server logs for startup errors
  - Verify web client can connect to the SSE endpoint
- **Wrong transport mode selected**:
  - Use `--help` to see available transport options
  - stdio: for desktop MCP clients (Claude Desktop, Cursor)
  - sse: for web applications
  - streamable-http: for HTTP API integrations

### Getting Help
- **Check server version**: `vnstock-mcp-server --version`
- **View all options**: `vnstock-mcp-server --help`
- **Test server startup**: Run with `--transport stdio` first to verify basic functionality

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests: `uv run pytest`
6. Submit a pull request

## Changelog

### v1.1.0 (Current Development)
- **NEW**: Added support for multiple transport modes (stdio, sse, streamable-http)
- **NEW**: Command line arguments for transport selection (`--transport`, `--mount-path`)
- **NEW**: SSE (Server-Sent Events) transport for web applications
- **NEW**: HTTP streaming transport for API integrations
- **IMPROVED**: Enhanced CLI with help messages and validation
- **IMPROVED**: Better error handling and user feedback
- **IMPROVED**: Comprehensive documentation for all transport modes

### v1.0.0
- Initial release
- Full Vietnam stock market data access via MCP
- Support for company data, financial statements, quotes, and more
- Wrapper around vnstock v3.2.6+
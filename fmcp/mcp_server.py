from fastmcp import FastMCP

# Create a server instance
finance_mcp = FastMCP(name="finance mcp server")

if __name__ == "__main__":
    # mcp.run()  # Default: uses STDIO transport. mcp.run(transport="stdio")
    # Streamable HTTP: Recommended for web deployments.
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp")
    # SSE: For compatibility with existing SSE clients.
    finance_mcp.run(transport="sse", host="127.0.0.1", port=8000)

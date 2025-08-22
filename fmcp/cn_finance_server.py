from fastmcp import FastMCP

# Create a china finance market server instance
cn_finance_mcp = FastMCP(name="china finance mcp server")

if __name__ == "__main__":
    # 只需运行主 Server
    cn_finance_mcp.run(transport="sse", host="127.0.0.1", port=8000)

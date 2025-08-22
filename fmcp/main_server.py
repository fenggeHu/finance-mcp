# main_server.py
from fastmcp import FastMCP
from fmcp import yahoo_finance_server
from fmcp import cn_finance_server

# 创建主 Server
server = FastMCP("finance mcp server")

# 挂载 us/
server.import_server(yahoo_finance_server.yfinance_mcp, prefix="us/")
# 挂载 cn/
server.import_server(cn_finance_server.cn_finance_mcp, prefix="cn/")

if __name__ == "__main__":
    # 只需运行主 Server
    server.run(transport="sse", host="127.0.0.1", port=8000)

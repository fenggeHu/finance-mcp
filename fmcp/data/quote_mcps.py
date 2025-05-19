from fmcp import mcp
from .chanel.em_srv import Eastmoney
from .models import Tick, Bar

quote = Eastmoney()


@mcp.tool(description="Get klines of a symbol on CN market data")
def kline(symbol: str, start: str, end: str) -> list[Bar]:
    """
    获取标的代码的日k线
    :param symbol: 标的代码
    :param start: 起始时间 - 2025-05-01
    :param end: 结束时间 - 2025-05-19
    :return: list[Bar]
    """
    return quote.kline(symbol, start, end)


@mcp.tool(description="Get ticks of a symbol on CN market data")
def tick(symbol: str) -> list[Tick]:
    """
    获取股票的逐笔成交
    :param symbol:
    :return:
    """
    return quote.tick(symbol)

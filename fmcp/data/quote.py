from fmcp.data.models import Bar, TickData


class Quote:
    """
    行情
    """

    # 前复权行情
    def kline(self, symbol: str, begin: str = None, end: str = None) -> list[Bar]:
        """
        前复权的日K线行情
        :param symbol:
        :param begin:
        :param end:
        :return:
        """
        pass

    def tick(self, symbol: str) -> TickData:
        pass

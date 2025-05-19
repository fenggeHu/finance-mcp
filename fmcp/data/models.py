from pydantic.dataclasses import dataclass
from enum import Enum
from typing import List


# 市场
class Market(Enum):
    CN = 'CN'
    US = 'US'


# 交易所
class Exchange(Enum):
    SH = "SH"
    SZ = "SZ"
    BJ = "BJ"
    ZS = "ZS"  # ZS - 指数


@dataclass
class Symbol:
    symbol: str
    name: str
    code: str
    market: int


# class ApiResponse:
#     def __init__(self, status: int = 200, message: str = None):
#         self.status = status  # 错误码
#         self.message = message  # 错误信息


@dataclass
class Bar:
    def __init__(self, datetime: str, o: float, c: float, h: float, l: float, v: float):
        self.datetime = datetime
        self.open = 0 if o == '-' else float(o)
        self.close = 0 if c == '-' else float(c)
        self.high = 0 if h == '-' else float(h)
        self.low = 0 if l == '-' else float(l)
        self.volume = 0 if v == '-' else float(v)


@dataclass
class Tick:
    time: int
    price: float
    volume: int
    bs: int


@dataclass
class TickData:
    code: str
    market: int
    name: str
    data: list[Tick]


@dataclass
class QuoteResponse:
    symbol: Symbol
    data: list[Bar]
    total: int


@dataclass
class Executive:
    name: str  # 姓名
    position: str  # 职位
    high_degree: str  # 最高学历
    gender: str  # 性别
    age: int  # 年龄
    resume: str  # 简历
    incumbent_date: str  # 司职日期


@dataclass
class ExecutiveResponse:
    symbol: str
    data: list[Executive]
    count: int


# 资金流
@dataclass
class CapitalFlowInfo:
    def __init__(self, code: str, name: str, market_code: str, datetime: str, main_in_net_amount: int,
                 small_in_net_amount: int, middle_in_net_amount: int, large_in_net_amount: int,
                 super_in_net_amount: int, main_in_net_percent: float, small_in_net_percent: float,
                 middle_in_net_percent: float, large_in_net_percent: float, super_in_net_percent: float,
                 close: float, change_rate: float):
        self.code = code
        self.name = name
        self.market_code = market_code
        self.datetime = datetime
        self.main_in_net_amount = main_in_net_amount
        self.small_in_net_amount = small_in_net_amount
        self.middle_in_net_amount = middle_in_net_amount
        self.large_in_net_amount = large_in_net_amount
        self.super_in_net_amount = super_in_net_amount
        self.main_in_net_percent = main_in_net_percent
        self.small_in_net_percent = small_in_net_percent
        self.middle_in_net_percent = middle_in_net_percent
        self.large_in_net_percent = large_in_net_percent
        self.super_in_net_percent = super_in_net_percent
        self.close = close
        self.change_rate = change_rate

    @classmethod
    def from_values(cls, code: str, name: str, market_code: str, values: List[str]):
        return cls(
            code=code,
            name=name,
            market_code=market_code,
            datetime=values[0],
            main_in_net_amount=int(float(values[1])),
            small_in_net_amount=int(float(values[2])),
            middle_in_net_amount=int(float(values[3])),
            large_in_net_amount=int(float(values[4])),
            super_in_net_amount=int(float(values[5])),
            main_in_net_percent=float(values[6]),
            small_in_net_percent=float(values[7]),
            middle_in_net_percent=float(values[8]),
            large_in_net_percent=float(values[9]),
            super_in_net_percent=float(values[10]),
            close=float(values[11]),
            change_rate=float(values[12])
        )

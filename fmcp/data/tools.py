import time
from fmcp.data.models import Exchange


def get_request_time():
    return int(time.time())


def to_code2(symbol):
    return [symbol[:2], symbol[2:]]


def to_code(symbol):
    codes = to_code2(symbol)
    return f"{codes[1]}.{codes[0]}"


def gen_secid(symbol):
    market_codes = gen_market_codes(symbol)
    return market_codes[0] + "." + market_codes[1]


def gen_market_codes(symbol):
    codes = to_code2(symbol)
    exchange = codes[0].upper()
    market = None

    if exchange == "SH":
        market = "1"
    elif exchange == "SZ":
        market = "0"
    elif exchange == "ZS":
        f3 = codes[1][:3]
        if f3 == "000":
            market = "1"
        elif f3 == "399":
            market = "0"

    # BJ-北交所0
    market = market or "0"

    return [market, codes[1]]


# 得到交易所代码 - SH\SZ\BJ
def get_cn_exchange(code):
    """
    Determines the Chinese stock exchange based on the stock code.

    Args:
        code (str): The stock code.

    Returns:
        Exchange: The corresponding Chinese stock exchange or raises an exception.

    Raises:
        RuntimeError: If the code length is not 6 or the code is invalid/unsupported.
    """
    if len(code) != 6:
        raise RuntimeError(f"Invalid code length: {code}")

    prefix = code[:3]
    if prefix in ("730", "700", "900", "580"):
        return Exchange.SH
    elif prefix in ("200", "201"):
        return Exchange.SZ
    elif code.startswith("6"):
        return Exchange.SH
    elif code.startswith("0") or code.startswith("3"):
        return Exchange.SZ
    elif code.startswith("4") or code.startswith("8") or prefix == "920":
        return Exchange.BJ
    else:
        raise RuntimeError(f"Invalid or unsupported code: {code}")


def get_symbol(market_code, code):
    if market_code == 1:
        if code.startswith('000'):
            return Exchange.ZS.value + code
        else:
            return Exchange.SH.value + code
    elif market_code == 0:
        if code.startswith('399') or code.startswith('899'):
            return Exchange.ZS.value + code
        else:
            return get_cn_symbol(code)  # 假设 get_cn_symbol 函数已定义
    elif market_code in (2, 90, 105, 106, 107):
        return code
    else:
        raise ValueError(f"Invalid market: {market_code} & code: {code}")


# 函数用来处理其他情况
def get_cn_symbol(code):
    return get_cn_exchange(code) + code

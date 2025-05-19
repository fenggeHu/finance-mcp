# via 18.com.cn
import datetime
from typing import List, Optional

import requests
import logging
from fmcp.data import tools as tools
from fmcp.data.models import Tick, TickData, Bar, Symbol, Executive, QuoteResponse, ExecutiveResponse, \
    CapitalFlowInfo
from fmcp.data.quote import Quote

log = logging.getLogger(__name__)


class Eastmoney(Quote):

    def kline(self, symbol: str, begin: str = None, end: str = None) -> list[Bar]:
        qr = qfq(symbol=symbol, begin=begin, end=end)
        return qr.data

    def tick(self, symbol: str) -> list[Tick]:
        return tick(symbol).data


# 查询股票的逐笔成交数据
def tick(symbol: str) -> TickData:
    codes = tools.gen_market_codes(symbol)
    url = (f"https://push2ex.eastmoney.com/getStockFenShi?pagesize=6000&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj"
           f"&pageindex=0&sort=2&ft=1&code={codes[1]}&market={codes[0]}&_={tools.get_request_time()}")
    response = requests.get(url)

    # 确保请求成功
    if response.status_code == 200:
        # 解析 JSON 数据
        result = response.json()['data']
        ret = TickData(code=result['c'], market=result['m'], name=result['n'],
                       data=[Tick(time=t['t'], price=t['p'], volume=t['v'], bs=t['bs']) for t in result['data']])
        ret.status = 100
        return ret
    else:
        log.info(f"请求失败，状态码: {response.status_code}")
        ret = TickData()
        ret.status = response.status_code
        ret.message = response.text
        return ret


# 查询股票前复权的K线数据
def qfq(symbol: str, begin: str = None, end: str = None) -> QuoteResponse:
    today = datetime.date.today()
    if end is None:
        end = today.strftime("%Y-%m-%d")
    if begin is None:
        begin = (today - datetime.timedelta(days=500)).strftime("%Y-%m-%d")

    secid = tools.gen_secid(symbol)
    bs = begin.replace("-", "")
    es = end.replace("-", "")
    url = (f"https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}"
           "&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61"
           f"&klt=101&fqt=1&beg={bs}&end={es}")
    response = requests.get(url)
    js = response.json()
    if js['data'] is not None:
        data = js['data']
        symbol = Symbol(code=data['code'], name=data['name'], market=data['market'],
                        symbol=tools.get_symbol(data['market'], data['code']))
        rows = [Bar(datetime=r[0], o=r[1], c=r[2], h=r[3], l=r[4], v=r[6])
                for line in data['klines']
                if line  # 添加一个简单的条件判断，确保line非空
                for r in [line.split(',')]  # 将每行分割成列表，再遍历
                ]

        return QuoteResponse(symbol=symbol, data=rows, total=data['dktotal'])

    return QuoteResponse(symbol=Symbol(symbol=symbol, name='', code=tools.to_code2(symbol)[1]), data=[], total=0)


# 公司高管
def executives(symbol: str) -> ExecutiveResponse:
    url = (
        "https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_F10_ORGINFO_MANAINTRO&columns=ALL"
        f"&quoteColumns=&filter=(SECUCODE%3D%22{tools.to_code(symbol)}%22)&pageNumber=1&pageSize=100&source=HSF10")
    response = requests.get(url)
    js = response.json()
    if js['result'] is not None:
        data = js['result']
        return ExecutiveResponse(symbol=symbol, count=data['count'], data=[
            Executive(name=r['PERSON_NAME'], position=r['POSITION'], gender=r['SEX'], high_degree=r['HIGH_DEGREE'],
                      age=r['AGE'], resume=r['RESUME'], incumbent_date=r['INCUMBENT_DATE'])
            for r in data['data']
        ])

    return ExecutiveResponse(symbol=symbol, data=[], count=0)


def capital_flow(symbol: str) -> Optional[List[CapitalFlowInfo]]:
    secid = tools.gen_secid(symbol)
    time = tools.get_request_time()
    url = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=0&klt=101" \
          + "&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65" \
          + f"&secid={secid}&_={time}"

    response_data = requests.get(url).json()
    data = response_data.get('data')

    if not data or 'klines' not in data:
        return []

    klines = data['klines']
    code = data.get('code', '')
    name = data.get('name', '')
    market_code = data.get('market', '')

    capital_flow_info_list = []

    for line in klines:
        values = line.split(",")
        capital_flow_info = CapitalFlowInfo.from_values(code, name, market_code, values)
        capital_flow_info_list.append(capital_flow_info)

    return capital_flow_info_list

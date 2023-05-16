import tinkoff.invest as ti
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.utils import now
import datetime as dt
import re
import matplotlib.pyplot as plt


def get_figi(client, ticker):
    for inst in client.instruments.find_instrument(query=ticker).instruments:
        if inst.ticker == ticker:
            return inst.figi

def get_quotations(client, ticker, from_, to='', timeframe=''):
    from_ = dt.datetime(*map(int, re.sub(r'(\.)0(\d)', r'\1\2', from_).split('.')[::-1]))
    to = dt.datetime(*map(int, re.sub(r'(\.)0(\d)', r'\1\2', to).split('.')[::-1])) if to != '' else now()
    timeframes = {'1 hour': ti.CandleInterval.CANDLE_INTERVAL_HOUR, '2 hours': ti.CandleInterval.CANDLE_INTERVAL_2_HOUR, '4 hours': ti.CandleInterval.CANDLE_INTERVAL_4_HOUR,
                 '1 day': ti.CandleInterval.CANDLE_INTERVAL_DAY, '1 week': ti.CandleInterval.CANDLE_INTERVAL_WEEK,
                 '1 month': ti.CandleInterval.CANDLE_INTERVAL_MONTH, '': ti.CandleInterval.CANDLE_INTERVAL_UNSPECIFIED}
    quotations = list(zip(*[(quot.time, quot.close.units) for quot in client.market_data.get_candles(figi=get_figi(client, ticker), from_=from_, to=to,
                                   interval=timeframes[timeframe]).candles]))
    return quotations

def get_all_tickers(client):
    l = []
    for inst in client.instruments.get_assets().assets:
        try:
            l.append(inst.name)
        except:
            pass
    return l


token = open(r'sandbox_token.txt').read()

with SandboxClient(token) as client:
    while True:
        try:
            ticker = input('Input a ticker: ').upper()
            from_ = input('Input a starting day: ')
            to = input('Input a last day: ')
            timeframe = input('Input a timeframe: ').lower()
            # quot = get_quotations(client, 'BELU', '10.05.2023', timeframe='4 hours')
            quot = get_quotations(client, ticker, from_, to, timeframe)
            plt.plot(*quot[:2])
            plt.show()
            break
        except:
            print('Some input is invalid. Try again.')

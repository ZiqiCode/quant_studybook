from jqdatasdk import *
import numpy as np
import pandas as pd
from datetime import time,datetime,timedelta
from jqdatasdk.alpha191 import *

auth('18813155136','AlphaNet666')

security = '601127.XSHG'


# 1-1 get fundamental data, 'open', 'close', 'low', 'high', 'volume', return df of 30 days
def getfundamental(security, date):
    df = get_price(security, count = 30, end_date=date, frequency='daily',
               fields=['open', 'close', 'low', 'high', 'volume'],
               skip_paused=True, fq='none',  panel=False, fill_paused=True)

    return df


# 1-2计算筹码集中度
def rPos(lista, b):
    for i in range(len(lista)):
        if (lista[i][0] == b):
            return i
    return -1


def getCM(security, date):
    # 函数返回2个值，第一个值是筹码分布的数组，第一列是价格，第二列是筹码百分数（单位：%），第二个值是当前的获利筹码比例（单位：%）
    daynum = 30

    df = get_price(security, end_date=date, frequency='1d', fields=['close'], count=daynum)["close"]
    tr = get_fundamentals_continuously(query(valuation.turnover_ratio).filter(valuation.code.in_([security])),
                                       end_date=date, count=daynum, panel=False)['turnover_ratio']

    data = []
    data.append([df[0], 100])
    for i in range(1, daynum):
        price = df[i]
        hs = tr[i]
        pos = rPos(data, price)
        if (pos == -1):
            for j in data:
                j[1] = j[1] * (100 - hs) * 0.01
            data.append([price, hs])
        else:
            for j in data:
                if (j[0] == price):
                    j[1] = j[1] * (100 - hs) * 0.01
                    j[1] = j[1] + hs
                else:
                    j[1] = j[1] * (100 - hs) * 0.01
    data.sort(key=lambda x: x[0], reverse=True)
    percent = 0
    for i in data:
        if (i[0] < price):
            percent = percent + i[1]
    return data, percent


# 筹码集中度函数返回当前价位上下浮动20% 区间筹码集中度，例如：0.34
def rateCM(security, date):
    score = 0
    #current_date = datetime.now().date() - timedelta(days=1)
    current_date = date
    df = get_price(security, end_date=current_date, frequency='daily',
                   fields=None, skip_paused=False,
                   fq='pre', count=1, panel=True, fill_paused=True)

    df = df.reset_index().rename(columns={'index': 'date'})  # add date column
    df = df.reset_index().rename(columns={'index': 'trade_date'})  # add number of trade date since today column
    cur_price = df.iloc[len(df) - 1, 3]
    lb = cur_price * 0.8
    ub = cur_price * 1.2
    CM_price, CM_percent = getCM(security, current_date)
    total_percent = 0

    for i in range(len(CM_price)):

        if lb <= CM_price[i][0] and CM_price[i][0] <= ub:
            total_percent += (CM_price[i][1] * 0.01)
    return total_percent

# Function to calculate rateCM for the last 30 days
def calculate_rateCM_30_days(security, end_date):
    # Create a date range for the last 30 days
    # start_date = end_date - timedelta(days=29)
    date_range = get_trade_days(start_date=None, end_date=end_date, count=30)

    # Calculate rateCM for each date in the date range
    data = {'Date': date_range, 'RateCM': [rateCM(security, date) for date in date_range]}

    # Create a dataframe from the calculated data
    df = pd.DataFrame(data)

    return df


# 1-3 turn over ratio, return df of 30 days
def get_turnover(security, date):
    tr = get_fundamentals_continuously(query(valuation.turnover_ratio).filter(valuation.code.in_(security)),
                                   end_date=date, count=30, panel=False)['turnover_ratio']
    return tr


# 1-4 get vwap
def get_vwap(security, date):

    return 0



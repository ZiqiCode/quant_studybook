from typing import List, Any

from jqdatasdk import *
import numpy as np
import pandas as pd
from datetime import time,datetime,timedelta
from jqdatasdk.alpha191 import *
from pandas_market_calendars import get_calendar

auth('18813155136','AlphaNet666')

security = '601127.XSHG'


# 1-1 get fundamental data, 'open', 'close', 'low', 'high', 'volume','avg, return df of 30 days
def getfundamental(security, date):
    df = get_price(security, count = 30, end_date=date, frequency='daily',
               fields=['open', 'close', 'low', 'high', 'volume', 'avg'],
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
    query_filter = query(valuation.turnover_ratio).filter(valuation.code.in_([security]))
    tr = get_fundamentals_continuously(query_filter, end_date=date, count=30, panel=False)['turnover_ratio']

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
    query_filter = query(valuation.turnover_ratio).filter(valuation.code.in_([security]))
    tr = get_fundamentals_continuously(query_filter, end_date=date, count=30, panel=False)['turnover_ratio']
    return tr



#get 10days return
def get_return10(security, date):
    a = get_price(security, count = 30, end_date=date, frequency='daily',
               fields=['open', 'close', 'low', 'high', 'volume'],
               skip_paused=True, fq='none',  panel=False, fill_paused=True)



## get the return rate

def get_return1(df):
    X = df.loc['close']
    X_0 = X[:-1].values.tolist()
    print(X_0)
    X_1 = X[1:].values.tolist()
    returnrate = [(X_1[i]-X_0[i])/X_0[i] for i in range(len(X_0))]
    print(returnrate)
    df_new = df.drop(df.columns[[0]], axis = 1)
    df_new.loc['return1'] = returnrate
    return df_new


#combine to form a matrix of 9*30
def combine930matrix(date):
    df = getfundamental(security,date)
    df2 = calculate_rateCM_30_days(security,date)
    df3 = get_turnover(security, date)

    df['RateCM'] = df2['RateCM']
    df['turnover'] = pd.Series(df3).values
    df = df.T
    df = get_return1(df)
    return df

#generate input matrix of 1 year
def inputmatrix():
    # Define the financial market calendar (e.g., NYSE)
    calendar = get_calendar('XSHG')
    # Set the end date as the current date
    end_date = pd.Timestamp.now(tz='UTC')
    # Calculate the start date as 1 year ago from the end date
    start_date = end_date - pd.DateOffset(years=1)
    # Get the trading days within the specified date range
    trading_days = calendar.sessions_in_range(start_date, end_date)
    # Filter trading days with at least 2 days in between
    filtered_trading_days = [day for i, day in enumerate(trading_days[:-2]) if (trading_days[i + 2] - day).days >= 2]
    list_of_dfs = []
    for date in filtered_trading_days:
        list_of_dfs = list_of_dfs + [combine930matrix(date)]
    return list_of_dfs

if __name__ == "__main__":
    count = get_query_count()
    print(count)
    print("HelloWorld!")
    print(combine930matrix('2023-1-10'))

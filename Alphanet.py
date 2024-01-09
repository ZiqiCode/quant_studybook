from jqdatasdk import *
import numpy as np
import pandas as pd
from datetime import time
auth('18813155136','AlphaNet666')

security = '601127.XSHG'
print(get_security_info(security).display_name)

df = get_price(security, count = 30, end_date='2023-10-1', frequency='daily',
               fields=['open', 'close', 'low', 'high', 'volume'],
               skip_paused=True, fq='none',  panel=False, fill_paused=True)

print(df)



q = query(valuation).filter(valuation.code == '601127.XSHG')
df_2 = get_fundamentals(q, '2023-1-10')
print(df_2['turnover_ratio'].values)

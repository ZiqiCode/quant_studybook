

q = query(valuation).filter(valuation.code == '601127.XSHG')
df_2 = get_fundamentals(q, '2023-1-10')
print(df_2['turnover_ratio'].values)

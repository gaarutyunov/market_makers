import pandas as pd
market_makers = pd.read_excel('/Users/germanarutyunov/PycharmProjects/market_makers/input/market_makers.xls')
market_makers = market_makers[:-3]
market_makers = market_makers.drop(columns=['№'])

import pandas as pd
from main import MAIN
import os
my_file = os.path.join(MAIN, 'input', 'market_makers.xls')
market_makers = pd.read_excel(my_file)
market_makers = market_makers[:-3]
market_makers = market_makers.drop(columns=['№'])
securities_key = market_makers.keys()[2]
market_makers = market_makers.dropna(subset=[securities_key])

sec_path = os.path.join(MAIN, 'output', 'securities.csv')
sec_file = pd.read_csv(sec_path, encoding='UTF-8')
sec_file = sec_file.dropna()\
    .reset_index(inplace=False)\
    .drop(columns=['index'])\
    .drop(columns=[sec_file.columns[0]])\
    .reset_index()

column = sec_file.columns[1]

market_makers_merged = pd.merge(market_makers, sec_file, how='inner', on=column).drop(columns=['index'])


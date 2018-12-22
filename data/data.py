import pandas as pd
from main import MAIN
import os
my_file = os.path.join(MAIN, 'input', 'market_makers.xls')
market_makers = pd.read_excel(my_file)
market_makers = market_makers[:-3]
market_makers = market_makers.drop(columns=['№'])

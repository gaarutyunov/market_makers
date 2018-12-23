import pandas as pd
from helpers.get_data import *


def get_sec(dt, path):
    dt.rename({'Торговый код ценной бумаги': 'code'})
    securities_df = pd.DataFrame(columns=['code', 'market', 'engine', 'board'])

    for index in range(0, len(dt)):
        search_code = dt.iloc[index, 5]
        data = get_data(search_code)
        code = get_code(data)
        market = get_market(data)
        engine = get_engine(data)
        board = get_board(data)
        securities_df.loc[index] = [code, market, engine, board]
        print(str(index + 1) + ' from ' + str(len(data)) + ', left: ' + str(len(dt) - index - 1))

    securities_df.to_csv(path, encoding='UTF-8')

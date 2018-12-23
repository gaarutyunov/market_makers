import pandas as pd
from data import securities_key, sec_path
from bonds import bonds_nd as market_makers
from helpers.get_data import *
securities_df = pd.DataFrame(columns=[securities_key, 'code', 'market', 'engine', 'board'])

for index in range(0, len(market_makers)):
    search_code = market_makers.iloc[index, 0]
    data = get_data(search_code)
    code = get_code(data)
    market = get_market(data)
    engine = get_engine(data)
    board = get_board(data)
    securities_df.loc[index] = [search_code, code, market, engine, board]
    print(str(index + 1) + ' from ' + str(len(market_makers)) + ', left: ' + str(len(market_makers) - index - 1))

securities_df.to_csv(sec_path, encoding='UTF-8')

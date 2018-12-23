from liquidity import concat_df
from helpers.fetch import get_data_asynchronous
import os
from main import MAIN
import pandas as pd
import asyncio
PATH = os.path.join(MAIN, 'output', 'securities_liquidity.csv')
PATH_HIS = os.path.join(MAIN, 'output', 'history_liquidity')

df = concat_df
file = pd.read_csv(PATH)
file = file.dropna()\
        .reset_index(inplace=False)\
        .drop(columns=['index'])\
        .drop(columns=[file.columns[0]])\
        .reset_index()


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(PATH_HIS, file))
    loop.run_until_complete(future)


main()

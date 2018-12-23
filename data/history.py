from helpers.fetch import get_data_asynchronous
import asyncio
import os
from data import MAIN
from data import sec_path, MAIN
import pandas as pd

PATH = os.path.join(MAIN, 'output', 'history')
sec_file = pd.read_csv(sec_path, encoding='UTF-8')
sec_file = sec_file.dropna()\
    .reset_index(inplace=False)\
    .drop(columns=['index'])\
    .drop(columns=[sec_file.columns[0]])\
    .reset_index()


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(PATH, sec_file))
    loop.run_until_complete(future)


main()

import asyncio
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from main import API, DATE, OUTPUT
import csv
import io
import pandas as pd

START_TIME = default_timer()


def fetch(session, sec):
    code = sec['code']
    market = sec['market']
    engine = sec['engine']
    board = sec['board']
    url = API + 'history/' + 'engines/' + engine + \
        '/markets/' + market + '/boards/' + board + \
        '/securities/' + str(code) + '.csv' + '?from=' + DATE
    with session.get(url) as response:
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))
        data = response.content
        elapsed = default_timer() - START_TIME
        time_completed_at = "{:5.2f}s".format(elapsed)
        print("{0:<30} {1:>20}".format(str(code) + '.csv', time_completed_at))
        return {str(code): data}


async def get_data_asynchronous(path, df):
    length = len(df)
    df = df.replace({'ppif': 'shares', 'etf': 'shares', 'dr': 'shares'})
    print("{0:<30} {1:>20}".format("File", "Completed at"))
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, df.iloc[i, :])
                )
                for i in range(0, len(df))
            ]
            for response in await asyncio.gather(*tasks):
                key = list(response.keys())[0]
                value = response.get(key)
                rawData = pd.read_csv(io.StringIO(value.decode('windows 1251')), sep=';', skiprows=1)
                rawData.to_csv(os.path.join(path, key + '.csv'))

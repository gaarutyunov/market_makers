from data import sec_path, MAIN
import pandas as pd
import asyncio
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from main import API, DATE
import csv

START_TIME = default_timer()

sec_file = pd.read_csv(sec_path, encoding='UTF-8')
sec_file = sec_file.dropna()\
    .reset_index(inplace=False)\
    .drop(columns=['index'])\
    .drop(columns=[sec_file.columns[0]])\
    .reset_index()
length = len(sec_file)


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
        data = response.text
        elapsed = default_timer() - START_TIME
        time_completed_at = "{:5.2f}s".format(elapsed)
        print("{0:<30} {1:>20}".format(str(code) + '.csv', time_completed_at))
        return {str(code): data}


async def get_data_asynchronous():
    print("{0:<30} {1:>20}".format("File", "Completed at"))
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, sec_file.iloc[i, :])
                )
                for i in range(0, length)
            ]
            for response in await asyncio.gather(*tasks):
                key = list(response.keys())[0]
                value = response.get(key)
                with open(os.path.join(MAIN, 'output', 'history', key + '.csv'), 'w', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    reader = csv.reader(value.splitlines())
                    for row in reader:
                        writer.writerow(row)


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)


main()

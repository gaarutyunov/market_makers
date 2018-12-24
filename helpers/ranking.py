import asyncio
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from main import API, DATE, OUTPUT, INPUT
import pandas as pd
import numpy as np
from helpers.get_data import get_data, get_code
START_TIME = default_timer()


def get_percent(value_b, value_s):
    pct = float(value_s) / float(value_b)
    print(pct)
    return '{0:.2%}'.format(pct)


def get_dates(name):
    data = get_data(name)
    name = get_code(data)
    df = pd.read_csv(os.path.join(OUTPUT, 'history', name + '.csv'))
    new_df = df[['TRADEDATE', 'VOLUME']]
    new_df = new_df.set_index(new_df.columns[0])
    return new_df


def fetch(session, program, name):
    dates_df = get_dates(name)
    data = get_data(name)
    name = get_code(data)
    new_df = pd.DataFrame(columns=['VOLUME_MM'], index=dates_df.index)
    for date in dates_df.index.values:
        url = API\
              + 'statistics/engines/stock/mmakers/ranks/types/'\
              + str(program) + '.jsonp?securities=' + str(name) + '&date=' + str(date) + '&ranks.columns=VOLUME'
        with session.get(url) as response:
            if response.status_code != 200:
                print("FAILURE::{0}".format(url))
            data = response.json()['ranks']['data']
            elapsed = default_timer() - START_TIME
            time_completed_at = "{:5.2f}s".format(elapsed)
            print("{0:<30} {1:>20}".format(name + '.jsonp', time_completed_at))
            values = [i[0] for i in data]
            values_sum = sum(values)
            new_df.loc[date] = values_sum
    merged_df = pd.concat([dates_df, new_df], axis=1)
    merged_df['PERCENTAGE'] = (merged_df['VOLUME_MM'] / merged_df['VOLUME']) * 100
    merged_df = merged_df.round({'PERCENTAGE': 2})
    merged_df = merged_df.rename(index=str,
                                 columns={'VOLUME_MM': 'Объем сделок Маркет-мейкеров, в шт. ценных бумаг',
                                          'VOLUME': 'Объем всех сделок, в шт. ценных бумаг',
                                          'PERCENTAGE': 'Процент сделок ММ среди всех сделок, в %',
                                          'TRADEDATE': 'Дата'})
    return {name: merged_df}


async def get_data_asynchronous(program):
    path = os.path.join(INPUT, program + '.csv')
    df = pd.read_csv(path, encoding='windows-1251', sep=';')
    print("{0:<30} {1:>20}".format("File", "Completed at"))
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, program, df.iloc[i, 0])
                )
                for i in range(0, len(df))
            ]
            for response in await asyncio.gather(*tasks):
                key = list(response.keys())[0]
                response = response.get(key)
                response.to_csv(os.path.join(OUTPUT, 'statistics', program, key + '.csv'))

import asyncio
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from main import API, DATE, OUTPUT, INPUT
import pandas as pd
import numpy as np
START_TIME = default_timer()


def get_percent(value_b, value_s):
    pct = float(value_s) / float(value_b)
    print(pct)
    return '{0:.2%}'.format(pct)


def get_dates(name):
    df = pd.read_csv(os.path.join(OUTPUT, 'history', name + '.csv'))
    df = df.sort_values(by='VOLUME', ascending=False).reset_index()
    best_date = df['TRADEDATE'][0]
    best_value = df['VOLUME'][0]
    worst_date = df['TRADEDATE'][len(df) - 1]
    worst_value = df['VOLUME'][len(df) - 1]
    values = {'sec_data': {
                    'dates': {
                        'best_date': best_date,
                        'worst_date': worst_date
                    },
                    'values': {
                        'best_date': best_value,
                        'worst_date': worst_value
                    }},
              'mm_data': {
                    'dates': {
                        'best_date': best_date,
                        'worst_date': worst_date
                    },
                    'values': {
                        'best_date': 0,
                        'worst_date': 0
              }}}
    return values


def fetch(session, program, name):
    datas = get_dates(name)
    for key, value in datas['sec_data']['dates'].items():
        url = API\
              + 'statistics/engines/stock/mmakers/ranks/types/'\
              + str(program) + '.jsonp?securities=' + str(name) + '&date=' + str(value) + '&ranks.columns=VOLUME'
        with session.get(url) as response:
            if response.status_code != 200:
                print("FAILURE::{0}".format(url))
            data = response.json()['ranks']['data']
            elapsed = default_timer() - START_TIME
            time_completed_at = "{:5.2f}s".format(elapsed)
            print("{0:<30} {1:>20}".format(name + '.jsonp', time_completed_at))
            values = [i[0] for i in data]
            values_sum = sum(values)
            datas['mm_data']['values'][key] = values_sum
    return {name: datas}


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
                best_date = response['sec_data']['dates']['best_date']
                worst_date = response['sec_data']['dates']['worst_date']
                best_value_sec = response['sec_data']['values']['best_date']
                worst_value_sec = response['sec_data']['values']['worst_date']
                best_value_mm = response['mm_data']['values']['best_date']
                worst_value_mm = response['mm_data']['values']['worst_date']
                np_array = np.array([
                    [best_value_sec, best_value_mm, get_percent(best_value_sec, best_value_mm)],
                    [worst_value_sec, worst_value_mm, get_percent(worst_value_sec, worst_value_mm)]])
                dataframe = pd.DataFrame(np_array,
                                         index=[best_date, worst_date],
                                         columns=['Объем всего', 'Объем маркет-мейкер', 'Процент'])
                dataframe.to_csv(os.path.join(OUTPUT, 'statistics', program, key + '.csv'))


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous('eq'))
    loop.run_until_complete(future)


main()

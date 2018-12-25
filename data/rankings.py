from helpers.ranking import get_data_asynchronous
import asyncio
from main import OUTPUT, INPUT
import os
import pandas as pd

STAT = os.path.join(OUTPUT, 'statistics')


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous('ofz2'))
    loop.run_until_complete(future)


def extract_mean(program, name):
    path = os.path.join(STAT, program, name + '.csv')
    df = pd.read_csv(path)
    percent = df.iloc[:, -1]
    percentage = '{:.1f}%'.format(percent.mean())
    return percentage


def create_df(program):
    path = os.path.join(INPUT, program + '.csv')
    df = pd.read_csv(path, encoding='windows 1251', sep=';')
    names = list(df.iloc[:, 0])
    new_df = pd.DataFrame(index=names, columns=['Средний процент'])
    for name in names:
        percent = extract_mean(program, name)
        new_df.loc[name] = percent
    return new_df


def save_data(program):
    path = os.path.join(STAT, program)
    df = create_df('bbo')
    df.to_csv(os.path.join(path, 'mean.csv'))


programs = ['bbo', 'eq', 'ofz1', 'ofz2']
for x in programs:
    save_data(x)

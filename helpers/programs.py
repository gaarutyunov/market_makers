import pandas as pd
from main import MAIN, OUTPUT, INPUT
import os


def get_volumes(program):
    bb_bo_df = pd.read_csv(os.path.join(INPUT, program + '.csv'), encoding='windows 1251', sep=';')
    codes = bb_bo_df.iloc[:, 0]
    codes = list(codes)
    ex_d = pd.read_csv(os.path.join(OUTPUT, 'history', 'AFLT.csv'), sep=',')
    ex_d_1 = list(ex_d['TRADEDATE'])
    start_df = pd.DataFrame(columns=[codes], index=ex_d_1)
    for code in codes:
        dates = pd.read_csv(os.path.join(OUTPUT, 'history', code + '.csv'), sep=',')
        dates_2 = list(dates['TRADEDATE'])
        dates_1 = dates[['TRADEDATE', 'VOLUME']]
        i = 0
        for date in dates_2:
            value = dates_1[dates_1['TRADEDATE'] == date]['VOLUME'][i]
            start_df.set_value(col=code, value=value, index=date)
            i += 1
    start_df.to_csv(os.path.join(OUTPUT, 'programs', program + '.csv'), encoding='UTF-8', sep=',')

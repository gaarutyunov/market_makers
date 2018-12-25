from main import *
from data import market_makers_merged
import pandas as pd
from helpers.get_data import *


def return_df(program):
    return pd.read_csv(os.path.join(INPUT, program + '.csv'), encoding='windows 1251', sep=';')


def return_codes(df):
    return df.iloc[:, 0].to_frame('code')


def return_code(name):
    data = get_data(name)
    return get_code(data)


def replace_codes(df):
    codes = df['code'].tolist()
    new_df = pd.DataFrame([return_code(x) for x in codes], columns=['code'])
    return new_df


def get_volumes(program, df):
    cds = df.iloc[:, 0].tolist()
    ex_d = pd.read_csv(os.path.join(OUTPUT, 'history', 'AFLT.csv'), sep=',')
    ex_d_1 = list(ex_d['TRADEDATE'])
    start_df = pd.DataFrame(columns=cds, index=ex_d_1)
    for code in cds:
        dates = pd.read_csv(os.path.join(OUTPUT, 'history', code + '.csv'), sep=',')
        dates_2 = list(dates['TRADEDATE'])
        dates_1 = dates[['TRADEDATE', 'VOLUME']]
        i = 0
        for date in dates_2:
            value = dates_1[dates_1['TRADEDATE'] == date]['VOLUME'][i]
            start_df.set_value(col=code, value=value, index=date)
            i += 1
    start_df.to_csv(os.path.join(OUTPUT, 'programs', program + '.csv'), encoding='UTF-8', sep=',')


all_df = market_makers_merged
codes = all_df['code'].to_frame('code')
bbo_df = return_df('bbo')
eq_df = return_df('eq')
ofz1_df = return_df('ofz1')
codes_bbo = return_codes(bbo_df)
codes_eq = return_codes(eq_df)
codes_ofz = return_codes(ofz1_df)
codes_ofz = replace_codes(codes_ofz)
codes = pd.concat([codes, codes_bbo, codes_eq, codes_ofz], axis=0)
codes = codes.drop_duplicates(keep=False).reset_index(inplace=False).drop(columns=['index'])

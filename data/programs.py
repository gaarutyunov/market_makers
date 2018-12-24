from main import INPUT, OUTPUT
import pandas as pd
import os

bb_bo_df = pd.read_csv(os.path.join(INPUT, 'bb-bo.csv'), encoding='windows 1251', sep=';')
code = bb_bo_df.iloc[:, 0]
dates = pd.read_csv(os.path.join(OUTPUT, 'history', 'AFLT.csv'), sep=',')
dates1 = dates.iloc[0]
# dates = dates.iloc[:, 1]
# new_df = pd.DataFrame(['code', ])

# for cd in code:
#     csv = pd.read_csv(os.path.join(OUTPUT, 'history', cd))

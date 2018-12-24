from main import OUTPUT
import os
import pandas as pd
from helpers.programs import get_volumes
from helpers.utils import create_plot

# get_volumes('shares_program')

programs_path = os.path.join(OUTPUT, 'programs')

df = pd.read_csv(os.path.join(programs_path, 'bb-bo.csv'))
df = df.set_index(df.columns[0])
# df = df.drop(columns=['VTBR'])
# df = df.reindex_axis(df.mean().sort_values().index, axis=1)
# df = df[df > 100000]
# df = df.dropna(axis='columns')
# df1 = df.iloc[:, :10]
# df2 = df.iloc[:, 10:]

create_plot(df, 'Программа Best Bid/Best Offer', 1000000)

# create_plot(df1, 'Открытая программа по поддержанию цены для группы ликвидных акций_1', 1000)
# create_plot(df2, 'Открытая программа по поддержанию цены для группы ликвидных акций_2', 1000000)

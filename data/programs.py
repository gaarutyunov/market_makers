from main import OUTPUT
import os
import pandas as pd
from helpers.programs import get_volumes
from helpers.utils import create_plot

get_volumes('bb-bo')

programs_path = os.path.join(OUTPUT, 'programs')

df = pd.read_csv(os.path.join(programs_path, 'bb-bo.csv'))
df = df.set_index(df.columns[0])
df = df.drop(columns=['VTBR'])


create_plot(df, 'Программа Best Bid/Best Offer')

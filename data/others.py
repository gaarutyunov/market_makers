from main import *
import pandas as pd
import os
from helpers.utils import create_plot

df = pd.read_csv(os.path.join(OUTPUT, 'programs', 'no_program.csv'))
df = df.set_index(df.columns[0])


df = df.fillna(0)
names = df.columns.values
names_bonds = [name for name in names if len(name) > 4]
names_shares = [name for name in names if len(name) == 4]
bonds = df[names_bonds]
shares = df[names_shares]
big_shares_names = ['MRKC', 'MRKP', 'YNDX', 'RGSS']
shares = shares.drop(columns=big_shares_names)
big_shares = df[big_shares_names].drop(columns='MRKP')

# create_plot(bonds, 'Облигации, не допущенные до программ', 1)
create_plot(shares, 'Ценные бумаги, не допущенные до программ', 1000)
# create_plot(big_shares, 'Акции и ДР крупных компаний, не допущенные до программ', 1000)


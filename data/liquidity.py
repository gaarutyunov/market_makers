from main import MAIN
import os
import pandas as pd
from data import sec_file
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

input_folder = os.path.join(MAIN, 'input')
bonds_l = pd.read_csv(os.path.join(input_folder, 'bonds_l.csv'), sep=';')
bonds_l['liquidity'] = 'l'
bonds_nl = pd.read_csv(os.path.join(input_folder, 'bonds_nl.csv'), sep=';')
bonds_nl['liquidity'] = 'nl'
ppif_l = pd.read_csv(os.path.join(input_folder, 'ppif_l.csv'), sep=';')
ppif_l['liquidity'] = 'l'
ppif_nl = pd.read_csv(os.path.join(input_folder, 'ppif_nl.csv'), sep=';')
ppif_nl['liquidity'] = 'nl'
shares_l = pd.read_csv(os.path.join(input_folder, 'shares_l.csv'), sep=';')
shares_l['liquidity'] = 'l'
shares_nl = pd.read_csv(os.path.join(input_folder, 'shares_nl.csv'), sep=';')
shares_nl['liquidity'] = 'nl'

securities = sec_file

concat_df = bonds_l.append([bonds_nl, ppif_l, ppif_nl, shares_l, shares_nl], ignore_index=True, sort=False)
concat_num = len(concat_df)
by_type = concat_df[['Тип ценной бумаги', 'liquidity']].rename(index=str, columns={'liquidity': 'Ликвидность'})
l_counted = by_type.groupby('Ликвидность').count().rename(index={'l': 'Ликвидные', 'nl': 'Низколиквидные'})

merged_df = securities.merge(concat_df, right_on='Торговый код ценной бумаги', left_on='code', how='inner')


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:d}".format(absolute)


labels = [l_counted.index[i] for i in range(0, len(l_counted))]
values = l_counted.values
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts, autotexts = ax.pie(values, autopct=lambda pct: func(pct, values),
                                  textprops=dict(color="w"))
ax.legend(wedges, labels,
          title="Ликвидность",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
plt.setp(autotexts, size=8, weight="bold")

ax.set_title('Все ценные бумаги')
plt.show()

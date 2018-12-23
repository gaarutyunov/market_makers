from main import MAIN
import os
import pandas as pd
from data import sec_file
from helpers.utils import *


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
concat_shares = shares_l.append(shares_nl)
concat_bonds = bonds_l.append(bonds_nl)
concat_ppif = ppif_l.append(ppif_nl)
concat_num = len(concat_df)
l_counted = group(concat_df, False)
shares_counted = group(concat_shares)
bonds_counted = group(concat_bonds)
ppif_counted = group(concat_ppif)

merged_df = securities.merge(concat_df, right_on='Торговый код ценной бумаги', left_on='code', how='inner')

create_pie(l_counted)
create_pie(shares_counted)
create_pie(bonds_counted)
create_pie(ppif_counted)

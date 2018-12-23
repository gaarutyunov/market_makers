from data import market_makers

bonds = market_makers.iloc[:, 2]
bonds_nd = bonds.drop_duplicates().reset_index(inplace=False).drop(columns=['index'])

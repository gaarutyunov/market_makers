from data.data import market_makers

bonds = market_makers.iloc[:, 3]
bonds_nd = bonds.drop_duplicates().reset_index(inplace=False)

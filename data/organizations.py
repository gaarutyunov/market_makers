from data.data import market_makers
organizations = market_makers.iloc[:, 1]
organizations_nd = organizations.drop_duplicates().reset_index(inplace=False)
organizations_number = len(organizations_nd)

from data import market_makers
organizations = market_makers.iloc[:, 1]
organizations_nd = organizations.drop_duplicates().reset_index(inplace=False).drop(columns=['index'])
organizations_number = len(organizations_nd)
print(organizations_nd.iloc[6, 0])

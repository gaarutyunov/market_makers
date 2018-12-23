from data import market_makers
issuers = market_makers.iloc[:, 2]
issuers_nd = issuers.drop_duplicates().reset_index(inplace=False).drop(columns=['index'])
issuers_number = len(issuers_nd)

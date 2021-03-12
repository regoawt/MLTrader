from data import QuandlApiData, FredApiData


# test = QuandlApiData('BITFINEX/BTCUSD', start_date='2014-04-15').remove(['Mid', 'Last', 'Bid', 'Ask'])
# print(test.df.tail())

treasury = FredApiData('DGS10', start_date='2020-04-15', series_name='10Y Treasury')
print(treasury.df.head())

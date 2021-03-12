import quandl
import pandas as pd
import numpy as np
from fredapi import Fred

class AbstractApiData():
    '''Base data API class'''

    def __init__(self, api_code, start_date, series_name=None):
        self.api_code = api_code
        self.series_name = series_name

    def remove(self, column_names):
        self.df.drop(columns = column_names, inplace=True)
        return self

    def include(self, column_names):
        self.df = self.df[column_names]
        return self


class QuandlApiData(AbstractApiData):
    '''Quandl data API class'''

    def __init__(self, api_code, start_date, series_name=None):
        super().__init__(api_code, start_date, series_name=series_name)

        with open('ignore_folder/quandl_api_key.txt','r') as file:
            key = file.read().replace('\n', '')
        quandl.ApiConfig.api_key = key
        self.df = pd.DataFrame(quandl.get(self.api_code, start_date=start_date))


class FredApiData(AbstractApiData):
    '''Fred data API class'''

    def __init__(self, api_code, start_date, series_name=None):
        super().__init__(api_code, start_date, series_name=series_name)

        with open('ignore_folder/fred_api_key.txt','r') as file:
            key = file.read().replace('\n', '')
        self.fred = Fred(api_key = key)
        self.df = pd.DataFrame(self.fred.get_series(self.api_code)).loc[start_date::]
        self.df.columns = [self.series_name]

import requests
import pandas as pd

class LifeExpectancy:
    def __init__(self, country_code='CAN'):
        self.country_code = country_code
        self._data = None

    def _fetch(self):
        if self._data is None:
            url = f'https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim%20eq%20%27{self.country_code}%27'
            response = requests.get(url).json()
            self._data = pd.DataFrame(response['value']).dropna(axis=1, how='all')
        return self._data

    def get_male(self):
        df = self._fetch()
        result = df.loc[df['Dim1'] == 'SEX_MLE', ['TimeDim', 'NumericValue']]
        return result.sort_values(by='TimeDim')

    def get_female(self):
        df = self._fetch()
        result = df.loc[df['Dim1'] == 'SEX_FMLE', ['TimeDim', 'NumericValue']]
        return result.sort_values(by='TimeDim')

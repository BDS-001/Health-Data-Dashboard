import requests
import pandas as pd

class LifeExpectancy:
    _all_data = None

    def __init__(self, country_code='CAN'):
        self.country_code = country_code

    @classmethod
    def _fetch_all(cls):
        if cls._all_data is None:
            url = 'https://ghoapi.azureedge.net/api/WHOSIS_000001'
            response = requests.get(url).json()
            cls._all_data = pd.DataFrame(response['value']).dropna(axis=1, how='all')
        return cls._all_data

    @classmethod
    def get_countries(cls):
        """Fetch available countries with names"""
        url = 'https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues'
        response = requests.get(url).json()
        all_countries = {item['Code']: item['Title'] for item in response['value']}

        codes = cls._fetch_all()['SpatialDim'].unique()

        return {all_countries[code]: code for code in codes if code in all_countries}

    def get_male(self):
        df = self._fetch_all()
        result = df.loc[
            (df['SpatialDim'] == self.country_code) & (df['Dim1'] == 'SEX_MLE'),
            ['TimeDim', 'NumericValue']
        ]
        return result.sort_values(by='TimeDim').rename(columns={'TimeDim': 'Year', 'NumericValue': 'Life Expectancy'})

    def get_female(self):
        df = self._fetch_all()
        result = df.loc[
            (df['SpatialDim'] == self.country_code) & (df['Dim1'] == 'SEX_FMLE'),
            ['TimeDim', 'NumericValue']
        ]
        return result.sort_values(by='TimeDim').rename(columns={'TimeDim': 'Year', 'NumericValue': 'Life Expectancy'})

    @classmethod
    def get_years(cls):
        df = cls._fetch_all()
        return sorted(df['TimeDim'].unique())

    @classmethod
    def get_by_year(cls, year):
        df = cls._fetch_all()
        result = df.loc[
            (df['Dim1'] == 'SEX_BTSX') & (df['TimeDim'] == year),
            ['SpatialDim', 'NumericValue']
        ]
        return result.sort_values(by='NumericValue', ascending=False).rename(columns={'SpatialDim': 'Country', 'NumericValue': 'Life Expectancy'})

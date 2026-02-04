import requests
import pandas as pd

class LifeExpectancy:
    _all_data = None

    def __init__(self, country='Canada'):
        self.country = country

    @classmethod
    def _fetch_all(cls):
        if cls._all_data is None:
            url = 'https://ghoapi.azureedge.net/api/WHOSIS_000001'
            response = requests.get(url).json()
            df = pd.DataFrame(response['value']).dropna(axis=1, how='all')

            country_url = 'https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues'
            country_response = requests.get(country_url).json()
            code_to_name = {item['Code']: item['Title'] for item in country_response['value']}

            df['SpatialDim'] = df['SpatialDim'].map(code_to_name)
            df = df.dropna(subset=['SpatialDim'])
            df = df.rename(columns={
                'SpatialDim': 'Country',
                'TimeDim': 'Year',
                'NumericValue': 'Life Expectancy',
                'Dim1': 'Sex'
            })

            cls._all_data = df
        return cls._all_data

    @classmethod
    def get_countries(cls):
        df = cls._fetch_all()
        return sorted(list(df['Country'].unique()))

    def get_male(self):
        df = self._fetch_all()
        result = df.loc[
            (df['Country'] == self.country) & (df['Sex'] == 'SEX_MLE'),
            ['Year', 'Life Expectancy']
        ]
        return result.sort_values(by='Year')

    def get_female(self):
        df = self._fetch_all()
        result = df.loc[
            (df['Country'] == self.country) & (df['Sex'] == 'SEX_FMLE'),
            ['Year', 'Life Expectancy']
        ]
        return result.sort_values(by='Year')

    @classmethod
    def get_years(cls):
        df = cls._fetch_all()
        return sorted(df['Year'].unique())

    @classmethod
    def get_by_year(cls, year):
        df = cls._fetch_all()
        result = df.loc[
            (df['Sex'] == 'SEX_BTSX') & (df['Year'] == year),
            ['Country', 'Life Expectancy']
        ]
        return result.sort_values(by='Life Expectancy', ascending=False)

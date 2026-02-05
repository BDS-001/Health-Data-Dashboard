import requests
import pandas as pd
from data.countries import COUNTRY_CODES

class HealthcareSpending:
    INDICATORS = {
        'spending_per_capita': 'GHED_CHE_pc_US_SHA2011',
        'spending_gdp': 'GHED_CHEGDP_SHA2011',
        'out_of_pocket': 'GHED_OOPSCHE_SHA2011',
        'gov_spending': 'GHED_GGHE-DCHE_SHA2011',
    }

    _spending_per_capita = None
    _spending_gdp = None
    _out_of_pocket = None
    _gov_spending = None

    def __init__(self, country='Canada'):
        self.country = country

    @classmethod
    def _fetch(cls, indicator_key):
        if getattr(cls, f"_{indicator_key}") is None:
            url = f'https://ghoapi.azureedge.net/api/{cls.INDICATORS[indicator_key]}'
            response = requests.get(url).json()
            df = pd.DataFrame(response['value']).dropna(axis=1, how='all')

            df['SpatialDim'] = df['SpatialDim'].map(COUNTRY_CODES)
            df = df.dropna(subset=['SpatialDim'])
            df = df.rename(columns={
                'SpatialDim': 'Country',
                'TimeDim': 'Year',
                'NumericValue': 'Value'
            })

            setattr(cls, f'_{indicator_key}', df)
        return getattr(cls, f"_{indicator_key}")

    def get_spending_per_capita(self):
        df = self._fetch('spending_per_capita')
        result = df.loc[df['Country'] == self.country, ['Year', 'Value']]
        return result.sort_values(by='Year')

    def get_spending_gdp(self):
        df = self._fetch('spending_gdp')
        result = df.loc[df['Country'] == self.country, ['Year', 'Value']]
        return result.sort_values(by='Year')

    def get_out_of_pocket(self):
        df = self._fetch('out_of_pocket')
        result = df.loc[df['Country'] == self.country, ['Year', 'Value']]
        return result.sort_values(by='Year')

    def get_gov_spending(self):
        df = self._fetch('gov_spending')
        result = df.loc[df['Country'] == self.country, ['Year', 'Value']]
        return result.sort_values(by='Year')

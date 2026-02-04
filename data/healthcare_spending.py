import requests
import pandas as pd

class HealthcareSpending:
    INDICATORS = {
        'spending_per_capita': 'GHED_CHE_pc_US_SHA2011',
        'spending_gdp': 'GHED_CHEGDP_SHA2011',
        'out_of_pocket': 'GHED_OOPSCHE_SHA2011',
        'gov_spending': 'GHED_GGHE-DCHE_SHA2011',
    }

    def __init__(self, country_code='CAN'):
        self.country_code = country_code
        self._spending_per_capita = None
        self._spending_gdp = None
        self._out_of_pocket = None
        self._gov_spending = None

    def _fetch(self, indicator_key):
        if getattr(self, f"_{indicator_key}") is None:
            url = f'https://ghoapi.azureedge.net/api/{self.INDICATORS[indicator_key]}'
            response = requests.get(url).json()
            data = pd.DataFrame(response['value']).dropna(axis=1, how='all')
            setattr(self, f'_{indicator_key}', data)
        return getattr(self, f"_{indicator_key}")

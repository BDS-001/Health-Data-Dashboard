import requests
import pandas as pd

def getData():
    df = pd.DataFrame()
    data = requests.get('https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim%20eq%20%27CAN%27').json()
    df = pd.DataFrame(data['value']).dropna(axis=1, how='all')
    final = df.loc[df['Dim1'] == 'SEX_MLE', ['TimeDim', 'NumericValue']]
    final = final.sort_values(by='TimeDim')
    return final

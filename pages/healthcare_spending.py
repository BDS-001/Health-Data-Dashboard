import streamlit as st
import plotly.express as px
import pandas as pd
from data.healthcare_spending import HealthcareSpending
from data.life_expectancy import LifeExpectancy
from utils.charts import add_trendline

st.title('Healthcare Spending')

countries = LifeExpectancy.get_countries()
default_index = countries.index('Canada') if 'Canada' in countries else 0
country = st.selectbox('Select Country', countries, index=default_index)

spending_data = HealthcareSpending(country)
life_data = LifeExpectancy(country)
life_exp_data = life_data.get_both()

indicators = [
    ('Spending Per Capita', spending_data.get_spending_per_capita()),
    ('Spending GDP', spending_data.get_spending_gdp()),
    ('Out of Pocket', spending_data.get_out_of_pocket()),
    ('Gov Spending', spending_data.get_gov_spending()),
]

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

for col, (title, spending_df) in zip([col1, col2, col3, col4], indicators):
    with col:
        st.header(title)
        combined = pd.merge(spending_df, life_exp_data, on='Year')
        fig = px.scatter(combined, x='Life Expectancy', y='Spending', text='Year', title=title)
        fig.update_traces(textposition='top center')
        fig, r = add_trendline(fig, combined['Life Expectancy'], combined['Spending'])
        st.plotly_chart(fig, width='stretch')
        st.caption(f'Correlation(r) = {r:.2f}')

st.divider()
st.header('Spending Efficiency')

efficiency_data = pd.merge(indicators[0][1], life_exp_data, on='Year')
efficiency_data['Efficiency'] = efficiency_data['Life Expectancy'] / efficiency_data['Spending']

fig_eff = px.line(
    efficiency_data, x='Year', y='Efficiency',
    title='Life Expectancy per Dollar Spent (Per Capita)'
)
fig_eff.update_yaxes(title='Years of Life Expectancy / $')
st.plotly_chart(fig_eff, width='stretch')
st.dataframe(efficiency_data[['Year', 'Life Expectancy', 'Spending', 'Efficiency']])
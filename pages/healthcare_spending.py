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

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.header('Spending Per Capita')
    per_capita_data = spending_data.get_spending_per_capita()
    life_exp_data = life_data.get_both()
    combined = pd.merge(per_capita_data, life_exp_data, on='Year')
    fig = px.scatter(combined, x='Life Expectancy', y='Spending', text='Year')
    fig.update_traces(textposition='top center')
    add_trendline(fig, combined['Life Expectancy'], combined['Spending'])
    st.plotly_chart(fig, width='stretch')

with col2:
    st.header('Spending GDP')
    gdp_data = spending_data.get_spending_gdp()
    life_exp_data = life_data.get_both()
    combined = pd.merge(gdp_data, life_exp_data, on='Year')
    fig = px.scatter(combined, x='Life Expectancy', y='Spending', text='Year')
    fig.update_traces(textposition='top center')
    add_trendline(fig, combined['Life Expectancy'], combined['Spending'])
    st.plotly_chart(fig, width='stretch')

with col3:
    st.header('Out of Pocket')
    out_of_pocket_data = spending_data.get_out_of_pocket()
    life_exp_data = life_data.get_both()
    combined = pd.merge(out_of_pocket_data, life_exp_data, on='Year')
    fig = px.scatter(combined, x='Life Expectancy', y='Spending', text='Year')
    fig.update_traces(textposition='top center')
    add_trendline(fig, combined['Life Expectancy'], combined['Spending'])
    st.plotly_chart(fig, width='stretch')

with col4:
    st.header('Gov Spending')
    gov_data = spending_data.get_gov_spending()
    life_exp_data = life_data.get_both()
    combined = pd.merge(gov_data, life_exp_data, on='Year')
    fig = px.scatter(combined, x='Life Expectancy', y='Spending', text='Year')
    fig.update_traces(textposition='top center')
    add_trendline(fig, combined['Life Expectancy'], combined['Spending'])
    st.plotly_chart(fig, width='stretch')
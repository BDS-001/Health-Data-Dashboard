import streamlit as st
import plotly.express as px
from data.life_expectancy import LifeExpectancy

st.title('Life Expectancy')

countries = LifeExpectancy.get_countries()
country_list = list(countries.keys())
default_index = country_list.index('Canada') if 'Canada' in country_list else 0
country = st.selectbox('Select Country', country_list, index=default_index)

data = LifeExpectancy(countries[country])

male_data = data.get_male()
female_data = data.get_female()

col1, col2 = st.columns(2)

with col1:
    st.header('Male')
    fig_male = px.line(male_data, x='TimeDim', y='NumericValue', title='Male Life Expectancy')
    st.plotly_chart(fig_male, use_container_width=True)
    st.dataframe(male_data)

with col2:
    st.header('Female')
    fig_female = px.line(female_data, x='TimeDim', y='NumericValue', title='Female Life Expectancy')
    st.plotly_chart(fig_female, use_container_width=True)
    st.dataframe(female_data)

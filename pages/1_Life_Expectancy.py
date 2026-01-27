import streamlit as st
import plotly.express as px
from data.life_expectancy import LifeExpectancy

st.title('Life Expectancy')

country = st.selectbox('Select Country', ['Canada', 'USA'])
country_codes = {'Canada': 'CAN', 'USA': 'USA'}

data = LifeExpectancy(country_codes[country])

# Male
st.header('Male')
male_data = data.get_male()
st.dataframe(male_data)
fig_male = px.line(male_data, x='TimeDim', y='NumericValue', title='Male Life Expectancy Over Time')
st.plotly_chart(fig_male)

# Female
st.header('Female')
female_data = data.get_female()
st.dataframe(female_data)
fig_female = px.line(female_data, x='TimeDim', y='NumericValue', title='Female Life Expectancy Over Time')
st.plotly_chart(fig_female)

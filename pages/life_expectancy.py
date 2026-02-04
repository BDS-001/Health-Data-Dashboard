import streamlit as st
import plotly.express as px
from data.life_expectancy import LifeExpectancy

st.title('Life Expectancy')

countries = LifeExpectancy.get_countries()
default_index = countries.index('Canada') if 'Canada' in countries else 0
country = st.selectbox('Select Country', countries, index=default_index)

data = LifeExpectancy(country)

male_data = data.get_male()
female_data = data.get_female()

col1, col2 = st.columns(2)

with col1:
    st.header('Male')
    fig_male = px.line(male_data, x='Year', y='Life Expectancy', title='Male Life Expectancy')
    st.plotly_chart(fig_male, width='stretch')
    st.dataframe(male_data)

with col2:
    st.header('Female')
    fig_female = px.line(female_data, x='Year', y='Life Expectancy', title='Female Life Expectancy')
    st.plotly_chart(fig_female, width='stretch')
    st.dataframe(female_data)

st.divider()
st.header('Life Expectancy by Country')

years = LifeExpectancy.get_years()
year = st.selectbox('Select Year', years, index=len(years)-1)

year_data = LifeExpectancy.get_by_year(year)


fig_year = px.bar(year_data, x='Country', y='Life Expectancy', title=f'Life Expectancy by Country ({year})')
fig_year.update_yaxes(range=[year_data['Life Expectancy'].min() - 10, year_data['Life Expectancy'].max() + 5])
st.plotly_chart(fig_year, width='stretch')
st.dataframe(year_data)

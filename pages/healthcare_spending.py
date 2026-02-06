import streamlit as st
import plotly.express as px
from data.healthcare_spending import HealthcareSpending
from data.life_expectancy import LifeExpectancy

st.title('Healthcare Spending')

countries = LifeExpectancy.get_countries()
default_index = countries.index('Canada') if 'Canada' in countries else 0
country = st.selectbox('Select Country', countries, index=default_index)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.header('Spending Per Capita')
with col2:
    st.header('Spending GDP')
with col3:
    st.header('Out of Pocket')
with col4:
    st.header('Gov Spending')
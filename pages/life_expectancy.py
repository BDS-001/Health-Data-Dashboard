import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data.life_expectancy import LifeExpectancy

st.title('Life Expectancy')

countries = LifeExpectancy.get_countries()
default_index = countries.index('Canada') if 'Canada' in countries else 0
country = st.selectbox('Select Country', countries, index=default_index)

data = LifeExpectancy(country)

male_data = data.get_male()
female_data = data.get_female()

all_values = pd.concat([male_data['Life Expectancy'], female_data['Life Expectancy']])
y_min = all_values.min() - 2
y_max = all_values.max() + 2

col1, col2 = st.columns(2)

with col1:
    st.header('Male')
    fig_male = px.line(male_data, x='Year', y='Life Expectancy', title='Male Life Expectancy')
    fig_male.update_yaxes(range=[y_min, y_max])
    st.plotly_chart(fig_male, width='stretch')
    st.dataframe(male_data)

with col2:
    st.header('Female')
    fig_female = px.line(female_data, x='Year', y='Life Expectancy', title='Female Life Expectancy')
    fig_female.update_yaxes(range=[y_min, y_max])
    st.plotly_chart(fig_female, width='stretch')
    st.dataframe(female_data)

st.divider()
st.header('Gender Gap (Female - Male)')

gap_data = pd.merge(
    male_data.rename(columns={'Life Expectancy': 'Male'}),
    female_data.rename(columns={'Life Expectancy': 'Female'}),
    on='Year'
)
gap_data['Gap'] = gap_data['Female'] - gap_data['Male']

fig_gap = go.Figure()
fig_gap.add_bar(x=gap_data['Year'], y=gap_data['Female'], name='Female', marker_color='pink')
fig_gap.add_bar(x=gap_data['Year'], y=gap_data['Male'], name='Male', marker_color='lightblue')
fig_gap.update_layout(
    title='Life Expectancy Gender Gap Over Time',
    xaxis_title='Year', yaxis_title='Life Expectancy',
    barmode='group'
)
fig_gap.update_yaxes(range=[gap_data[['Male', 'Female']].min().min() - 5, gap_data[['Male', 'Female']].max().max() + 2])
st.plotly_chart(fig_gap, width='stretch')
st.dataframe(gap_data[['Year', 'Male', 'Female', 'Gap']])

st.divider()
st.header('Year-over-Year Growth Rate')

both_data = data.get_both().copy()
both_data['Growth Rate (%)'] = both_data['Life Expectancy'].pct_change() * 100
growth_data = both_data.dropna(subset=['Growth Rate (%)'])
growth_data['Color'] = growth_data['Growth Rate (%)'].apply(lambda x: 'Positive' if x >= 0 else 'Negative')

fig_growth = px.bar(
    growth_data, x='Year', y='Growth Rate (%)',
    color='Color',
    color_discrete_map={'Positive': 'green', 'Negative': 'red'},
    title='Year-over-Year Life Expectancy Growth Rate'
)
fig_growth.update_layout(showlegend=False)
st.plotly_chart(fig_growth, width='stretch')
st.dataframe(growth_data[['Year', 'Life Expectancy', 'Growth Rate (%)']])

st.divider()
st.header('Life Expectancy by Country')

years = LifeExpectancy.get_years()
year = st.selectbox('Select Year', years, index=len(years)-1)

year_data = LifeExpectancy.get_by_year(year)

fig_year = px.bar(year_data, x='Country', y='Life Expectancy', title=f'Life Expectancy by Country ({year})')
fig_year.update_yaxes(range=[year_data['Life Expectancy'].min() - 10, year_data['Life Expectancy'].max() + 5])
st.plotly_chart(fig_year, width='stretch')
st.dataframe(year_data)

import streamlit as st
import pandas as pd
import plotly.express as px
import canLifeExpectancy

testData = {
    'id': [0,1,2,3,4],
    'names':['bob', 'foo', 'bar', 'baz', 'jack'],
    'blood_pressure': [120, 115, 145, 110, 135],
}

df = pd.DataFrame(testData)

st.write('Life Expectancy')
st.dataframe(canLifeExpectancy.getData())

high_bp = df[df['blood_pressure'] > 130]
st.write("Patients with BP > 130:")
st.dataframe(high_bp)

fig = px.bar(high_bp, x='names', y='blood_pressure', title='test graph')
st.plotly_chart(fig)
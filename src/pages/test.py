import streamlit as st
import plotly.graph_objects as go

import plotly.express as px

col1, col2, col3 = st.columns(3)


a = 500
b =12


col1.metric('hello', 120, a/b)
col2.metric('hello', 120, a/b)
col3.metric('hello', 120, a/b)




# Use included Google price data to make one plot
df_stocks = px.data.stocks()
ch = px.line(df_stocks, x='date', y='GOOG', labels={'x':'Date', 'y':'Price'})
st.plotly_chart(ch)
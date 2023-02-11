import streamlit as st
import pandas as pd
import plotly.express as px

import connect
import filters

cursor = connect.connect()

f = open('data/uid.txt', 'r')
uid = f.read()

tab1, tab2 = st.tabs(['Income', 'Expense'])

with tab1:
    sel_date = filters.date_range('Range')

    try:
        cursor.execute('select * from inc_pie_chart(%s, %s)', (uid, sel_date))
        df = pd.DataFrame(cursor.fetchall())
        df.columns = ['Category', 'Amount']
        df = filters.category_select(df)
        pie_chart = px.pie(
            data_frame = df,
            values = 'Amount',
            names = 'Category',
            title = 'Income'
        )
        pie_chart.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(pie_chart, use_container_width=True)
        st.dataframe(df)

    except(ValueError):
        st.error('Empty Set')

with tab2:
    sel_date = filters.date_range('range')

    try:
        cursor.execute('select * from exp_pie_chart(%s, %s)', (uid, sel_date))
        df = pd.DataFrame(cursor.fetchall())
        df.columns = ['Category', 'Amount']
        df = filters.category_select(df)
        pie_chart = px.pie(
            data_frame = df,
            values = 'Amount',
            names = 'Category',
            title = 'Expenses'
        )
        pie_chart.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(pie_chart, use_container_width=True)
        st.dataframe(df)

    except(ValueError):
        st.error('No Transactions')




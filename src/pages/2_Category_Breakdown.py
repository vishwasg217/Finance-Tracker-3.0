import streamlit as st
import pandas as pd
import plotly.express as px

import connect
import filters

st.set_page_config(layout="wide")


if st.session_state['logged_in'] == True:
    st.title('Category Breakdown')
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
            col1, col2 = tab1.columns(2)
            pie_chart = px.pie(
                data_frame = df,
                values = 'Amount',
                names = 'Category',
                title = 'Income'
            )
            bar_chart = px.bar(
                data_frame=df,
                x="Category",
                y="Amount",               
            )
            pie_chart.update_traces(textposition='inside', textinfo='percent+label')
            col1.plotly_chart(pie_chart, use_container_width=True)
            col2.plotly_chart(bar_chart, use_container_width=True)
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
            col3, col4 = tab2.columns(2)
            pie_chart = px.pie(
                data_frame = df,
                values = 'Amount',
                names = 'Category',
                title = 'Income'
            )
            bar_chart = px.bar(
                data_frame=df,
                x="Category",
                y="Amount",               
            )
            pie_chart.update_traces(textposition='inside', textinfo='percent+label')
            col3.plotly_chart(pie_chart, use_container_width=True)
            col4.plotly_chart(bar_chart, use_container_width=True)
            st.dataframe(df)

        except(ValueError):
            st.error('No Transactions')

else:
    st.error('Please login to access this page')


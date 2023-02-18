import streamlit as st
import pandas as pd

import connect
import filters

st.set_page_config(layout="wide")


if st.session_state['logged_in'] == True:

    st.title('Cashflow')
    cursor = connect.connect()

    cashflow_section = st.container()
    category_breakdown_section = st.container()

    st.subheader('Cashflow Breakdown')

    f = open('data/uid.txt', 'r')
    uid = f.read()
    sel_date = filters.date_range('Range')


    try:
        cursor.execute('select * from cashflow(%s, %s)', (uid, sel_date))
        df = pd.DataFrame(cursor.fetchall()).transpose()
        if len(df.axes[1]) > 0:
            df = df.rename(columns={df.columns[0]: 'Income'})
            df = df.rename(index={0: 'Number of Transactions', 1: 'Total'})
        inc = 0
        exp = 0
        if len(df.axes[1]) > 1:
            df = df.rename(columns={df.columns[1]: 'Expense'})
            inc = df.loc['Total']['Income']
            exp = df.loc['Total']['Expense']
        st.dataframe(df)
        net = "₹ "+str("{:,}".format(inc-exp))
        st.metric(label='Net Income', value=net)
    except(ValueError):
        st.error('No Transactions')

    st.subheader('Cashflow Breakdown By Category')


    tab1, tab2 = st.tabs(['Income', 'Expense'])
    with tab1:
        sel_date = filters.date_range('Date Range')
        try:
            cursor.execute('select * from inc_pie_chart(%s, %s)', (uid, sel_date))
            df = pd.DataFrame(cursor.fetchall())
            df.columns = ['Category', 'Amount']
            df = filters.category_select(df)
            st.dataframe(df)
        except(ValueError):
            st.error('Empty Set')


    with tab2:
        sel_date = filters.date_range('Date range')
        try:
            cursor.execute('select * from exp_pie_chart(%s, %s)', (uid, sel_date))
            df = pd.DataFrame(cursor.fetchall())
            df.columns = ['Category', 'Amount']
            df = filters.category_select(df)
            st.dataframe(df)
        except(ValueError):
            st.error('Empty Set')

else:
    st.error('Please login to access this page')


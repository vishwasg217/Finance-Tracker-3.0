import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import connect

uid = 'abc123'
cursor = connect.connect()

date_options = ['7 Days', '1 Month', '3 Months', '6 Months', '1 year', 'All Time']
date_select = st.selectbox('Range', date_options)

sel_date = ''
match date_select:
    case '7 Days':
        sel_date = date.today() - relativedelta(days=7)
    case '1 Month':
        sel_date = date.today() - relativedelta(months=1)
    case '3 Months':
        sel_date = date.today() - relativedelta(months=3)
    case '6 Months':
        sel_date = date.today() - relativedelta(months=6)
    case '1 year':
        sel_date = date.today() - relativedelta(years=1)
    case 'All Time':
        sel_date = date.today() - relativedelta(years=5)
    
        
try: 
    cursor.execute('select * from rec(%s, %s)', (uid, sel_date))
    df = pd.DataFrame(cursor.fetchall())
    df.columns = ['Transaction ID', 'Transaction Date', 'Sender', 'Receiver', 'Amount', 'Type', 'Category']
    category_options = sorted(df['Category'].unique())
    category_select = st.multiselect('Category', category_options, category_options)
    df = df[(df['Category'].isin(category_select))]
    if df.empty:
        st.error('No transactions in this time frame')
    else:
        stats_container = st.container()
        st.write('Number of Transactions: ', str(len(df)))
        st.dataframe(df)
        
        inc = df.loc[df['Type'] == 'income']['Amount'].sum()
        exp = df.loc[df['Type'] == 'expense']['Amount'].sum()
        net = inc - exp

        net = "₹ "+str("{:,}".format(net))
        inc =  "₹ "+str("{:,}".format(inc))
        exp = "₹ "+str("{:,}".format(exp))

        with stats_container:
            col1, col2, col3, = st.columns(3)
            col1.metric(label='Net Income', value=net)
            col2.metric(label='Total Income', value=inc)
            col3.metric(label='Total Expenses', value=exp)

except(ValueError):
    st.error("No transactions in this time333 frame")







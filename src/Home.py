import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

import connect
# import records

st.title('Personal Finance Tracker')
st.write(' ')
cursor = connect.connect()

uid = 'abc123'
cursor.execute("select account_balance from users where uid = %s", (uid, ))
acc_bal ="₹ "+str("{:,}".format(cursor.fetchone()[0]))

st.metric(label='Account Balance', value=acc_bal)
st.write(' ')

st.subheader('Transactions in the past 7 days')
sel_date = date.today() - relativedelta(days=7)


try: 
    cursor.execute('select * from rec(%s, %s)', (uid, sel_date))
    df = pd.DataFrame(cursor.fetchall())
    df.columns = ['Transaction ID', 'Transaction Date', 'Sender', 'Receiver', 'Amount', 'Type', 'Category']
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




import streamlit as st
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

st.subheader('Transactions in the past 7 days')
sel_date = date.today() - relativedelta(days=7)
# df = records.get_records(uid=uid, sel_date=sel_date)
# st.write('Number of Transactions: ', str(len(df)))
# st.dataframe(df)




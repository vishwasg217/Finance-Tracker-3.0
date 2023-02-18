import streamlit as st
import pandas as pd
import connect
import filters

st.set_page_config(layout="wide")


if st.session_state['logged_in'] == True:
    st.title('Transaction History')
    cursor = connect.connect()

    f = open('data/uid.txt', 'r')
    uid = f.read()
    sel_date = filters.date_range('Range')
        
    try: 
        cursor.execute('select * from rec(%s, %s)', (uid, sel_date))
        df = pd.DataFrame(cursor.fetchall())
        df.columns = ['Transaction ID', 'Transaction Date', 'Sender', 'Receiver', 'Amount', 'Type', 'Category']
        df = filters.category_select(df)
        if df.empty:
            st.error('No Transactions')
        else:
            stats_container = st.container()
            st.write('Number of Transactions: ', str(len(df)))
            st.dataframe(df)
            
            inc = df.loc[df['Type'] == 'income']['Amount'].sum()
            exp = df.loc[df['Type'] == 'expense']['Amount'].sum()
            net = inc - exp

            delta_exp = ((exp/inc)*100).round(2)
            delta_inc = ((net/inc)*100).round(2)

            net = "₹ "+str("{:,}".format(net))
            inc =  "₹ "+str("{:,}".format(inc))
            exp = "₹ "+str("{:,}".format(exp))

            delta_exp = str(delta_exp)+"%"
            delta_inc = str(delta_inc)+"%"

            with stats_container:
                col1, col2, col3, = st.columns(3)
                col1.metric(label='Total Income', value=inc)
                col2.metric(label='Total Expenses', value=exp, delta=delta_exp, delta_color='off')
                col3.metric(label='Savings', value=net, delta=delta_inc, delta_color='off')

    except(ValueError):
        st.error('No Transactions')

else:
    st.error('Please login to access this page')
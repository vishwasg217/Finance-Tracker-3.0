import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

import connect

header_section = st.container()
login_section = st.container()
signup_section = st.container()

cursor = connect.connect()

def verify_account(username, passwd):
    try:
        cursor.execute("select password from users where username = %s", (username, ))
        check_passwd = cursor.fetchone()[0]
        if check_passwd == passwd:
            st.session_state['logged_in'] = True
            cursor.execute('select uid from users where username = %s', (username, ))
            uid = cursor.fetchone()[0]
            with open('uid.txt', 'w') as f:
                f.write(uid)
        else:
            st.error("Invalid username or password")
            st.session_state['logged_in'] = False

    except TypeError:
        st.error("Invalid username or password")

def logout():
    st.session_state['logged_in'] = False

def show_login_page():
    with login_section:
        if st.session_state['logged_in'] == False:
            username = st.text_input("Enter your username:")
            passwd = st.text_input("Enter your password", type='password')
            st.button("Login", on_click=verify_account, args=(username, passwd))

    with signup_section:
        st.markdown("""---""")

def show_main_page():
    try: 
        f = open('uid.txt', 'r')
        uid = f.read()
        cursor.execute("select account_balance from users where uid = %s", (uid, ))
        acc_bal ="₹ "+str("{:,}".format(cursor.fetchone()[0]))

        st.metric(label='Account Balance', value=acc_bal)
        st.write(' ')

        st.subheader('Transactions in the past 7 days')
        sel_date = date.today() - relativedelta(days=7)
        cursor.execute('select * from rec(%s, %s)', (uid, sel_date))
        df = pd.DataFrame(cursor.fetchall())
        df.columns = ['Transaction ID', 'Transaction Date', 'Sender', 'Receiver', 'Amount', 'Type', 'Category']
        if df.empty:
            st.error('No Transactions')
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

    except(ValueError, TypeError):
        st.error('No Transactions')

def show_logout_button():
    if st.session_state['logged_in']:
        st.sidebar.button('Logout', on_click=logout)    

with header_section:
    st.title('Personal Finance Tracker')
    st.write(' ')
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        show_login_page()
    else:
        if st.session_state['logged_in']:
            show_main_page()
            show_logout_button()
        else:
            show_login_page()











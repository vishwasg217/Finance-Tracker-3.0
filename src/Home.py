import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

import connect
#import utilities.sign_up as sign_up


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
            with open('data/uid.txt', 'w') as f:
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
            st.subheader('Login')            
            username = st.text_input("Enter your username:")
            passwd = st.text_input("Enter your password", type='password')
            st.button("Login", on_click=verify_account, args=(username, passwd))

def show_main_page():
    try: 
        f = open('data/uid.txt', 'r')
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

            delta_exp = ((exp/inc)*100).round(2)
            delta_inc = ((net/inc)*100).round(2)

            inc =  "₹ "+str("{:,}".format(inc))
            exp = "₹ "+str("{:,}".format(exp))
            net = "₹ "+str("{:,}".format(net))

            delta_exp = str(delta_exp)+"%"
            delta_inc = str(delta_inc)+"%"

            with stats_container:
                col1, col2, col3, = st.columns(3)
                col1.metric(label='Total Income', value=inc)
                col2.metric(label='Total Expenses', value=exp, delta=delta_exp, delta_color='off')  
                col3.metric(label='Savings', value=net, delta=delta_inc, delta_color='off')

        st.subheader('Line Chart')
        cursor.execute('select * from inc_line_chart(%s)', (uid, ))
        inc = pd.DataFrame(cursor.fetchall())
        cursor.execute('select * from exp_line_chart(%s)', (uid, ))
        exp = pd.DataFrame(cursor.fetchall())
        df = pd.concat([inc, exp], axis=True, ignore_index=True)
        
        df.drop([2, 3], axis=1, inplace=True)
        df.columns = ['date', 'income', 'expense', 'savings target']
        df['savings'] = df['income'] - df['expense']
        st.line_chart(data=df,x='date',y=('income', 'expense', 'savings', 'savings target'), use_container_width=True)

    except(ValueError, TypeError):
        st.error('No Transactions')

# def show_signup_button():
#     with signup_section:
#         st.markdown("""---""")
#         st.subheader('Sign Up')
#         if st.button('sign up', on_click=sign_up.details_1):
#             sign_up.sign_up()
#             sign_up.next_page


def show_logout_button():
    if st.session_state['logged_in']:
        st.sidebar.button('Logout', on_click=logout)    

with header_section:
    st.title('Personal Finance Tracker')
    st.write(' ')
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state.page = 0
        st.session_state['sign_up'] = False
        show_login_page()
        # show_signup_button()
    else:
        if st.session_state['logged_in']:
            show_main_page()
            show_logout_button()
        if st.session_state['sign_up']:
            pass
            #sign_up.details_1()
        else:
            show_login_page()
            # show_signup_button()
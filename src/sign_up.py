import streamlit as st
import pandas as pd
import uuid

import connect

details_2_section = st.container()
signup_section = st.container()


def details_1():
    if st.session_state['sign_up']:
        uid = str(uuid.uuid4())[:8]
        username = st.text_input("username:")
        passwd = st.text_input("Enter the password", type='password')
        check = st.text_input("confirm password", type='password')

        st.markdown('---')
        st.subheader('Personal Details')
        first_name = st.text_input('Enter your first name')
        last_name = st.text_input('Enter your last name')

        email_id = st.text_input('Enter your email address')
        dob = st.date_input('Enter your date of birth')
        gender = st.selectbox('Choose a gender', ['m', 'f'])

        st.markdown('---')
        st.subheader('Banking Details')
        cursor, conn = connect.connect2()

        cursor.execute('select bank_name from bank')
        bank_options = pd.DataFrame(cursor.fetchall()).to_numpy().flatten()
        bank_select = st.selectbox("Choose your bank", bank_options)
        cursor.execute('select bank_id from bank where bank_name = %s', (bank_select, ))
        bank_id = cursor.fetchone()[0]

        bank_account_id = st.text_input("Enter your bank account ID")

        account_balance = st.number_input("Enter your bank account balance", step=1)
        
        if st.button('Confirm'):
            if passwd == check:
                cursor.execute('''
                insert into users 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (uid, username, passwd, first_name, last_name, email_id, dob, gender, bank_id, bank_account_id, account_balance))
                conn.commit()
                st.session_state['sign_up'] = False
                return
            else: 
                st.error('Passwords do not match')
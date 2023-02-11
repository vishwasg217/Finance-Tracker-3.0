import streamlit as st
import pandas as pd
import uuid

import connect



def details_1():
    if st.session_state['sign_up']:
        form = st.form(key='sign_up_form')
        form.header('Sign Up')
        
        uid = str(uuid.uuid4())[:8]
        username = form.text_input("username:")
        passwd = form.text_input("Enter the password", type='password')
        check = form.text_input("confirm password", type='password')

        form.markdown('---')
        form.subheader('Personal Details')
        first_name = form.text_input('Enter your first name')
        last_name = form.text_input('Enter your last name')

        email_id = form.text_input('Enter your email address')
        dob = form.date_input('Enter your date of birth')
        gender = form.selectbox('Choose a gender', ['m', 'f'])

        form.markdown('---')
        form.subheader('Banking Details')
        cursor, conn = connect.connect2()

        cursor.execute('select bank_name from bank')
        bank_options = pd.DataFrame(cursor.fetchall()).to_numpy().flatten()
        bank_select = form.selectbox("Choose your bank", bank_options)
        cursor.execute('select bank_id from bank where bank_name = %s', (bank_select, ))
        bank_id = cursor.fetchone()[0]

        bank_account_id = form.text_input("Enter your bank account ID")

        account_balance = form.number_input("Enter your bank account balance", step=1)

        button = form.form_submit_button('Confirm')

        if button:
            if passwd == check:
                cursor.execute('''
                insert into users 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (uid, username, passwd, first_name, last_name, email_id, dob, gender, bank_id, bank_account_id, account_balance))
                conn.commit()
                st.success('New account created!! Please go to home page to login')
                st.session_state['sign_up'] = False
            else: 
                st.error('Passwords do not match')
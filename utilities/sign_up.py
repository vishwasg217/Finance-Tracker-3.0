import streamlit as st
import pandas as pd
import uuid

import connect

#st.session_state.page = 1

def next_page(): st.session_state.page += 1
def first_page(): st.session_state.page = 0
def details_not_empty(details: list): 
    for det in details:
        if det == '':
            return False
    return True

form = st.form(key='sign_up_form')
form.header('Sign Up')
next_page_button = st.button('Next page')
button = form.form_submit_button('Confirm')


details = []

def sign_up():
    if st.session_state.page == 1:
        
        uid = str(uuid.uuid4())[:8]
        username = form.text_input("username:")
        passwd = form.text_input("Enter the password", type='password')
        check = form.text_input("confirm password", type='password')
        details.extend([uid, username, passwd, check])
        if next_page_button:
            if details_not_empty(details):
                if passwd == check:
                    next_page()
                else:
                    st.error('The passwords do not match')
            else:
                details.clear()
                st.error('Please fill in all the fields')


        

def page_2():
    if st.session_state.page == 2:
        form.markdown('---')
        form.subheader('Personal Details')
        first_name = form.text_input('Enter your first name')
        last_name = form.text_input('Enter your last name')

        email_id = form.text_input('Enter your email address')
        dob = form.date_input('Enter your date of birth')
        gender = form.selectbox('Choose a gender', ['m', 'f'])
        details.extend([first_name, last_name, email_id, dob, gender])

        if next_page_button:
            if details_not_empty(details):
                    next_page()
            else:
                for _ in range(4):
                    index = details.pop()
                st.error('Please fill in all the fields')



def page_3():
    if st.session_state.page == 3:
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

        details.extend(bank_id, bank_account_id, account_balance)


        if button:
            if details_not_empty(details):
                cursor.execute('''
                insert into users 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                details)
                conn.commit()
                st.success('New account created!! Please go to home page to login')
                first_page()
            else:
                for _ in range(3):
                    index = details.pop()
                st.error('Please fill in all the fields')

            
def page_4():
    pass

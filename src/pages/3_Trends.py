import streamlit as st
import pandas as pd
import connect
import filters

st.set_page_config(layout="wide")


if st.session_state['logged_in'] == True:
    st.title('Trends')
    cursor = connect.connect()
    f = open('data/uid.txt', 'r')
    uid = f.read()

    try:
        st.subheader('Category-wise Trends')
        category = filters.category_select2()
        cursor.execute('select * from cat_line_chart(%s, %s)', (uid, category))
        df = pd.DataFrame(cursor.fetchall())
        df.columns = ['date', category]
        st.line_chart(data=df, x='date', y=category, use_container_width=True)
        
        col1, col2 = st.columns(2)
        col1.subheader('General Trends')
        cursor.execute('select * from inc_line_chart(%s)', (uid, ))
        inc = pd.DataFrame(cursor.fetchall())
        cursor.execute('select * from exp_line_chart(%s)', (uid, ))
        exp = pd.DataFrame(cursor.fetchall())
        df = pd.concat([inc, exp], axis=True, ignore_index=True)
        
        df.drop([2, 3], axis=1, inplace=True)
        df.columns = ['date', 'income', 'expense', 'savings target']
        df['savings'] = df['income'] - df['expense']
        col1.line_chart(data=df,x='date',y=('income', 'expense', 'savings', 'savings target'), use_container_width=True)

        col2.subheader('Networth Trend')
        net_worth  = df[['date', 'savings']]
        net_worth['net worth'] = net_worth['savings'].cumsum()
        col2.line_chart(data=net_worth, x='date', y='net worth', use_container_width=True)



    except(ValueError):
        st.error('Empty Set')
else:
    st.error('Please login to access this page')
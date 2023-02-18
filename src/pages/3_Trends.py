import streamlit as st
import pandas as pd
import connect
import filters

st.set_page_config(layout="wide")


if st.session_state['logged_in'] == True:
    st.title('Line Chart')
    cursor = connect.connect()
    f = open('data/uid.txt', 'r')
    uid = f.read()

    try:
        category = filters.category_select2()
        cursor.execute('select * from cat_line_chart(%s, %s)', (uid, category))
        df = pd.DataFrame(cursor.fetchall())
        df.columns = ['date', category]
        st.line_chart(data=df, x='date', y=category, use_container_width=True)
    except(ValueError):
        st.error('Empty Set')
else:
    st.error('Please login to access this page')
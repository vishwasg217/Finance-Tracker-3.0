import streamlit as st
import pandas as pd
from datetime import date
import connect
from dateutil.relativedelta import relativedelta

def date_range(name: str):
    date_options = ['7 Days', '1 Month', '3 Months', '6 Months', '1 year', 'All Time']
    date_select = st.selectbox(name, date_options)
    sel_date = ''
    match date_select:
        case '7 Days':
            sel_date = date.today() - relativedelta(days=7)
        case '1 Month':
            sel_date = date.today() - relativedelta(months=1)
        case '3 Months':
            sel_date = date.today() - relativedelta(months=3)
        case '6 Months':
            sel_date = date.today() - relativedelta(months=6)
        case '1 year':
            sel_date = date.today() - relativedelta(years=1)
        case 'All Time':
            sel_date = date.today() - relativedelta(years=5)
    return sel_date

def category_select(df: pd.DataFrame):
    category_options = sorted(df['Category'].unique())
    category_select = st.multiselect('Category', category_options, category_options)
    df = df[(df['Category'].isin(category_select))]
    return df

def category_select2():
    cursor = connect.connect()
    cursor.execute('select category_name from category order by category_name')
    category_options = cursor.fetchall()
    cat_options = []
    for i in category_options:
        for j in i:
            cat_options.append(j)
    category_select = st.selectbox('Category', cat_options)
    return category_select
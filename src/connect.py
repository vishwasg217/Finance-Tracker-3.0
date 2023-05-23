import psycopg2
import streamlit as st

def connect():
    conn = psycopg2.connect(
    **st.secrets["postgres"]
    )
    cursor = conn.cursor()
    return cursor

def connect2():
    conn = psycopg2.connect(
    database="tracker", 
    user='postgres', 
    password='PgAdmin@21', 
    host='127.0.0.1', 
    port= '5432'
    )
    cursor = conn.cursor()
    return cursor, conn
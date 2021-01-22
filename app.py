import streamlit as st
import pandas as pd
import sqlite3

stdb = "data/streamlit.db"

st.title('My first app')

@st.cache
def dfFromSql(dbpath, query, params=None):
    con = sqlite3.connect(dbpath)
    df = pd.read_sql(query, con, params=params).reset_index(drop=True)
    con.close()
    return df.convert_dtypes()

materials = dfFromSql(stdb, "SELECT * FROM materials")

categories = materials['ct_2_text'].drop_duplicates().tolist()

def filterdata(selections=[]):
    if len(selections) < 1:
        return materials
    else:
        return materials[materials['ct_2_text'].isin(selections)]

selection = st.sidebar.multiselect('select category', categories)

st.write('You selected:', filterdata(selection))
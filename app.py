import streamlit as st
import pandas as pd
import sqlite3
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


stdb = "data/streamlit.db"

st.title('My first app')

@st.cache
def dfFromSql(dbpath, query, params=None):
    con = sqlite3.connect(dbpath)
    df = pd.read_sql(query, con, params=params).reset_index(drop=True)
    con.close()
    return df.convert_dtypes()


def shapedata(df):
    df = (
        df
        .groupby('mt_no mt_name'.split())
        .agg(lambda x: list(set(list(x))))
    )
    return df

def filterdata(df, keys=[]):
    if len(keys) < 1:
        return df
    else:
        letters_s = set(keys)
        return df[df['ct_2_text'].map(letters_s.issubset)]

def get_tags(df):
    tags = df.explode('ct_2_text')['ct_2_text'].unique().tolist()
    return tags

materials = dfFromSql(stdb, "SELECT * FROM testmaterial")

data = shapedata(materials)

# categories = materials['ct_2_text'].drop_duplicates().tolist()

selection = st.multiselect('select category', get_tags(data))

data = filterdata(data, selection)

st.write('You selected:', data)
import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title('Bangladesh WiFi Data Analysis')
st.sidebar.title('WiFi Data Analysis')

st.markdown("WiFI User Of Bangladesh")
st.sidebar.markdown("Wifi Users")

DATA_URL = ('/Users/khoundokarzahid/Downloads/ada.csv')


@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL,nrows=nrows,parse_dates=['last_seen'])
    data.dropna(subset=['con_type'], inplace=True)
    lowercase = lambda x:str(x).lower()
    data.rename(lowercase, axis='columns',inplace=True)
    data.rename(columns={'last_seen_date_time':'date/time'},inplace=True)
    return data

data = load_data(100000)
data[['latitude', 'longitude']].to_csv('lat_lng.csv',index=False)

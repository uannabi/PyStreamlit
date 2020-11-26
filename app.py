import streamlit as st

import pandas as pd
import numpy as np

st.title('sentiment analysis of tweets about us airlines')
st.sidebar.title('sentiment analysis of tweets about us airlines')

st.markdown("sentiment of tweet")
st.sidebar.markdown("sentiment of tweet")

DATA_URL = ('/Users/khoundokarzahid/Stack/github/PyStreamlit/Tweets.csv')


@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data


data = load_data()

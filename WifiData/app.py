import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pydeck as pdk
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
DATE_TIME = "date/time"
st.title('Bangladesh WiFi Data Analysis')
st.sidebar.title('WiFi Data Analysis')

st.markdown("WiFI User Of Bangladesh")
st.sidebar.markdown("Wifi Users")

DATA_URL = ('/Users/khoundokarzahid/Downloads/ada.csv')


@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=['last_seen'])
    data.dropna(subset=['con_type'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'last_seen_date_time': 'date/time'}, inplace=True)
    return data


data = load_data(100000)
data[['latitude', 'longitude']].to_csv('lat_lng.csv', index=False)
st.sidebar.subheader("Where People ar the most WiFI used ?")
wifi_user = st.sidebar.slider('Number of Wifi user in Bangladesh', 1, 1000)
st.map(data.query("brq_count >= @wifi_user")[['latitude', 'longitude']].dropna(how="any"))
if st.sidebar.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data[['last_seen', 'latitude', 'longitude']],
            get_position=['longitude', 'latitude'],
            auto_highlight=True,
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
        ),
    ],
))

st.sidebar.subheader("Wifi User Via its Type")
choice = st.sidebar.multiselect('Pick Wifi Type',
                                ('Cable/DSL', 'Dialup', 'Corporate'), key='0')

if len(choice) > 0:
    choice_data = data[data.con_type.isin(choice)]
    fig_choice = px.histogram(choice_data, x='gps_city', y='con_type', histfunc='count',
                              color='con_type', facet_col='con_type',
                              labels={'BD_WIFI_USER:type'}, height=600, width=800)
    st.plotly_chart(fig_choice)


data = load_data(nrows=5000)

st.sidebar.subheader('Bar chart according to BRQ')
df = pd.DataFrame(data[:5000],columns=['con_type','gps_city','brq_count'])
df.hist()
plt.show()
st.pyplot()

st.sidebar.subheader('City wise Connection Type')
if st.sidebar.checkbox('Show Stacked Information'):
    st.write(data)
    st.bar_chart(data['last_seen'])



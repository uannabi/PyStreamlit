import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pydeck as pdk
import plotly.express as px

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

# st.sidebar.header("When wifi user are seen ?")
# hour = st.sidebar.slider("Hour to look at", 0, 23)
# date = data[data['last_seen'].dt.hour == hour]
# original_data = data
#
# data = data[data[DATE_TIME].dt.hour == hour]
# st.sidebar.markdown("user last seen between %i:00 and %i:00" % (hour, (hour + 1) % 24))

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

# wifi_options = st.sidebar.radio('con_type',('Cable/DSL','Corporate','Dialup'))
# st.sidebar.markdown(data.query('con_type == @wifi_options'))
# ['brq_count'].sample(n=1).iat[0,0]
#
# st.sidebar.markdown("### number of wifi by options")
# select = st.sidebar.selectbox('Visualization type', ['Histogram','Pie Chart'],key='1')
#
# wifi_count = data['con_type'].value_counts()
#
# wifi_count = pd.DataFrame({'WiFi':wifi_count.index,'Type':wifi_count.values})
# if not st.sidebar.checkbox("Hide",True):
#     st.markdown("### Number of Bangladesh wifi users")
#     if select == 'Histogram':
#         fig = px.bar(wifi_count,x='Wifi', y='User',color='Wifi', height=500)
#         st.plotly_chart(fig)

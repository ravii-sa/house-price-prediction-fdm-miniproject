import streamlit as st
import pandas as pd
import os
import numpy as np
from util.functions import hide_footer_and_menu, load_lottie
from streamlit_lottie import st_lottie

import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import plotly.express as px

st.set_page_config(page_title="Data Summary", page_icon="📊", layout="wide")
st.title("Data Summary")

hide_footer_and_menu()

exports_dir = os.path.join(os.path.dirname(__file__),'..', 'exports')

@st.cache_resource
def read_df():
    df = pd.read_csv(os.path.join(exports_dir, 'visualise_data.csv'))
    return df

df = read_df()

@st.cache_resource
def get_plots():
    global df

    dist_map = folium.Map(location=[6.9271, 79.8612], zoom_start=7)
    dist_map.add_child(folium.plugins.HeatMap(df[['lat', 'lon']], radius=10))

    avg_price_district = df.groupby('district')['price_per_house_size'].mean().reset_index()
    avg_price_city = df.groupby('city')['price_per_house_size'].mean().reset_index()

    avg_price_per_bed = df.groupby('beds')['price'].mean().reset_index()

    avg_price_per_bath = df.groupby('baths')['price'].mean().reset_index()

    return dist_map, avg_price_district, avg_price_city, avg_price_per_bed, avg_price_per_bath

dist_map, avg_house_price_district, avg_house_price_city, avg_price_per_bed, avg_price_per_bath = get_plots()

st.subheader('Distribution of houses considered for the study')
st_folium(dist_map, use_container_width=True)

st.divider()

st.subheader('Average house price by district')
fig = px.bar(avg_house_price_district, x='district', y='price_per_house_size')
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader('Average house price by city')
fig = px.bar(avg_house_price_city, x='city', y='price_per_house_size')
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader('Average house price by number of bedrooms')
fig = px.bar(avg_price_per_bed, x='beds', y='price')
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader('Average house price by number of bathrooms')
fig = px.bar(avg_price_per_bath, x='baths', y='price')
st.plotly_chart(fig, use_container_width=True)

end_anim = load_lottie("https://lottie.host/9197dc86-5626-49ca-b728-d29e20b07b91/m4PytQh6SF.json")
st_lottie(
    end_anim,
    speed=1,
    loop=1,
    height=100,
)
import streamlit as st
import pickle
import os
import pandas as pd
import numpy as np
from util.functions import hide_footer_and_menu

st.set_page_config(page_title="House Price Calculator", page_icon="🏠", layout="centered")
st.title("Calculate House Price")

hide_footer_and_menu()

st.write(
    """
    This app estimates the price of a house in Sri Lanka based on the the provided details.
    """
)

@st.cache_resource
def read_exports():
    # get the full path to the exports directory
    exports_dir = os.path.join(os.path.dirname(__file__), 'exports')

    # load best model
    with open(os.path.join(exports_dir, 'model.pkl'), 'rb') as file:
        model = pickle.load(file)

    # load std_scaler
    with open(os.path.join(exports_dir, 'std_scaler.pkl'), 'rb') as file:
        continuous_features, std_scaler = pickle.load(file)

    # load minmax_scaler
    with open(os.path.join(exports_dir, 'minmax_scaler.pkl'), 'rb') as file:
        discrete_features, minmax_scaler = pickle.load(file)

    # load column order
    with open(os.path.join(exports_dir, 'column_order.pkl'), 'rb') as file:
        column_order = pickle.load(file)

    # load column info
    with open(os.path.join(exports_dir, 'column_info.pkl'), 'rb') as file:
        column_info = pickle.load(file)

    # load location hierarchy
    with open(os.path.join(exports_dir, 'location_hierarchy.pkl'), 'rb') as file:
        location_hierarchy = pickle.load(file)

    return model, continuous_features, std_scaler, discrete_features, minmax_scaler, column_order, column_info, location_hierarchy

model, continuous_features, std_scaler, discrete_features, minmax_scaler, column_order, column_info, location_hierarchy = read_exports()

def generate_features(df):
    df['sqft_per_bed'] = df['house_size'] / df['beds']
    df['house_land_ratio'] = np.ceil(df['house_size'] / df['land_size'] / 272.25 )
    df['baths_per_bed'] = df['baths'] / df['beds']
    
    return df

st.divider()

col1, col2 = st.columns(2)

input_form = st.container()

district_options = location_hierarchy.keys()
all_city_options = list(set(city for cities in location_hierarchy.values() for city in cities))

with input_form:
    beds = st.number_input(
        label="Number of bedrooms",
        min_value=int(column_info['beds']['min']),
        max_value=int(column_info['beds']['max']),
        value=int(column_info['beds']['mean']),
        step=1,
        key="beds",
    )

    baths = st.number_input(
        label="Number of bathrooms",
        min_value=int(column_info['baths']['min']),
        max_value=int(column_info['baths']['max']),
        value=int(column_info['baths']['mean']),
        step=1,
        key="baths",
    )

    house_size = st.number_input(
        label="House size (sqft)",
        min_value=column_info['house_size']['min'],
        max_value=column_info['house_size']['max'],
        value=column_info['house_size']['mean'],
        step=0.01,
        key="house_size",
    )

    land_size = st.number_input(
        label="Land size (perches)",
        min_value=column_info['land_size']['min'],
        max_value=column_info['land_size']['max'],
        value=column_info['land_size']['mean'],
        step=0.01,
        key="land_size",
    )

    lon_col, lat_col = st.columns(2)

    lon = lon_col.number_input(
        label="Longitude",
        min_value=column_info['lon']['min'],
        max_value=column_info['lon']['max'],
        value=column_info['lon']['mean'],
        step=0.01,
        key="lon",
    )

    lat = lat_col.number_input(
        label="Latitude",
        min_value=column_info['lat']['min'],
        max_value=column_info['lat']['max'],
        value=column_info['lat']['mean'],
        step=0.01,
        key="lat",
    )

    dist_col, city_col = st.columns(2)

    district = dist_col.selectbox(
        label="District",
        options=district_options,
        index=0,
        key="district",
    )

    city = city_col.selectbox(
        label="City",
        options=location_hierarchy[district],
        index=0,
        key="city",
    )


    form_submitted = st.button(label="Submit")

st.divider()

prediction = 0

if form_submitted:

    inputs = {
        'baths': baths,
        'beds': beds,
        'house_size': house_size,
        'land_size': land_size,
        'lon': lon,
        'lat': lat,
    }

    df = pd.DataFrame(columns=column_order, index=[0], data=0)
    
    for name, value in inputs.items():
        df[name] = value

    df['city_' + city] = 1
    df['district_' + district] = 1
    
    generate_features(df)

    df[continuous_features] = std_scaler.transform(df[continuous_features])
    df[discrete_features] = minmax_scaler.transform(df[discrete_features])

    st.session_state['prediction'] = model.predict(df)[0]

    
st.metric(label="Predicted Price", value=f"{(st.session_state['prediction'] if 'prediction' in st.session_state else 0):,.0f} LKR")

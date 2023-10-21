import streamlit as st
import requests

@st.cache_resource
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def hide_footer_and_menu():
    st.markdown(
        """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
        """ 
        , unsafe_allow_html=True)
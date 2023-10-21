import streamlit as st
from streamlit_lottie import st_lottie
from util.functions import load_lottie

st.set_page_config(page_title="About Us", page_icon="📚", layout="centered")

# Hide footer and menu
st.markdown(
    """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """ 
    , unsafe_allow_html=True)

st.title("About Us")

st.write(
    """
    Welcome to House Price Calculator.
    We are a group of undergraduate students who have come together to create this web application.
    Our mission is to help home buyers, sellers and real estate enthusiasts to get a better understanding of the housing market.
    So that they can make informed decisions when it comes to one of most important financial decisions of their lives.
    """
)

st.divider()

st.write(
    """
    ### Our Team
    """
)

st.write(
    """
    ##### [Hapuarachchi H.A.R.S.](https://www.linkedin.com/in/ravindu-hapuarachchi/)
    ##### [Somarathne D.K.](https://www.linkedin.com/in/ravindu-hapuarachchi/)
    ##### [Thilakarathne M.B.N.](https://www.linkedin.com/in/ravindu-hapuarachchi/)
    ##### [Edirisinghe E.A.K.G.](https://www.linkedin.com/in/ravindu-hapuarachchi/)

    """
)

team_anim = load_lottie("https://lottie.host/c69ef07a-0a18-4399-8338-e259b347edc4/0YnSm1KmpA.json")
st_lottie(
    team_anim,
    speed=1,
    height=200,
)
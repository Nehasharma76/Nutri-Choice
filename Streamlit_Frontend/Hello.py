# import streamlit as st

# st.set_page_config(
#     page_title="Hello",   
#     page_icon="👋",
# )

# st.write("# Welcome to NUTRI CHOICE! 👋")

# st.sidebar.success("Select a recommendation app.")

# st.markdown(  
#     """
#     A diet recommendation web application using content-based approach with Scikit-Learn, FastAPI and Streamlit.
#     You can find more details and the whole project on my [repo](https://github.com/Nehasharma76/Nutri-Choice).
#     """
# )


import streamlit as st
from streamlit_lottie import st_lottie
import requests

# ---- Load Lottie Animation ----
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_food = load_lottie("https://assets2.lottiefiles.com/packages/lf20_7wwm6xi5.json")

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="NutriChoice",
    page_icon="🥗",
    layout="wide"
)

# ---- HEADER ----
st.markdown(
    """
    <h1 style='text-align:center; color:#2E8B57; font-size:42px;'>
        🥗 NutriChoice – Your Smart Meal Recommendation System
    </h1>
    <p style='text-align:center; font-size:18px; color:#555;'>
        Eat smarter. Choose better. Get personalized recipes based on your ingredients and meal type.
    </p>
    """,
    unsafe_allow_html=True
)

st.write("")

# ---- Two Column Layout ----
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown(
        """
        <h3 style='color:#2E8B57;'>✨ What NutriChoice Does</h3>
        <ul style='font-size:17px; color:#444;'>
            <li>🔍 Finds recipes based on ingredients you already have</li>
            <li>🥣 Filters by Breakfast, Lunch, or Dinner</li>
            <li>🤖 Uses machine learning (cosine similarity) for smart recommendations</li>
            <li>⚡ Fast performance with FastAPI backend + Streamlit UI</li>
            <li>🐳 Easily deployable inside Docker</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🚀 Ready to get started?")
    st.markdown(
        """
        <a href="/1_💪_Diet_Recommendation" target="_self">
            <button style="
                background-color:#2E8B57;
                color:white;
                padding:15px 30px;
                font-size:18px;
                border:none;
                border-radius:8px;
                cursor:pointer;">
                Start Recommending Recipes →
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

with right_col:
    if lottie_food:
        st_lottie(lottie_food, height=350)

# ---- FOOTER ----
st.write("")
st.markdown(
    """
    <hr>
    <p style='text-align:center; color:#777;'>
        Built with ❤️ using FastAPI, Streamlit & Machine Learning  
    </p>
    """,
    unsafe_allow_html=True
)


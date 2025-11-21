import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Nutri-Choice! 👋")

st.sidebar.success("Select a recommendation app.")

st.markdown(
    """
    A diet recommendation web application using content-based approach with Scikit-Learn, FastAPI and Streamlit.
    You can find more details and the whole project on my [repo](https://https://github.com/Nehasharma76/Nutri-Choice).
    """         
)

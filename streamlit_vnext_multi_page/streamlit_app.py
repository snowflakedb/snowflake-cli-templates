import streamlit as st

from common.ui import APP_LOGO

st.logo(
    APP_LOGO,
    size="large",
)

navigation = [
    st.Page(
        "app_pages/home_page.py",
        title="Home",
        icon=":material/home:",
    ),
    st.Page(
        "app_pages/example_page.py",
        title="Example page",
        icon=":material/comedy_mask:",
    ),
    # Add more pages here!
]

current_page = st.navigation(
    navigation,
    position="top",  # You can try position="sidebar" too!
)

current_page.run()

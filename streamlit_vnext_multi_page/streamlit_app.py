import streamlit as st

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

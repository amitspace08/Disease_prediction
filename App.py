import streamlit as st
from modules import heart, liver, kidney, diabetes
from components import styles, navbar, sidebar, home, about, footer

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="MediPredict | AI Powered Health Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Initialize Navigation State
if "page" not in st.session_state:
    # Read page from query parameters for deep-linking
    url_page = st.query_params.get("page", "Home")
    if url_page in ["Home", "Heart", "Liver", "Kidney", "Diabetes", "About", "History"]:
        st.session_state.page = url_page
    else:
        st.session_state.page = "Home"

# Sync browser URL query parameters with active session state
st.query_params["page"] = st.session_state.page

# 3. Inject Global CSS Stylesheet
st.markdown(styles.get_base_css(), unsafe_allow_html=True)

# 4. Render Fixed Navigation Components
navbar.render_navbar()
sidebar.render_sidebar()

# 5. Route Page Content
current_page = st.session_state.page

if current_page == "Home":
    home.render_home()
elif current_page == "About":
    about.render_about()
elif current_page == "History":
    from components import history
    history.render_history()
elif current_page == "Heart":
    heart.app()
elif current_page == "Liver":
    liver.app()
elif current_page == "Kidney":
    kidney.app()
elif current_page == "Diabetes":
    diabetes.app()

# 6. Render Footer Component
footer.render_footer()
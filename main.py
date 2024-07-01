import streamlit as st

# Streamlit interface
st.set_page_config(page_title="BaVista", page_icon=":memo:", layout='wide', initial_sidebar_state='collapsed')

# Using columns to center the logo
col1, col2, col3 = st.columns([1,2,1])  # Adjust the ratio as needed to center the logo
with col2:
    logo_path = "bavista_logo.png"  # Update 'path_to_your_logo.png' with the real path to your logo file
    st.image(logo_path, use_column_width=True)  # Adjust 'use_column_width' to True or set width parameter

st.title('Select one of the use cases below:')

st.markdown("""
    <style>
        button {
            padding-top: 50px !important;
            padding-bottom: 50px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Create three columns
col1, col2, col3 = st.columns(3)

# Add a button to each column
with col1:
    if st.button("📈 **Digram Generation** $(Alpha)$", use_container_width=True):
        st.switch_page("pages/diagram_agent.py")

with col2:
    if st.button("**👩🏻‍🏫 Document Translator**", use_container_width=True):
        st.switch_page("pages/translator_agent.py")

with col3:
    if st.button("**📝 Minutes to Requirements** $(Beta)$", use_container_width=True):
        st.switch_page("pages/requirements_agent.py")

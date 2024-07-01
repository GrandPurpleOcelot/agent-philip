import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import logging
import urllib.parse

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants for Google OAuth
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

def create_google_oauth_client():
    return OAuth2Session(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scope=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri="https://bavista.streamlit.app/",
        token_endpoint='https://oauth2.googleapis.com/token'
    )

def load_google_userinfo(token):
    client = create_google_oauth_client()
    client.token = token
    userinfo_response = client.get('https://openidconnect.googleapis.com/v1/userinfo')
    logger.debug(f"Userinfo Response: {userinfo_response.json()}")
    return userinfo_response.json()

# Initialize session state for auth token
if 'auth_token' not in st.session_state:
    st.session_state['auth_token'] = None

st.set_page_config(page_title="BaVista", page_icon=":memo:", layout='wide', initial_sidebar_state='collapsed')

if st.session_state['auth_token'] is None:
    oauth_client = create_google_oauth_client()
    authorization_endpoint = "https://accounts.google.com/o/oauth2/auth"
    auth_url, state = oauth_client.create_authorization_url(authorization_endpoint, prompt="consent")         
    if 'code' in st.query_params:
        # Decode and log the authorization code
        code = urllib.parse.unquote(st.query_params['code'][0])
        logger.debug(f"Decoded Authorization Code: {code}")

        try:
            token = oauth_client.fetch_token(code=code)
            st.session_state['auth_token'] = token
            st.experimental_rerun()
        except Exception as e:
            error_response = e.response.json() if e.response else 'No response'
            logger.error(f"Error fetching token: {e}, Response: {error_response}")
            st.error(f"Failed to authenticate. Please try again. Error: {error_response}")
    else:
        st.markdown(f"Please log in to continue: [Login with Google]({auth_url})")
else:
    user_info = load_google_userinfo(st.session_state['auth_token'])
    st.write(f"Welcome {user_info['name']}!")

    # Using columns to center the logo
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        logo_path = "bavista_logo.png"
        st.image(logo_path, use_column_width=True)

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
        if st.button("📈 **Diagram Generation** $(Alpha)$", use_container_width=True):
            st.switch_page("pages/diagram_agent.py")

    with col2:
        if st.button("**👩🏻‍🏫 Document Translator**", use_container_width=True):
            st.switch_page("pages/translator_agent.py")

    with col3:
        if st.button("**📝 Minutes to Requirements** $(Beta)$", use_container_width=True):
            st.switch_page("pages/requirements_agent.py")

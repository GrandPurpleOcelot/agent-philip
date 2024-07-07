import streamlit as st
from authlib.integrations.requests_client import OAuth2Session, OAuthError
import logging
import urllib.parse

# Constants for Google OAuth
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

def create_google_oauth_client():
    return OAuth2Session(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scope=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri="https://bavista.streamlit.app/oauth2callback",  # Updated redirect URI
        token_endpoint='https://oauth2.googleapis.com/token'
    )

def load_google_userinfo(token):
    client = create_google_oauth_client()
    client.token = token
    userinfo_response = client.get('https://openidconnect.googleapis.com/v1/userinfo')
    return userinfo_response.json()

# Initialize session state for auth token
if 'auth_token' not in st.session_state:
    st.session_state['auth_token'] = None

def handle_auth_callback():
    query_params = st.query_params
    code = query_params.get("code", [None])[0]
    if code:
        try:
            oauth_client = create_google_oauth_client()
            token = oauth_client.fetch_token(code=code)
            st.session_state['auth_token'] = token
            return True
        except OAuthError as e:
            st.error(f"Failed to authenticate. Please try again. Error: {e.error}")
            return False
        except Exception as e:
            st.error("Failed to authenticate. Please try again.")
            return False
    return False

st.set_page_config(page_title="BaVista", page_icon=":memo:", layout='wide', initial_sidebar_state='collapsed')

if st.session_state['auth_token'] is None:
    if not handle_auth_callback():
        oauth_client = create_google_oauth_client()
        authorization_endpoint = "https://accounts.google.com/o/oauth2/auth"
        auth_url, state = oauth_client.create_authorization_url(authorization_endpoint, prompt="consent")
        col1, col2, col3 = st.columns([2,1,2])  # Adjust the ratios as needed for better alignment
        with col2:
            logo_path = "xvista_logo.png"
            st.image(logo_path, use_column_width=True)
            st.markdown("<h3 style='text-align: center;'>Sign in</h3>", unsafe_allow_html=True)
            st.link_button("Continue with Google", auth_url, use_container_width=True, type="primary")
            st.markdown(
            "<p style='text-align: center;'>New to xVista? Contact "
            "<a href='mailto:thienn@fpt.com'>thienn@fpt.com</a> for access</p>", 
            unsafe_allow_html=True
            )
else:
    user_info = load_google_userinfo(st.session_state['auth_token'])
    st.write(f"Welcome {user_info['name']}!")

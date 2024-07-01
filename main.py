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
        redirect_uri="http://localhost:8508/home",
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
        code = urllib.parse.unquote(st.query_params['code'][0])
        try:
            token = oauth_client.fetch_token(code=code)
            st.session_state['auth_token'] = token
            st.experimental_rerun()
        except OAuthError as e:  # Catch specific OAuth errors
            error_response = e.error
            logger.error(f"OAuth Error fetching token: {e.error}")
            st.error(f"Failed to authenticate. Please try again. Error: {error_response}")
        except Exception as e:  # Catch any other exceptions
            logger.error(f"General Error fetching token: {str(e)}")
            st.error("Failed to authenticate. Please try again.")
    else:
        st.markdown(f"Please log in to continue: [Login with Google]({auth_url})")
else:
    user_info = load_google_userinfo(st.session_state['auth_token'])
    st.write(f"Welcome {user_info['name']}!")

import streamlit as st
import hmac
import hashlib
import time
import json
from datetime import datetime, timedelta
import extra_streamlit_components as stx

# Create cookie manager - simpler initialization
def get_manager():
    return stx.CookieManager()

# Initialize cookie manager at the very top
cookie_manager = get_manager()

# Must be called once at the start of your app
cookie_manager.get_all()

st.title('Secure User Login App')

def hash_password(password, salt=None):
    """Hash password with SHA-256 and random salt"""
    if salt is None:
        salt = hashlib.sha256(str(time.time()).encode()).hexdigest()
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        100000  # Number of iterations
    ).hex()
    return pw_hash, salt

def verify_password(password, stored_hash, salt):
    """Verify password against stored hash"""
    pw_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(pw_hash, stored_hash)

def create_session_token(username):
    """Create a secure session token with expiry"""
    expiry = (datetime.now() + timedelta(hours=24)).isoformat()
    session_data = {
        'username': username,
        'expiry': expiry,
        'token': hmac.new(
            st.secrets["SECRET_KEY"].encode(),
            f"{username}{expiry}".encode(),
            hashlib.sha256
        ).hexdigest()
    }
    return json.dumps(session_data)

def verify_session(token_str):
    """Verify session token is valid"""
    if not token_str:
        return False, None
    try:
        token_data = json.loads(token_str)
        username = token_data['username']
        expiry = datetime.fromisoformat(token_data['expiry'])

        # Check expiration
        if expiry < datetime.now():
            return False, None

        # Verify token authenticity
        expected_token = hmac.new(
            st.secrets["SECRET_KEY"].encode(),
            f"{username}{token_data['expiry']}".encode(),
            hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(expected_token, token_data['token']):
            return True, username
        return False, None
    except:
        return False, None

# Mock user database - in production, use a real database
USERS = {
    'admin': {
        'password_hash': 'bc903dbbe8aa6f641d85498009a95d5422bd2fd56364c31decd023c19e83811f',  # hashed '1234'
        'salt': 'default_salt'
    }
}

# Check for existing session
session_token = cookie_manager.get('session_token')
if session_token:
    is_valid, username = verify_session(session_token)
    if is_valid:
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
    else:
        # Clear invalid cookie
        cookie_manager.delete('session_token')
        st.session_state['logged_in'] = False

# Login/Logout Logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.write('Please login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    submit = st.button('Login')

    if submit:
        if username in USERS and verify_password(
            password,
            USERS[username]['password_hash'],
            USERS[username]['salt']
        ):
            # Create and set session token
            session_token = create_session_token(username)
            cookie_manager.set(
                'session_token',
                session_token,
                # Explicitly set cookie options
                expires_at=datetime.now() + timedelta(hours=24),
                path='/'  # Make cookie available across all paths
            )
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.error('Invalid username or password')

else:
    st.write(f'Welcome back, {st.session_state["username"]}!')

    if st.button('Logout'):
        # Clear cookie
        cookie_manager.delete('session_token')
        # Clear session state
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.rerun()

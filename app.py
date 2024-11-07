import streamlit as st
import hmac
import hashlib
import time

st.set_page_config(
    page_title="Cortado Rating",
    page_icon="☕",
    layout="centered",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title('Simple User Login App')


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


# Mock user database - in production, use a real database
USERS = {
    'admin': {
        'password_hash': 'bc903dbbe8aa6f641d85498009a95d5422bd2fd56364c31decd023c19e83811f',  # hashed '1234'
        'salt': 'default_salt'
    }
}


# Initialize session state
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
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.error('Invalid username or password')

else:
    st.write(f'Welcome back, {st.session_state["username"]}!')

    if st.button('Logout'):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.rerun()

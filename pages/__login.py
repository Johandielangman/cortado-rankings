from datetime import datetime, timedelta
from utils.mongo import MongoUtils
from constants import Constants
import streamlit as st
import hashlib
import hmac
import time


def reload():
    st.rerun()


class Login:
    def __init__(self, callback) -> None:
        c: Constants = Constants()
        if (
            "login" in st.session_state and
            st.session_state.login and
            (datetime.now() < st.session_state.login + timedelta(minutes=c.login_duration_mins))
        ):
            callback()
        else:
            st.title('🔐 Please login')
            username = st.text_input(
                "Username",
                ""
            )
            password = st.text_input('Password', type='password')
            submit = st.button('Login', type='primary')

            if submit:
                try:
                    with st.spinner('Logging in...'):
                        mu: MongoUtils = MongoUtils(
                            username=str(st.secrets["mongo"]["username"]),
                            password=str(st.secrets["mongo"]["password"]),
                            cluster=str(st.secrets["mongo"]["cluster"]),
                            database=str(st.secrets["mongo"]["database"]),
                        )
                        user_data: dict = mu.db['users'].find_one({'username': username})
                        if self.verify_password(
                            password=password,
                            stored_hash=user_data['password'],
                            salt=c.secrets['mongo']['salt']
                        ):
                            st.session_state.login = datetime.now() + timedelta(minutes=c.login_duration_mins)
                            st.session_state.username = username
                            st.rerun()
                        else:
                            st.error('Invalid username or password')
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    def hash_password(
        self,
        password: str,
        salt: str = None
    ) -> tuple[str, str]:
        if salt is None:
            salt = hashlib.sha256(str(time.time()).encode()).hexdigest()
        pw_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000  # Number of iterations
        ).hex()
        return pw_hash, salt

    def verify_password(
        self,
        password: str,
        stored_hash: str,
        salt: str
    ) -> bool:
        pw_hash, _ = self.hash_password(password, salt)
        return hmac.compare_digest(pw_hash, stored_hash)

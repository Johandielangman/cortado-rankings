from utils.google_maps import GoogleMapsConverter
from streamlit_star_rating import st_star_rating
from utils.mongo import MongoUtils
import streamlit as st
import os
from pages.__login import Login
from constants import Constants
from datetime import datetime
import pytz


class Rate:
    def __init__(self) -> None:
        Login(callback=self.__display_from)

    def __display_from(self):
        st.title("How was your Cortado? ☕")
        c = Constants()
        with st.form("rate!"):
            stars = st_star_rating(
                "Rate the taste",
                size=30,
                maxValue=5,
                defaultValue=0,
                key="rating"
            )
            nickname = st.text_input(
                "Shop nickname",
                ""
            )

            google_maps_link = st.text_input(
                "Google Maps Link",
                ""
            )

            additional_comments = st.text_input(
                "Any additional comments?",
                ""
            )

            submitted = st.form_submit_button("Submit")
            if submitted:
                try:
                    with st.spinner('Saving your rating...'):
                        gmaps_converter = GoogleMapsConverter(c.secrets['google']['api_key'])
                        gmaps_data = gmaps_converter.process_url(google_maps_link)
                        mu: MongoUtils = MongoUtils(
                            username=str(st.secrets["mongo"]["username"]),
                            password=str(st.secrets["mongo"]["password"]),
                            cluster=str(st.secrets["mongo"]["cluster"]),
                            database=str(st.secrets["mongo"]["database"]),
                        )
                        mu.db['ratings'].insert_one({
                            "created_at": datetime.now(pytz.timezone("Africa/Johannesburg")),
                            "stars": stars,
                            "nickname": nickname,
                            "name": gmaps_data.get('result', {}).get('name'),
                            "lat_long": gmaps_data.get('result', {}).get('geometry', {}).get('location'),
                            "google_maps_link": google_maps_link,
                            "additional_comments": additional_comments,
                            "website": gmaps_data.get('result', {}).get('website'),
                            "address": gmaps_data.get('result', {}).get('formatted_address'),
                            "username": st.session_state.username,
                        })
                    st.success("Saved! Now get another Cortado ☕")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if not os.path.basename(__file__).startswith("__"):
    r: Rate = Rate()

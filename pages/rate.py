import streamlit as st
from streamlit_star_rating import st_star_rating
from utils.mongo import MongoUtils
from typing import (
    List,
    Optional
)


class Rate:
    def __init__(self) -> None:
        st.title("How was your Cortado? ☕")
        self._display_from()

    def _display_from(self):
        with st.form("rate!"):
            stars = st_star_rating(
                "Rate the taste",
                size=30,
                maxValue=5,
                defaultValue=0,
                key="rating"
            )
            shop_name = st.text_input(
                "Shop name",
                ""
            )

            province = st.selectbox(
                "Choose a province",
                (
                    "Eastern Cape",
                    "Free State",
                    "Gauteng",
                    "KwaZulu-Natal",
                    "Limpopo",
                    "Mpumalanga",
                    "North West",
                    "Northern Cape",
                    "Western Cape",
                ),
                index=None,
                placeholder="Select a province...",
            )

            lat_long = st.text_input(
                "Lat Long",
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
                        mu: MongoUtils = MongoUtils(
                            username=str(st.secrets["mongo"]["username"]),
                            password=str(st.secrets["mongo"]["password"]),
                            cluster=str(st.secrets["mongo"]["cluster"]),
                            database=str(st.secrets["mongo"]["database"]),
                        )
                        mu.db['ratings'].insert_one({
                            "stars": stars,
                            "province": province,
                            "shop_name": shop_name,
                            "lat_long": self._lat_long_from_string(lat_long),
                            "additional_comments": additional_comments
                        })
                    st.success("Saved! Now get another Cortado ☕")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    def _lat_long_from_string(
        self,
        lat_long: str
    ) -> Optional[List[float]]:
        if "," not in lat_long:
            return None
        try:
            return [float(x) for x in lat_long.split(",")]
        except ValueError:
            return None

r: Rate = Rate()

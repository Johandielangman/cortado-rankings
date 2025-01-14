import streamlit as st
import pandas as pd
from pages.__login import Login
import os
from utils.mongo import MongoUtils


@st.cache_data(ttl=60)
def get_all_ratings():
    mu: MongoUtils = MongoUtils(
        username=str(st.secrets["mongo"]["username"]),
        password=str(st.secrets["mongo"]["password"]),
        cluster=str(st.secrets["mongo"]["cluster"]),
        database=str(st.secrets["mongo"]["database"]),
    )
    return list(mu.db['ratings'].find({}))


def create_display_name(row):
    name = row['name']
    nickname = row.get('nickname', '')
    if nickname and nickname != name:
        display = f"{name} ({nickname})"
    else:
        display = name
    return f"[{display}]({row['google_maps_link']})"


def format_stars(stars):
    return "⭐" * int(stars)


class Home:
    def __init__(self) -> None:
        Login(callback=self.__display)

    def __display(self):
        if "username" in st.session_state:
            st.title(f"Hello, {st.session_state.username}👋!")
        with st.spinner("Loading ratings..."):
            ratings = get_all_ratings()
        st.write(f"We've had {len(ratings)} ratings so far! 🎉")

        df = pd.DataFrame(ratings)
        df = df.sort_values('created_at', ascending=False)

        map_data = pd.DataFrame(
            [[r['lat_long']['lat'], r['lat_long']['lng']] for r in ratings],
            columns=['latitude', 'longitude']
        )

        # Display map
        st.subheader("Cortado Locations 📍")
        st.map(map_data)

        # Process data for display
        display_df = pd.DataFrame({
            'Date': df['created_at'].dt.strftime("%d %B %Y"),
            'Shop': df.apply(create_display_name, axis=1),
            'Rating': df['stars'].apply(format_stars),
            'Comments': df['additional_comments'],
            'Rated By': df['username']
        })

        # Display table
        st.subheader("Cortado Ratings ⭐")
        st.markdown(display_df.to_markdown(index=False), unsafe_allow_html=True)


if not os.path.basename(__file__).startswith("__"):
    i: Home = Home()

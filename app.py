from utils.page import PageUtils
from pages.__login import Login
from constants import Constants
import streamlit as st
import os


class App:
    def __init__(self) -> None:
        self.c: Constants = Constants()
        self._setup()

    def _setup(self):
        st.set_page_config(
            page_title=self.c.page_setup.page_title,
            page_icon=self.c.page_setup.page_icon,
            layout=self.c.page_setup.layout,
        )
        Login(callback=self.__run)

    def __run(self):
        if "username" in st.session_state:
            st.sidebar.write(f"Hello, {st.session_state.username}! 👋")
        pg = st.navigation(
            [st.Page(**page) for page in self._get_pages()],
            position="sidebar"
        )
        pg.run()

    def _get_pages(self):
        pages = []
        for file in os.listdir("pages"):
            if (
                file.endswith(".py") and
                not file.startswith("__")
            ):
                pages.append({
                    "page": PageUtils.page(file),
                    "title": PageUtils.title(file),
                    "icon": "☕",
                    "url_path": PageUtils.url_path(file)
                })
        return pages


if __name__ == "__main__":
    app = App()

import tomllib
import os
from dataclasses import dataclass, field
from typing import (
    Dict,
    Optional
)


@dataclass(frozen=True)
class PageSetup:
    "Streamlit page setup"
    page_title: str = "Cortado"
    page_icon: str = "☕"
    layout: str = "centered"


@dataclass(frozen=True)
class Paths:
    cwd: str = os.getcwd()
    root: str = os.path.dirname(__file__)
    streamlit_folder_name: str = ".streamlit"
    secrets_file_name: str = "secrets.toml"

    @property
    def secrets_path(self):
        return os.path.join(self.root, self.streamlit_folder_name, self.secrets_file_name)


@dataclass
class Constants:
    page_setup: PageSetup = PageSetup()
    paths: Paths = Paths()
    login_duration_mins: int = 60
    _secrets: Optional[Dict] = field(
        repr=False,
        default_factory=dict
    )

    def __post_init__(self):
        self._load_secrets()

    def _load_secrets(self):
        with open(self.paths.secrets_path, 'rb') as f:
            self._secrets = tomllib.load(f)

    @property
    def secrets(self):
        return self._secrets

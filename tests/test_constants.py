from constants import Constants
from urllib.parse import quote


def test_load_constants():
    c: Constants = Constants()
    assert c.page_setup.page_title == "Cortado"
    c.secrets


def test_percentage_encoding():
    # Because: https://www.mongodb.com/docs/manual/reference/connection-string/
    # Need to make sure we parse $ : / ? # [ ] @
    assert quote("$", safe='') == "%24"
    assert quote(":", safe='') == "%3A"
    assert quote("/", safe='') == "%2F"
    assert quote("?", safe='') == "%3F"
    assert quote("#", safe='') == "%23"
    assert quote("[", safe='') == "%5B"
    assert quote("]", safe='') == "%5D"
    assert quote("@", safe='') == "%40"

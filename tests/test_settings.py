import pytest
from pages.base_page import BasePage
from pages.settings_page import SettingsPage

@pytest.mark.settings
def test_settings_loaded(page):
    BasePage(page).open_sidebar("Settings")
    sp = SettingsPage(page)
    sp.assert_loaded()

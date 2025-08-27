import pytest
from pages.base_page import BasePage

@pytest.mark.navigation
@pytest.mark.parametrize("menu,heading", [
    ("Dashboard", "Dashboard"),
    ("Accounts", "Accounts"),
    ("Exposed Inventory", "Exposed Inventory"),
    ("Vaulted Secrets", "Vaulted Secrets"),
    ("Risks", "Risk"),
    ("Settings", "Settings"),
])
def test_sidebar_navigation(page, menu, heading):
    bp = BasePage(page)
    bp.goto("https://qa.entro.security/")
    # Using storage_state fixture login already happened; navigating should work
    bp.open_sidebar(menu)
    bp.assert_heading(heading)

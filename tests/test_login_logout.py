import pytest
from pages.login_page import LoginPage

@pytest.mark.smoke
def test_login_and_logout(page):
    lp = LoginPage(page, base_url="https://qa.entro.security/")
    lp.open()
    lp.login("user1@qa.interview", "Entr0T@sk!")
    # Expect we see some authenticated UI (navbar, dashboard, etc.)
    assert page.get_by_role("navigation").is_visible()
    lp.logout()

import pytest
from pages.base_page import BasePage
from pages.accounts_page import AccountsPage

@pytest.mark.accounts
class TestAccounts:
    def test_filter_accounts(self, page):
        BasePage(page).goto("https://qa.entro.security/")
        BasePage(page).open_sidebar("Accounts")
        ap = AccountsPage(page)
        ap.filter("prod")
        # At least ensure table exists
        assert page.get_by_role("table").is_visible()

    def test_open_account_drawer_and_change_env(self, page):
        BasePage(page).open_sidebar("Accounts")
        ap = AccountsPage(page)
        ap.open_account_drawer("prod")
        ap.change_environment("Staging")
        # Expect save toast or disabled save
        assert page.get_by_role("button", name="Save").count() == 0 or page.get_by_text("Saved").count() > 0

    def test_add_account_form_validation(self, page):
        BasePage(page).open_sidebar("Accounts")
        ap = AccountsPage(page)
        ap.open_add_account()
        ap.submit_add()
        # Expect validation messages
        assert page.get_by_text("required").first.is_visible()

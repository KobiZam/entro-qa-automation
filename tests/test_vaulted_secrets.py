import pytest
from pages.base_page import BasePage
from pages.vaulted_secrets_page import VaultedSecretsPage

@pytest.mark.secrets
class TestVaultedSecrets:
    def test_filter_and_open_drawer(self, page):
        BasePage(page).open_sidebar("Vaulted Secrets")
        vs = VaultedSecretsPage(page)
        vs.filter("api")
        vs.open_drawer("api")
        assert page.get_by_role("dialog").is_visible()

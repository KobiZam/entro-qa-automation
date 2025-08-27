import pytest
from pages.base_page import BasePage
from pages.vaulted_secrets_page import VaultedSecretsPage

@pytest.mark.secrets
@pytest.mark.smoke
def test_export_vaulted_secrets(page, tmp_path):
    # Set download dir and verify an export trigger works (no logging)
    page.context.set_default_timeout(15000)
    BasePage(page).open_sidebar("Vaulted Secrets")
    vs = VaultedSecretsPage(page)
    with page.expect_download() as dl_info:
        vs.export()
    download = dl_info.value
    target = tmp_path / download.suggested_filename
    download.save_as(target)
    assert target.exists() and target.stat().st_size > 0

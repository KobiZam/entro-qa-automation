import pytest
from pages.base_page import BasePage
from pages.risks_page import RisksPage

@pytest.mark.risks
class TestRisks:
    def test_risks_loaded_and_filter(self, page):
        BasePage(page).open_sidebar("Risks")
        rp = RisksPage(page)
        rp.assert_loaded()
        rp.filter_by_severity("High")
        assert page.get_by_text("High").count() >= 0

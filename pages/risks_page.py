from playwright.sync_api import Page, expect

class RisksPage:
    def __init__(self, page: Page):
        self.page = page

    def assert_loaded(self):
        expect(self.page.get_by_role("heading", name="Risk", exact=False)).to_be_visible()

    def filter_by_severity(self, severity: str):
        self.page.get_by_role("combobox", name="Severity").click()
        self.page.get_by_role("option", name=severity, exact=False).click()

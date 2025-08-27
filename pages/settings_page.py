from playwright.sync_api import Page, expect

class SettingsPage:
    def __init__(self, page: Page):
        self.page = page

    def assert_loaded(self):
        expect(self.page.get_by_role("heading", name="Settings", exact=False)).to_be_visible()

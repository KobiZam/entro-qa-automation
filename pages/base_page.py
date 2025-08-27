from playwright.sync_api import Page, expect
from utils.selectors import sidebar_item

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, path: str):
        self.page.goto(path)

    def open_sidebar(self, name: str):
        # Click the item and wait for URL change or a known heading
        with self.page.expect_navigation(wait_until="networkidle"):
            sidebar_item(self.page, name).click()

    def assert_heading(self, text: str):
        expect(self.page.get_by_role("heading", name=text, exact=False)).to_be_visible()

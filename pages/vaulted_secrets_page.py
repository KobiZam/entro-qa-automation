from playwright.sync_api import Page, expect
from utils.selectors import input_by_label, button, row_by_text

class VaultedSecretsPage:
    def __init__(self, page: Page):
        self.page = page

    def filter(self, text: str):
        if input_by_label(self.page, "Search").count():
            input_by_label(self.page, "Search").fill(text)
        else:
            self.page.get_by_placeholder("Search").fill(text)

    def export(self):
        button(self.page, "Export").click()
        # expect file chooser to be triggered or toast displayed

    def open_drawer(self, text: str):
        row_by_text(self.page, text).get_by_role("button", name="Details").click()

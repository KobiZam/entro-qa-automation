from playwright.sync_api import Page, expect
from utils.selectors import input_by_label, button, row_by_text

class ExposedInventoryPage:
    def __init__(self, page: Page):
        self.page = page

    def filter(self, text: str):
        if input_by_label(self.page, "Filter").count():
            input_by_label(self.page, "Filter").fill(text)
        else:
            self.page.get_by_placeholder("Filter").fill(text)

    def open_drawer_by_row(self, text: str):
        row_by_text(self.page, text).get_by_role("button", name="Details").click()

    def apply_bulk_operation(self, op_name: str):
        self.page.get_by_role("button", name="Bulk actions").click()
        self.page.get_by_role("menuitem", name=op_name, exact=False).click()
        # confirm if needed
        if self.page.get_by_role("button", name="Confirm").count():
            button(self.page, "Confirm").click()

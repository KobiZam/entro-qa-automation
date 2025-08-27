from playwright.sync_api import Page, expect
from utils.selectors import button, input_by_label, row_by_text

class AccountsPage:
    def __init__(self, page: Page):
        self.page = page

    def open_add_account(self):
        button(self.page, "Add account").click()

    def fill_add_form_minimal(self, name: str, env: str = "Production"):
        # Generic labels; adapt as needed in runtime
        if input_by_label(self.page, "Account name").count():
            input_by_label(self.page, "Account name").fill(name)
        else:
            self.page.get_by_placeholder("Account name").fill(name)
        # environment dropdown
        self.page.get_by_role("button", name="Environment").click()
        self.page.get_by_role("option", name=env, exact=False).click()

    def submit_add(self):
        button(self.page, "Create").click()

    def filter(self, text: str):
        if input_by_label(self.page, "Search").count():
            input_by_label(self.page, "Search").fill(text)
        else:
            self.page.get_by_placeholder("Search").fill(text)

    def open_account_drawer(self, name: str):
        row_by_text(self.page, name).get_by_role("button", name="Details").click()

    def change_environment(self, new_env: str):
        self.page.get_by_role("combobox", name="Environment").click()
        self.page.get_by_role("option", name=new_env, exact=False).click()
        button(self.page, "Save").click()

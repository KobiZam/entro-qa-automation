from playwright.sync_api import Page, expect
from utils.selectors import input_by_label, button

class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(self.base_url)

    def login(self, email: str, password: str):
        # Works whether landing on login page or need to click a Sign in button first
        if self.page.get_by_role("button", name="Sign in").count():
            self.page.get_by_role("button", name="Sign in").click()
        # Fill by common labels/placeholders
        if self.page.get_by_label("Email").count():
            self.page.get_by_label("Email").fill(email)
        else:
            self.page.get_by_placeholder("Email").fill(email)

        if self.page.get_by_label("Password").count():
            self.page.get_by_label("Password").fill(password)
        else:
            self.page.get_by_placeholder("Password").fill(password)

        button(self.page, "Sign in").click()
        expect(self.page).to_have_url(lambda url: "login" not in url.lower(), timeout=15000)

    def logout(self):
        # Try avatar menu / user menu patterns
        if self.page.get_by_role("button", name="Logout").count():
            self.page.get_by_role("button", name="Logout").click()
        else:
            # Open profile menu then click Logout
            self.page.get_by_role("button", name="Profile").click(timeout=5000)
            self.page.get_by_role("menuitem", name="Logout").click()
        expect(self.page).to_have_url(lambda url: "login" in url.lower(), timeout=10000)

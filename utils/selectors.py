from playwright.sync_api import Page, Locator

# Helper selectors centralized here for resilience and reuse.
# Prefer role-based and text-based locators that survive DOM changes.

def sidebar_item(page: Page, name: str) -> Locator:
    # Try multiple strategies: role+name, has-text fallback
    return page.get_by_role("navigation").get_by_role("link", name=name, exact=False)


def input_by_label(page: Page, label: str) -> Locator:
    return page.get_by_label(label, exact=False)


def button(page: Page, name: str) -> Locator:
    return page.get_by_role("button", name=name, exact=False)


def row_by_text(page: Page, text: str) -> Locator:
    return page.get_by_role("row").filter(has_text=text)


def drawer_by_title(page: Page, title: str) -> Locator:
    return page.get_by_role("dialog").filter(has_text=title)

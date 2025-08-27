import pytest
from pages.base_page import BasePage
from pages.exposed_inventory_page import ExposedInventoryPage

@pytest.mark.inventory
class TestExposedInventory:
    def test_filter_and_open_drawer(self, page):
        BasePage(page).goto("https://qa.entro.security/")
        BasePage(page).open_sidebar("Exposed Inventory")
        inv = ExposedInventoryPage(page)
        inv.filter("token")
        inv.open_drawer_by_row("token")
        assert page.get_by_role("dialog").is_visible()

    def test_bulk_operation_apply(self, page):
        BasePage(page).open_sidebar("Exposed Inventory")
        inv = ExposedInventoryPage(page)
        inv.apply_bulk_operation("Dismiss")
        # Expect a toast/notification appears
        assert page.get_by_text("Dismissed").count() > 0 or page.get_by_role("alert").count() > 0

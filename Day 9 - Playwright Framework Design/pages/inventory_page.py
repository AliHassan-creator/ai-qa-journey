from playwright.sync_api import Page

from .base_page import BasePage
from .cart_page import CartPage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def products_heading(self):
        return self.page.get_by_text("Products", exact=True)

    def add_backpack_to_cart(self):
        self.page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
        return self

    @property
    def cart_badge(self):
        return self.page.get_by_test_id("shopping-cart-badge")

    def open_cart(self) -> CartPage:
        self.page.get_by_test_id("shopping-cart-link").click()
        return CartPage(self.page)

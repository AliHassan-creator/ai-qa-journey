from playwright.sync_api import Page

from .base_page import BasePage
from .checkout_page import CheckoutPage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def cart_heading(self):
        return self.page.get_by_text("Your Cart", exact=True)

    @property
    def checkout_button(self):
        return self.page.get_by_role("button", name="Checkout")

    def checkout(self):
        self.checkout_button.click()
        return CheckoutPage(self.page)

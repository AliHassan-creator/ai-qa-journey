from playwright.sync_api import Page

from .base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def error_message(self):
        return self.page.get_by_role("alert")

    @property
    def overview_heading(self):
        return self.page.get_by_text("Checkout: Overview", exact=True)

    @property
    def complete_heading(self):
        return self.page.get_by_text("Checkout: Complete!", exact=True)

    def continue_with_customer(self, first_name: str, last_name: str, postal_code: str):
        self.page.get_by_test_id("firstName").fill(first_name)
        self.page.get_by_test_id("lastName").fill(last_name)
        self.page.get_by_test_id("postalCode").fill(postal_code)
        self.page.get_by_role("button", name="Continue").click()
        return self

    def finish_order(self):
        self.page.get_by_role("button", name="Finish").click()
        return self

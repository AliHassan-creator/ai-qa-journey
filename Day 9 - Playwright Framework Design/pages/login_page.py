import os

from playwright.sync_api import Page

from .base_page import BasePage
from .inventory_page import InventoryPage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username = os.getenv("SAUCEDEMO_USER", "standard_user")
        self.password = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")

    def open(self):
        self.page.goto(self.BASE_URL)
        return self

    @property
    def error_message(self):
        return self.page.get_by_role("alert")

    def login(self, username: str | None = None, password: str | None = None) -> InventoryPage:
        user = self.username if username is None else username
        pw = self.password if password is None else password

        self.page.get_by_placeholder("Username").fill(user)
        self.page.get_by_placeholder("Password").fill(pw)
        self.page.get_by_role("button", name="Login").click()

        return InventoryPage(self.page)

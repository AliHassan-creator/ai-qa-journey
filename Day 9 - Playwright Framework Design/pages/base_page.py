import os

from playwright.sync_api import Page


class BasePage:
    BASE_URL = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com")

    def __init__(self, page: Page):
        self.page = page

    def open(self, path: str = "") -> "BasePage":
        target = f"{self.BASE_URL}{path}"
        self.page.goto(target)
        return self

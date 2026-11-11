import re

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage


def test_valid_login_opens_inventory(page):
    login_page = LoginPage(page)

    inventory_page = login_page.open().login()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory_page.products_heading).to_be_visible()


@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        pytest.param("", "secret_sauce", "Username is required", id="missing-username"),
        pytest.param("standard_user", "wrong-password", "Username and password do not match", id="wrong-password"),
    ],
)
def test_login_rejects_invalid_credentials(page, username, password, expected_error):
    login_page = LoginPage(page).open()

    login_page.login(username, password)

    expect(login_page.error_message).to_contain_text(expected_error)


def test_saved_storage_state_starts_on_inventory(authenticated_page):
    from pages.inventory_page import InventoryPage

    expect(authenticated_page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(InventoryPage(authenticated_page).products_heading).to_be_visible()


def test_add_to_cart_updates_badge(authenticated_page):
    from pages.inventory_page import InventoryPage

    inventory_page = InventoryPage(authenticated_page)
    inventory_page.add_backpack_to_cart()

    expect(inventory_page.cart_badge).to_have_text("1")


def test_cart_shows_selected_product(authenticated_page):
    from pages.inventory_page import InventoryPage

    cart_page = InventoryPage(authenticated_page).add_backpack_to_cart().open_cart()

    expect(cart_page.cart_heading).to_be_visible()
    expect(authenticated_page.get_by_text("Sauce Labs Backpack", exact=True)).to_be_visible()


def test_checkout_requires_first_name(authenticated_page):
    from pages.inventory_page import InventoryPage

    checkout_page = InventoryPage(authenticated_page).add_backpack_to_cart().open_cart().checkout()
    checkout_page.continue_with_customer("", "Learner", "12345")

    expect(checkout_page.error_message).to_contain_text("First Name is required")


def test_customer_can_complete_checkout(authenticated_page):
    from pages.inventory_page import InventoryPage

    checkout_page = InventoryPage(authenticated_page).add_backpack_to_cart().open_cart().checkout()
    checkout_page.continue_with_customer("QE", "Learner", "12345")

    expect(checkout_page.overview_heading).to_be_visible()
    expect(authenticated_page.get_by_text("Sauce Labs Backpack", exact=True)).to_be_visible()
    checkout_page.finish_order()

    expect(checkout_page.complete_heading).to_be_visible()
    expect(authenticated_page.get_by_role("heading", name="Thank you for your order!")).to_be_visible()

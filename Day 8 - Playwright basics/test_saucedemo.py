"""Browser checks for the public SauceDemo training store."""

import os
import re
from decimal import Decimal

import pytest

pytest.importorskip(
    "pytest_playwright",
    reason="Install the Day 8 requirements to run browser tests.",
)

from playwright.sync_api import Page, expect


BASE_URL = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com")
STANDARD_USER = os.getenv("SAUCEDEMO_USER", "standard_user")
STANDARD_PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")

pytestmark = pytest.mark.ui


@pytest.fixture(scope="session", autouse=True)
def configure_saucedemo_test_id_attribute(playwright):
    """SauceDemo uses data-test, while Playwright defaults to data-testid."""
    playwright.selectors.set_test_id_attribute("data-test")


def _login(page: Page, username: str = STANDARD_USER, password: str = STANDARD_PASSWORD):
    page.goto(BASE_URL)
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Login").click()


def _add_backpack_to_cart(page: Page):
    _login(page)
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()


def test_saucedemo_test_id_configuration_uses_data_test(page: Page):
    page.set_content('<button data-test="example-action">Continue</button>')

    expect(page.get_by_test_id("example-action")).to_be_visible()


def test_login_form_has_named_controls(page: Page):
    page.goto(BASE_URL)

    expect(page.get_by_placeholder("Username")).to_be_visible()
    expect(page.get_by_placeholder("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()


def test_valid_login_opens_inventory(page: Page):
    _login(page)

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.get_by_text("Products", exact=True)).to_be_visible()


@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        pytest.param("", STANDARD_PASSWORD, "Username is required", id="missing-username"),
        pytest.param(STANDARD_USER, "", "Password is required", id="missing-password"),
        pytest.param(STANDARD_USER, "wrong-password", "Username and password do not match", id="wrong-password"),
    ],
)
def test_login_rejects_invalid_input(page: Page, username: str, password: str, expected_error: str):
    _login(page, username, password)

    expect(page.get_by_role("alert")).to_contain_text(expected_error)


def test_locked_out_user_sees_access_error(page: Page):
    _login(page, "locked_out_user", STANDARD_PASSWORD)

    expect(page.get_by_role("alert")).to_contain_text("locked out")


def test_add_to_cart_updates_item_count(page: Page):
    _add_backpack_to_cart(page)

    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")
    expect(page.get_by_test_id("remove-sauce-labs-backpack")).to_be_visible()


def test_remove_from_cart_clears_item_count(page: Page):
    _add_backpack_to_cart(page)
    page.get_by_test_id("remove-sauce-labs-backpack").click()

    expect(page.get_by_test_id("shopping-cart-badge")).to_have_count(0)
    expect(page.get_by_test_id("add-to-cart-sauce-labs-backpack")).to_be_visible()


def test_cart_shows_the_selected_product(page: Page):
    _add_backpack_to_cart(page)
    page.get_by_test_id("shopping-cart-link").click()

    expect(page.get_by_text("Your Cart", exact=True)).to_be_visible()
    expect(page.get_by_text("Sauce Labs Backpack", exact=True)).to_be_visible()


def test_checkout_requires_first_name(page: Page):
    _add_backpack_to_cart(page)
    page.get_by_test_id("shopping-cart-link").click()
    page.get_by_role("button", name="Checkout").click()
    page.get_by_role("button", name="Continue").click()

    expect(page.get_by_role("alert")).to_contain_text("First Name is required")


def test_customer_can_complete_checkout(page: Page):
    _add_backpack_to_cart(page)
    page.get_by_test_id("shopping-cart-link").click()
    page.get_by_role("button", name="Checkout").click()
    page.get_by_test_id("firstName").fill("QE")
    page.get_by_test_id("lastName").fill("Learner")
    page.get_by_test_id("postalCode").fill("12345")
    page.get_by_role("button", name="Continue").click()

    expect(page.get_by_text("Checkout: Overview", exact=True)).to_be_visible()
    expect(page.get_by_text("Sauce Labs Backpack", exact=True)).to_be_visible()
    page.get_by_role("button", name="Finish").click()

    expect(page.get_by_text("Checkout: Complete!", exact=True)).to_be_visible()
    expect(page.get_by_role("heading", name="Thank you for your order!")).to_be_visible()


def test_product_sorting_low_to_high_price(page: Page):
    _login(page)

    sort_control = page.get_by_test_id("product-sort-container")
    sort_control.select_option(label="Price (low to high)")
    expect(sort_control).to_have_value("lohi")

    displayed_prices = page.get_by_test_id("inventory-item-price").all_text_contents()
    prices = [Decimal(price.replace("$", "")) for price in displayed_prices]

    assert len(prices) > 1, "Expected multiple product prices to verify sorting."
    assert prices == sorted(prices), f"Prices are not in ascending order: {prices}"

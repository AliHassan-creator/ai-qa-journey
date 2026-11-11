from playwright.sync_api import Page, expect


def test_demo_store_homepage(page: Page):
    page.goto("https://www.saucedemo.com/")

    expect(page).to_have_title("Swag Labs")
    expect(page.locator("[data-test='username']")).to_be_visible()
    expect(page.locator("[data-test='password']")).to_be_visible()
    expect(page.locator("[data-test='login-button']")).to_be_visible()

def test_successful_login(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")
    expect(page.locator(".inventory_item")).to_have_count(6)


def test_invalid_login(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator("[data-test='username']").fill("invalid_user")
    page.locator("[data-test='password']").fill("wrong_password")
    page.locator("[data-test='login-button']").click()

    error_message = page.locator("[data-test='error']")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text(
        "Username and password do not match"
    )

    expect(page).to_have_url("https://www.saucedemo.com/")


def test_add_product_to_cart(page: Page):
    page.goto("https://www.saucedemo.com/")

    # Log in
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    # Add the first product to the cart
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()

    # Verify the cart badge
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    # Open the cart
    page.locator(".shopping_cart_link").click()

    # Verify the product is in the cart
    expect(page.locator(".cart_item")).to_have_count(1)
    expect(page.locator(".inventory_item_name")).to_have_text(
        "Sauce Labs Backpack"
    )
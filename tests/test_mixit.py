import pytest

BASE_URL = "https://www.mixit.cz"


def test_mixit_page_loads(page):
    page.goto(BASE_URL)
    assert "Mixit" in page.title()


def test_mixit_logo_visible(page):
    page.goto(BASE_URL)
    logo = page.locator("a[href='/']")
    assert logo.is_visible()


def test_login_button_visible(page):
    page.goto(BASE_URL)
    login_button = page.locator("button:has-text('Přihlásit')")
    assert login_button.is_visible()
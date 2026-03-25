import pytest
import re
from playwright.sync_api import expect

BASE_URL = "https://www.mixit.cz"


@pytest.fixture
def home_page(page):
    page.goto(BASE_URL)
    try:
        page.get_by_role("button", name="Souhlasím").click(timeout=2000)
    except:
        pass
    return page


def test_mixit_page_loads(home_page):
    expect(home_page).to_have_title(re.compile("Mixit"))


def test_mixit_logo_visible(home_page):
    logo = home_page.locator("a[href='/']").first
    expect(logo).to_be_visible()


def test_login_button_visible(home_page):
    login_button = home_page.locator("button").filter(has_text="Přihlásit")
    expect(login_button.first).to_be_visible()
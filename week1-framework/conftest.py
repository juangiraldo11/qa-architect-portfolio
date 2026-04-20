import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption(
        "--headed", action="store_true", default=False, help="Run browser in headed mode"
    )


@pytest.fixture(scope="session")
def browser(request):
    headless = not request.config.getoption("--headed")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def login_page(page):
    lp = LoginPage(page)
    page.goto(LoginPage.URL)
    return lp

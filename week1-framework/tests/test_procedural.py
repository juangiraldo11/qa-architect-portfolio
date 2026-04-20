import pytest
from playwright.sync_api import sync_playwright, expect

def test_login_procedural():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.click("button[type='submit']")
        expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")
        browser.close()

def test_invalid_login_procedural():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "wrongpass")
        page.click("button[type='submit']")
        expect(page.locator("#flash")).to_contain_text("Your password is invalid")
        browser.close()

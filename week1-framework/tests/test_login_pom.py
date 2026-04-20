from pages.login_page import User

VALID_USER = User("tomsmith", "SuperSecretPassword!")


def test_valid_login(login_page):
    secure = login_page.login_with(VALID_USER)
    secure.flash.should_contain("You logged into a secure area!")


def test_invalid_password(login_page):
    result = login_page.login_expecting_failure(User("tomsmith", "wrongpass"))
    result.flash.should_contain("Your password is invalid")


def test_empty_username(login_page):
    result = login_page.login_expecting_failure(User("", "SuperSecretPassword!"))
    result.flash.should_contain("Your username is invalid")


def test_empty_password(login_page):
    result = login_page.login_expecting_failure(User("tomsmith", ""))
    result.flash.should_contain("Your password is invalid")

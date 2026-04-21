from __future__ import annotations

from dataclasses import dataclass

from pages.flash_message import FlashMessage
from pages.secure_page import SecurePage


@dataclass
class User:
    username: str
    password: str


class LoginPage:
    URL = "https://the-internet.herokuapp.com/login"

    def __init__(self, page):
        self.page = page
        self.flash = FlashMessage(page)
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def _submit_credentials(self, user: User) -> None:
        self.username_input.fill(user.username)
        self.password_input.fill(user.password)
        self.login_button.click()

    def login_with(self, user: User) -> "SecurePage":
        self._submit_credentials(user)
        return SecurePage(self.page)

    def login_expecting_failure(self, user: User) -> "LoginPage":
        self._submit_credentials(user)
        return self

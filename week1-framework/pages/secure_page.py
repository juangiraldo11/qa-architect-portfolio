from pages.flash_message import FlashMessage


class SecurePage:
    URL = "https://the-internet.herokuapp.com/secure"

    def __init__(self, page):
        self.page = page
        self.flash = FlashMessage(page)
        self.heading = page.get_by_role("heading", name="Secure Area")
        self.logout_button = page.get_by_role("link", name="Logout")

    def is_loaded(self) -> bool:
        return self.heading.is_visible()

    def logout(self):
        self.logout_button.click()

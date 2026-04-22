from playwright.sync_api import Page


class BrowseTheWeb:
    def __init__(self, page: Page):
        self.page = page

    @classmethod
    def using(cls, page: Page) -> "BrowseTheWeb":
        return cls(page)

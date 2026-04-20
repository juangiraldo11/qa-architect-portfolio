from playwright.sync_api import expect


class FlashMessage:
    def __init__(self, page):
        self._locator = page.locator("#flash")

    def should_contain(self, text: str):
        expect(self._locator).to_contain_text(text)

    @property
    def is_success(self) -> bool:
        return "success" in (self._locator.get_attribute("class") or "")

    @property
    def is_error(self) -> bool:
        return "error" in (self._locator.get_attribute("class") or "")

from playwright.sync_api import expect
import re

class FlashMessage:
    """
    Componente del banner flash. 
    
    Para aserciones en tests, usa los métodos `should_*` (incluyen auto-wait).
    Las @property existen SOLO para consultas puntuales donde el caller ya
    sabe que el elemento está presente (ej. debugging, logging).
    """
    
    def __init__(self, page):
        self._locator = page.locator("#flash")

    def should_contain(self, text: str) -> None:
        expect(self._locator).to_contain_text(text)

    def should_be_success(self) -> None:
        expect(self._locator).to_have_class(re.compile(r"\bsuccess\b"))

    def should_be_error(self) -> None:
        expect(self._locator).to_have_class(re.compile(r"\berror\b"))
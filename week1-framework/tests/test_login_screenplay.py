from screenplay.actions.navigate import Navigate
from screenplay.tasks.log_in import LogIn
from screenplay.questions.the_text import TheText
from screenplay.questions.current_url import CurrentUrl
from screenplay.targets import FLASH_MESSAGE

LOGIN_URL = "https://the-internet.herokuapp.com/login"


def test_valid_login(maria):
    maria.attempts_to(
        Navigate.to(LOGIN_URL),
        LogIn.with_credentials("tomsmith", "SuperSecretPassword!"),
    )
    assert "You logged into a secure area!" in maria.asks(TheText.of(FLASH_MESSAGE))


def test_invalid_login(maria):
    maria.attempts_to(
        Navigate.to(LOGIN_URL),
        LogIn.with_credentials("tomsmith", "wrongpass"),
    )
    assert "Your password is invalid!" in maria.asks(TheText.of(FLASH_MESSAGE))


def test_redirects_to_secure_area_after_login(maria):
    maria.attempts_to(
        Navigate.to(LOGIN_URL),
        LogIn.with_credentials("tomsmith", "SuperSecretPassword!"),
    )
    assert "/secure" in maria.asks(CurrentUrl.value())

from dataclasses import dataclass


@dataclass(frozen=True)
class Target:
    """Wrapper semántico sobre un selector CSS/XPath."""
    name: str
    selector: str


USERNAME_FIELD = Target("username field", "#username")
PASSWORD_FIELD = Target("password field", "#password")
LOGIN_BUTTON   = Target("login button",   "button[type='submit']")
FLASH_MESSAGE  = Target("flash message",  "#flash")

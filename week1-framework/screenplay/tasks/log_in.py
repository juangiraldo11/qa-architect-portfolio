from ..actor import Actor
from ..actions.fill import Fill
from ..actions.click import Click
from ..targets import USERNAME_FIELD, PASSWORD_FIELD, LOGIN_BUTTON


class LogIn:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def with_credentials(cls, username: str, password: str) -> "LogIn":
        return cls(username, password)

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(
            Fill.field(USERNAME_FIELD).with_(self.username),
            Fill.field(PASSWORD_FIELD).with_(self.password),
            Click.on(LOGIN_BUTTON),
        )

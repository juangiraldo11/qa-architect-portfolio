from ..actor import Actor
from ..abilities.browse_the_web import BrowseTheWeb


class Navigate:
    def __init__(self, url: str):
        self.url = url

    @classmethod
    def to(cls, url: str) -> "Navigate":
        return cls(url)

    def perform_as(self, actor: Actor) -> None:
        actor.ability_to(BrowseTheWeb).page.goto(self.url)

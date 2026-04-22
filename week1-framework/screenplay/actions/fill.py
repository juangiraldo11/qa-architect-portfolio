from ..actor import Actor
from ..abilities.browse_the_web import BrowseTheWeb
from ..targets import Target


class Fill:
    def __init__(self, target: Target, value: str = ""):
        self.target = target
        self.value = value

    @classmethod
    def field(cls, target: Target) -> "Fill":
        return cls(target)

    def with_(self, value: str) -> "Fill":
        self.value = value
        return self

    def perform_as(self, actor: Actor) -> None:
        actor.ability_to(BrowseTheWeb).page.fill(self.target.selector, self.value)

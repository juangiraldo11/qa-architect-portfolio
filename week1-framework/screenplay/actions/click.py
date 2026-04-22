from ..actor import Actor
from ..abilities.browse_the_web import BrowseTheWeb
from ..targets import Target


class Click:
    def __init__(self, target: Target):
        self.target = target

    @classmethod
    def on(cls, target: Target) -> "Click":
        return cls(target)

    def perform_as(self, actor: Actor) -> None:
        actor.ability_to(BrowseTheWeb).page.click(self.target.selector)

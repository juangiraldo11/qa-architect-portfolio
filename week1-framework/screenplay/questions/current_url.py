from ..actor import Actor
from ..abilities.browse_the_web import BrowseTheWeb


class CurrentUrl:
    @classmethod
    def value(cls) -> "CurrentUrl":
        return cls()

    def answered_by(self, actor: Actor) -> str:
        return actor.ability_to(BrowseTheWeb).page.url

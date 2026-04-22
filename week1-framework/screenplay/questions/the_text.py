from ..actor import Actor
from ..abilities.browse_the_web import BrowseTheWeb
from ..targets import Target


class TheText:
    def __init__(self, target: Target):
        self.target = target

    @classmethod
    def of(cls, target: Target) -> "TheText":
        return cls(target)

    def answered_by(self, actor: Actor) -> str:
        return actor.ability_to(BrowseTheWeb).page.text_content(self.target.selector) or ""

from typing import Protocol, runtime_checkable

@runtime_checkable
class Performable(Protocol):
    """Cualquier cosa que un Actor pueda ejecutar."""
    def perform_as(self, actor: "Actor") -> None: ...

@runtime_checkable
class Question(Protocol):
    """Cualquier cosa que un Actor pueda consultar."""
    def answered_by(self, actor: "Actor"): ...

class Actor:
    def __init__(self, name: str):
        self.name = name
        self._abilities = {}

    @classmethod
    def named(cls, name: str) -> "Actor":
        return cls(name)

    def who_can(self, *abilities) -> "Actor":
        for ability in abilities:
            self._abilities[type(ability)] = ability
        return self

    def ability_to(self, ability_class):
        if ability_class not in self._abilities:
            raise RuntimeError(f"{self.name} cannot {ability_class.__name__}")
        return self._abilities[ability_class]

    def attempts_to(self, *performables: Performable) -> "Actor":
        for p in performables:
            p.perform_as(self)
        return self

    def asks(self, question: Question):
        return question.answered_by(self)
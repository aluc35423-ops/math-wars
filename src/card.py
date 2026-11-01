from dataclasses import dataclass, replace


@dataclass(eq=False)  # eq=False: dos cartas iguales siguen siendo objetos distintos
class Card:
    name: str
    cost: int
    attack: int
    hp: int
    color: tuple

    def clone(self):
        return replace(self)

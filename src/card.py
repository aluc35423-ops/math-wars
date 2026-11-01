from dataclasses import dataclass, field, replace


@dataclass(eq=False)  # eq=False: dos cartas iguales siguen siendo objetos distintos
class Card:
    name: str
    cost: int
    attack: int
    hp: int
    color: tuple
    symbol: str = "?"                       # símbolo matemático que se dibuja en la carta
    max_hp: int = field(init=False, default=0)

    def __post_init__(self):
        self.max_hp = self.hp               # sirve para mostrar si la criatura está dañada

    def clone(self):
        return replace(self)

import random
from src.card_data import CARD_LIBRARY


class Deck:
    def __init__(self, size=24):
        # Más cartas baratas que caras, como en Card Wars
        weights = [max(1, 6 - c.cost) for c in CARD_LIBRARY]
        self.cards = [c.clone() for c in random.choices(CARD_LIBRARY, weights, k=size)]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def __len__(self):
        return len(self.cards)

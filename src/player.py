from src.settings import *
from src.deck import Deck


class Player:
    def __init__(self, name):
        self.name = name
        self.hp = START_HP
        self.deck = Deck()
        self.hand = []
        self.board = [None] * LANES   # una criatura por línea
        self.max_energy = 2
        self.energy = 0
        self.draw_cards(START_HAND)

    def draw_cards(self, n=1):
        for _ in range(n):
            if len(self.hand) >= MAX_HAND:
                break
            card = self.deck.draw()
            if card:
                self.hand.append(card)

    def start_turn(self):
        self.max_energy = min(self.max_energy + 1, MAX_ENERGY)
        self.energy = self.max_energy
        self.draw_cards(1)

    def can_play(self, card):
        return card.cost <= self.energy

    def play_card(self, card, lane):
        self.energy -= card.cost
        self.hand.remove(card)
        self.board[lane] = card

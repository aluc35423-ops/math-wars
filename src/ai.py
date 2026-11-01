"""IA sencilla del rival: juega las cartas más caras que pueda pagar."""
import random


def play_turn(enemy):
    enemy.start_turn()
    while True:
        free = [i for i, c in enumerate(enemy.board) if c is None]
        playable = [c for c in enemy.hand if enemy.can_play(c)]
        if not free or not playable:
            break
        card = max(playable, key=lambda c: c.cost)
        enemy.play_card(card, random.choice(free))

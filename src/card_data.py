"""Catálogo de cartas. Agrega aquí nuevas criaturas fácilmente."""
from src.card import Card

CARD_LIBRARY = [
    Card("Sapo Suma",      1, 1, 2, (46, 139, 87),   "+"),
    Card("Gato Resta",     1, 2, 1, (186, 85, 120),  "-"),
    Card("Mago Multi",     2, 2, 3, (123, 97, 200),  "×"),
    Card("Robot Divide",   2, 3, 2, (90, 130, 170),  "÷"),
    Card("Dino Decimal",   3, 3, 4, (200, 130, 50),  "0.5"),
    Card("Ninja Potencia", 3, 4, 3, (60, 60, 110),   "x²"),
    Card("Golem Raíz",     4, 5, 5, (130, 110, 90),  "√"),
    Card("Dragón Pi",      4, 6, 4, (190, 70, 60),   "π"),
    Card("Rey Álgebra",    5, 7, 6, (170, 140, 40),  "x"),
]

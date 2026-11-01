"""Constantes globales del juego."""
WIDTH, HEIGHT = 1100, 720
FPS = 60
TITLE = "Math Wars - Cartas Educativas"

# Tamaño de carta y reglas
CARD_W, CARD_H = 120, 160
LANES = 4            # líneas de batalla por jugador
START_HP = 25
START_HAND = 4
MAX_HAND = 7
MAX_ENERGY = 6

# Colores
BG = (30, 34, 54)
PANEL = (44, 50, 78)
WHITE = (255, 255, 255)
BLACK = (15, 15, 25)
GOLD = (255, 206, 84)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
GRAY = (120, 125, 150)

# --- Paleta ampliada (parte 6: mejora de diseño) ---
BG_TOP = (22, 24, 48)          # fondo: degradado índigo -> violeta
BG_BOTTOM = (48, 32, 84)
PANEL_DARK = (20, 22, 40)
GRAY_DARK = (70, 76, 110)
PURPLE = (111, 66, 193)
ORANGE = (230, 126, 34)
GREEN_DARK = (39, 174, 96)
RED_DARK = (192, 57, 43)

# Color del borde de cada carta según su coste (de bronce a oro)
RARITY = {
    1: (176, 141, 87),
    2: (190, 195, 205),
    3: (88, 166, 255),
    4: (186, 104, 200),
    5: (255, 206, 84),
}

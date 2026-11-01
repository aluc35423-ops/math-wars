"""Componentes visuales reutilizables: texto, paneles, botones, cartas, HUD y efectos."""
import random
import pygame
from src.settings import *

FONT_NAMES = "segoeui,trebuchetms,verdana,dejavusans,arial"
_fonts = {}
_face_cache = {}
_shadow_cache = {}
_dim_cache = {}


# ---------------------------------------------------------------- utilidades
def get_font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont(FONT_NAMES, size, bold=bold)
    return _fonts[key]


def lighten(color, f):
    return tuple(min(255, int(c + (255 - c) * f)) for c in color)


def darken(color, f):
    return tuple(int(c * (1 - f)) for c in color)


def draw_text(surface, text, pos, size=20, color=WHITE, center=False, bold=False,
              shadow=False, midleft=False):
    font = get_font(size, bold)

    def place(img, offset=0):
        p = (pos[0] + offset, pos[1] + offset)
        if center:
            return img.get_rect(center=p)
        if midleft:
            return img.get_rect(midleft=p)
        return img.get_rect(topleft=p)

    if shadow:
        sh = font.render(text, True, BLACK)
        surface.blit(sh, place(sh, 2))
    img = font.render(text, True, color)
    rect = place(img)
    surface.blit(img, rect)
    return rect


def draw_fitted_text(surface, text, center, max_w, size=20, color=WHITE, bold=True,
                     shadow=False, min_size=9):
    """Texto centrado que reduce su tamaño hasta caber en max_w."""
    while size > min_size and get_font(size, bold).size(text)[0] > max_w:
        size -= 1
    return draw_text(surface, text, center, size, color, True, bold, shadow)


def draw_shadow(surface, rect, radius=12, offset=(4, 6), alpha=90):
    key = (rect.w, rect.h, radius, alpha)
    if key not in _shadow_cache:
        s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, alpha), s.get_rect(), border_radius=radius)
        _shadow_cache[key] = s
    surface.blit(_shadow_cache[key], (rect.x + offset[0], rect.y + offset[1]))


def dim_screen(surface, alpha=170):
    """Oscurece toda la pantalla (fondo de ventanas emergentes)."""
    key = (surface.get_width(), surface.get_height(), alpha)
    if key not in _dim_cache:
        s = pygame.Surface((key[0], key[1]), pygame.SRCALPHA)
        s.fill((8, 8, 20, alpha))
        _dim_cache[key] = s
    surface.blit(_dim_cache[key], (0, 0))


def draw_dim(surface, rect, alpha=120, radius=12):
    key = (rect.w, rect.h, alpha, radius)
    if key not in _dim_cache:
        s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (8, 8, 20, alpha), s.get_rect(), border_radius=radius)
        _dim_cache[key] = s
    surface.blit(_dim_cache[key], rect.topleft)


def draw_panel(surface, rect, fill=PANEL, border=None, radius=14, shadow=True):
    if shadow:
        draw_shadow(surface, rect, radius, (0, 5), 80)
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, 2, border_radius=radius)


def draw_button(surface, rect, text, mouse, color=GREEN, text_color=BLACK, size=20, enabled=True):
    hover = enabled and rect.collidepoint(mouse)
    base = color if enabled else GRAY_DARK
    draw_shadow(surface, rect, 12, (0, 5), 110)
    r = rect.move(0, -2) if hover else rect
    pygame.draw.rect(surface, lighten(base, 0.18) if hover else base, r, border_radius=12)
    pygame.draw.rect(surface, darken(base, 0.35), r, 2, border_radius=12)
    draw_text(surface, text, r.center, size, text_color if enabled else GRAY, True, True)
    return hover


# ---------------------------------------------------------------- fondo
def make_background():
    """Degradado índigo-violeta con símbolos matemáticos muy tenues. Se genera una sola vez."""
    bg = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        t = y / HEIGHT
        color = tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3))
        pygame.draw.line(bg, color, (0, y), (WIDTH, y))
    rng = random.Random(7)
    font = get_font(44, True)
    for _ in range(28):
        img = font.render(rng.choice(["+", "-", "×", "÷", "=", "π", "√", "%", "x²"]), True, WHITE)
        img.set_alpha(14)
        bg.blit(img, (rng.randint(0, WIDTH), rng.randint(0, HEIGHT)))
    return bg


# ---------------------------------------------------------------- cartas
def _card_face(card, size):
    key = (card.name, card.hp, card.attack, size)
    if key in _face_cache:
        return _face_cache[key]
    w, h = size
    face = pygame.Surface(size, pygame.SRCALPHA)
    full = pygame.Rect(0, 0, w, h)
    pygame.draw.rect(face, RARITY.get(card.cost, GRAY), full, border_radius=12)
    pygame.draw.rect(face, darken(card.color, 0.55), full.inflate(-8, -8), border_radius=9)

    # ventana de arte con el símbolo matemático de la criatura
    art = pygame.Rect(12, 12, w - 24, 76)
    pygame.draw.rect(face, lighten(card.color, 0.15), art, border_radius=8)
    pygame.draw.circle(face, lighten(card.color, 0.35), art.center, 31)
    pygame.draw.circle(face, card.color, art.center, 25)
    pygame.draw.rect(face, darken(card.color, 0.4), art, 2, border_radius=8)
    draw_fitted_text(face, card.symbol, art.center, 40, 44, WHITE, True, shadow=True)

    # gema de coste
    pygame.draw.circle(face, BLUE, (17, 17), 13)
    pygame.draw.circle(face, WHITE, (17, 17), 13, 2)
    draw_text(face, str(card.cost), (17, 17), 16, WHITE, True, True)

    # placa con el nombre
    plate = pygame.Rect(10, 94, w - 20, 20)
    pygame.draw.rect(face, PANEL_DARK, plate, border_radius=6)
    draw_fitted_text(face, card.name, plate.center, plate.w - 8, 13, WHITE, True)

    # ataque y vida (la vida cambia de color si la criatura está dañada)
    pw = (w - 30) // 2
    atk = pygame.Rect(10, h - 34, pw, 24)
    hp = pygame.Rect(w - 10 - pw, h - 34, pw, 24)
    pygame.draw.rect(face, RED_DARK, atk, border_radius=8)
    pygame.draw.rect(face, ORANGE if card.hp < card.max_hp else GREEN_DARK, hp, border_radius=8)
    draw_fitted_text(face, f"ATK {card.attack}", atk.center, pw - 6, 13, WHITE, True)
    draw_fitted_text(face, f"HP {card.hp}", hp.center, pw - 6, 13, WHITE, True)

    _face_cache[key] = face
    return face


def draw_card(surface, card, rect, selected=False):
    draw_shadow(surface, rect, 12, (4, 7), 110)
    surface.blit(_card_face(card, rect.size), rect.topleft)
    if selected:
        pygame.draw.rect(surface, GOLD, rect.inflate(8, 8), 3, border_radius=15)


def draw_card_back(surface, rect, count=None):
    draw_shadow(surface, rect, 12, (4, 7), 110)
    pygame.draw.rect(surface, PURPLE, rect, border_radius=12)
    pygame.draw.rect(surface, darken(PURPLE, 0.45), rect.inflate(-12, -12), border_radius=8)
    pygame.draw.rect(surface, GOLD, rect.inflate(-12, -12), 2, border_radius=8)
    draw_text(surface, "MW", rect.center, 34, GOLD, True, True, shadow=True)
    if count is not None:
        draw_text(surface, f"{count} cartas", (rect.centerx, rect.bottom - 22), 14, WHITE, True, True)


# ---------------------------------------------------------------- HUD
def draw_hp_bar(surface, rect, hp, max_hp):
    ratio = max(0.0, min(1.0, hp / max_hp))
    radius = rect.h // 2
    pygame.draw.rect(surface, PANEL_DARK, rect, border_radius=radius)
    if ratio > 0:
        color = GREEN if ratio > 0.5 else (GOLD if ratio > 0.25 else RED)
        fill = pygame.Rect(rect.x, rect.y, max(rect.h, int(rect.w * ratio)), rect.h)
        pygame.draw.rect(surface, color, fill, border_radius=radius)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=radius)
    draw_text(surface, f"{max(0, hp)} / {max_hp}", rect.center, 14, WHITE, True, True, shadow=True)


def draw_energy(surface, x, y, energy, max_energy):
    for i in range(MAX_ENERGY):
        c = (x + i * 22, y)
        if i < energy:
            pygame.draw.circle(surface, GOLD, c, 8)
            pygame.draw.circle(surface, lighten(GOLD, 0.7), (c[0] - 2, c[1] - 2), 3)
        elif i < max_energy:
            pygame.draw.circle(surface, GOLD, c, 8, 2)
        else:
            pygame.draw.circle(surface, GRAY_DARK, c, 5, 1)


def draw_hud(surface, rect, player, accent):
    draw_panel(surface, rect, PANEL_DARK, GRAY_DARK, 12)
    pygame.draw.rect(surface, accent, (rect.x + 6, rect.y + 8, 5, rect.h - 16), border_radius=3)
    draw_text(surface, player.name, (rect.x + 22, rect.centery), 18, WHITE, bold=True, midleft=True)
    draw_hp_bar(surface, pygame.Rect(rect.x + 128, rect.centery - 10, 220, 20), player.hp, START_HP)
    draw_text(surface, "Energía", (rect.x + 372, rect.y + 5), 11, GRAY)
    draw_energy(surface, rect.x + 380, rect.bottom - 15, player.energy, player.max_energy)


# ---------------------------------------------------------------- efectos
class FloatingText:
    """Número de daño que sube y se desvanece."""

    def __init__(self, text, pos, color, size=30, life=1.1):
        self.text, self.x, self.y = text, pos[0], pos[1]
        self.color, self.size, self.life, self.age = color, size, life, 0.0

    @property
    def alive(self):
        return self.age < self.life

    def update(self, dt):
        self.age += dt
        self.y -= 40 * dt

    def draw(self, surface):
        alpha = max(0, int(255 * (1 - self.age / self.life)))
        font = get_font(self.size, True)
        img = font.render(self.text, True, self.color)
        shadow = font.render(self.text, True, BLACK)
        img.set_alpha(alpha)
        shadow.set_alpha(alpha)
        rect = img.get_rect(center=(self.x, self.y))
        surface.blit(shadow, rect.move(2, 2))
        surface.blit(img, rect)

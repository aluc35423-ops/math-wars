"""Funciones de dibujo reutilizables."""
import pygame
from src.settings import *

_fonts = {}


def get_font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont("arial", size, bold=bold)
    return _fonts[key]


def draw_text(surface, text, pos, size=20, color=WHITE, center=False, bold=False):
    img = get_font(size, bold).render(text, True, color)
    rect = img.get_rect(center=pos) if center else img.get_rect(topleft=pos)
    surface.blit(img, rect)
    return rect


def draw_card(surface, card, rect, selected=False):
    pygame.draw.rect(surface, card.color, rect, border_radius=10)
    pygame.draw.rect(surface, GOLD if selected else BLACK, rect,
                     4 if selected else 2, border_radius=10)
    pygame.draw.circle(surface, BLUE, (rect.left + 20, rect.top + 20), 15)
    draw_text(surface, str(card.cost), (rect.left + 20, rect.top + 20), 18, WHITE, True, True)
    draw_text(surface, card.name, (rect.centerx, rect.top + 62), 15, WHITE, True, True)
    draw_text(surface, f"ATK {card.attack}", (rect.left + 10, rect.bottom - 28), 16, GOLD, bold=True)
    draw_text(surface, f"HP {card.hp}", (rect.right - 58, rect.bottom - 28), 16, GREEN, bold=True)

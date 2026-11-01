import pygame
from src.settings import *
from src.ui import (draw_text, draw_fitted_text, draw_panel, dim_screen, lighten, darken)


class QuizModal:
    """Ventana emergente con una pregunta. Llama on_done(correcto) al cerrarse."""

    def __init__(self, question, on_done):
        self.q = question
        self.on_done = on_done
        self.chosen = None
        self.panel = pygame.Rect(0, 0, 680, 450)
        self.panel.center = (WIDTH // 2, HEIGHT // 2)
        self.buttons = []
        for i in range(len(question.options)):
            r = pygame.Rect(0, 0, 290, 58)
            r.topleft = (self.panel.left + 30 + (i % 2) * 330,
                         self.panel.top + 180 + (i // 2) * 76)
            self.buttons.append(r)

    def handle_click(self, pos):
        """Devuelve True cuando el modal terminó y debe cerrarse."""
        if self.chosen is None:
            for i, r in enumerate(self.buttons):
                if r.collidepoint(pos):
                    self.chosen = i
            return False
        self.on_done(self.chosen == self.q.answer)
        return True

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        p = self.panel
        dim_screen(surface, 175)
        draw_panel(surface, p, PANEL, GOLD, 20)

        # encabezado: tema y dificultad
        header = pygame.Rect(p.left, p.top, p.w, 56)
        pygame.draw.rect(surface, PANEL_DARK, header, border_top_left_radius=20,
                         border_top_right_radius=20)
        draw_text(surface, f"Reto: {self.q.topic}", (p.left + 26, header.centery), 22, GOLD,
                  bold=True, midleft=True)
        for i in range(5):
            c = (p.right - 30 - (4 - i) * 20, header.centery)
            if i < self.q.level:
                pygame.draw.circle(surface, GOLD, c, 7)
            else:
                pygame.draw.circle(surface, GRAY_DARK, c, 7, 2)

        draw_text(surface, "Acierta para invocar tu criatura", (p.centerx, p.top + 82), 15, GRAY, True)
        draw_fitted_text(surface, self.q.text, (p.centerx, p.top + 132), p.w - 60, 44, WHITE, True)

        # opciones
        for i, r in enumerate(self.buttons):
            if self.chosen is None:
                color = lighten(BLUE, 0.2) if r.collidepoint(mouse) else BLUE
            elif i == self.q.answer:
                color = GREEN_DARK
            elif i == self.chosen:
                color = RED_DARK
            else:
                color = GRAY_DARK
            pygame.draw.rect(surface, color, r, border_radius=12)
            pygame.draw.rect(surface, darken(color, 0.4), r, 2, border_radius=12)
            pygame.draw.circle(surface, WHITE, (r.left + 30, r.centery), 16)
            draw_text(surface, "ABCD"[i], (r.left + 30, r.centery), 18, darken(color, 0.4), True, True)
            draw_fitted_text(surface, self.q.options[i], (r.centerx + 16, r.centery), r.w - 90, 28,
                             WHITE, True)

        # resultado
        if self.chosen is not None:
            ok = self.chosen == self.q.answer
            banner = pygame.Rect(p.left + 30, p.top + 336, p.w - 60, 42)
            pygame.draw.rect(surface, GREEN_DARK if ok else RED_DARK, banner, border_radius=10)
            draw_text(surface, "¡Correcto!" if ok else "Casi, revisa la explicación",
                      banner.center, 22, WHITE, True, True)
            draw_fitted_text(surface, self.q.explanation, (p.centerx, p.top + 398), p.w - 60, 17,
                             WHITE, False)
            draw_text(surface, "Haz clic para continuar", (p.centerx, p.top + 428), 14, GRAY, True)

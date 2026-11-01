import pygame
from src.settings import *
from src.ui import draw_text


class QuizModal:
    """Ventana emergente con una pregunta. Llama on_done(correcto) al cerrarse."""

    def __init__(self, question, on_done):
        self.q = question
        self.on_done = on_done
        self.chosen = None
        self.panel = pygame.Rect(0, 0, 640, 420)
        self.panel.center = (WIDTH // 2, HEIGHT // 2)
        self.buttons = []
        for i in range(len(question.options)):
            r = pygame.Rect(0, 0, 260, 56)
            r.topleft = (self.panel.left + 40 + (i % 2) * 300,
                         self.panel.top + 170 + (i // 2) * 76)
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
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))
        pygame.draw.rect(surface, PANEL, self.panel, border_radius=16)
        pygame.draw.rect(surface, GOLD, self.panel, 3, border_radius=16)
        cx = self.panel.centerx
        draw_text(surface, "¡Reto para jugar la carta!", (cx, self.panel.top + 35), 26, GOLD, True, True)
        draw_text(surface, self.q.text, (cx, self.panel.top + 100), 34, WHITE, True, True)
        for i, r in enumerate(self.buttons):
            color = BLUE
            if self.chosen is not None:
                color = GREEN if i == self.q.answer else (RED if i == self.chosen else GRAY)
            pygame.draw.rect(surface, color, r, border_radius=10)
            draw_text(surface, self.q.options[i], r.center, 26, WHITE, True, True)
        if self.chosen is not None:
            ok = self.chosen == self.q.answer
            draw_text(surface, "¡Correcto!" if ok else "Casi... revisa la explicación",
                      (cx, self.panel.top + 335), 22, GREEN if ok else RED, True, True)
            draw_text(surface, self.q.explanation, (cx, self.panel.top + 365), 16, WHITE, True)
            draw_text(surface, "Haz clic para continuar", (cx, self.panel.top + 398), 14, GRAY, True)

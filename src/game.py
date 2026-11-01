import math
import pygame
from src.settings import *
from src.player import Player
from src.card_data import CARD_LIBRARY
from src.questions import generate_question
from src.quiz import QuizModal
from src.combat import resolve_attacks, winner
from src import ai
from src.ui import (draw_card, draw_card_back, draw_text, draw_fitted_text, draw_panel,
                    draw_button, draw_hud, draw_dim, dim_screen, make_background,
                    FloatingText, lighten)

# ---- disposición de la pantalla de juego ----
ENEMY_HUD_Y = 12
ENEMY_Y = 70
RIBBON_Y = 236
PLAYER_Y = 278
PLAYER_HUD_Y = 448
HUD_W, HUD_H = 540, 48
HUD_X = (WIDTH - HUD_W) // 2


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"                      # "menu" o "playing"
        self.bg = self.build_background()
        self.end_btn = pygame.Rect(WIDTH - 230, PLAYER_Y + 52, 180, 56)
        self.play_btn = pygame.Rect(0, 0, 260, 64)
        self.play_btn.center = (WIDTH // 2, 470)
        self.menu_cards = [CARD_LIBRARY[0].clone(), CARD_LIBRARY[2].clone(), CARD_LIBRARY[8].clone()]
        self.new_game()

    def build_background(self):
        bg = make_background()
        for y, tint in ((ENEMY_Y - 14, (231, 76, 60, 30)), (PLAYER_Y - 14, (52, 152, 219, 30))):
            panel = pygame.Surface((620, CARD_H + 28), pygame.SRCALPHA)
            pygame.draw.rect(panel, tint, panel.get_rect(), border_radius=18)
            bg.blit(panel, ((WIDTH - 620) // 2, y))
        return bg

    def new_game(self):
        self.player = Player("Jugador")
        self.enemy = Player("Rival")
        self.selected = None
        self.quiz = None
        self.winner = None
        self.floaters = []
        self.message = "Elige una carta de tu mano y luego una línea libre."
        self.player.start_turn()

    def start_game(self):
        self.new_game()
        self.state = "playing"

    # ---------- geometría ----------
    def lane_rect(self, i, y):
        gap = 20
        total = LANES * CARD_W + (LANES - 1) * gap
        x = (WIDTH - total) // 2 + i * (CARD_W + gap)
        return pygame.Rect(x, y, CARD_W, CARD_H)

    def hand_rect(self, i, n):
        gap = 12
        total = n * CARD_W + (n - 1) * gap
        x = (WIDTH - total) // 2 + i * (CARD_W + gap)
        return pygame.Rect(x, HEIGHT - CARD_H - 15, CARD_W, CARD_H)

    def hand_hit_rect(self, i, n):
        r = self.hand_rect(i, n)
        return pygame.Rect(r.x, r.y - 18, r.w, r.h + 18)   # incluye la zona donde sube al seleccionarla

    # ---------- lógica ----------
    def try_play(self, lane):
        card = self.selected
        if self.player.board[lane] is not None:
            self.message = "Esa línea ya está ocupada."
        elif not self.player.can_play(card):
            self.message = "No tienes energía suficiente."
        else:
            # El nivel de dificultad de la pregunta depende del coste de la carta
            question = generate_question(card.cost)
            self.quiz = QuizModal(question, lambda ok: self.resolve_quiz(ok, card, lane))

    def resolve_quiz(self, correct, card, lane):
        if correct:
            self.player.play_card(card, lane)
            self.message = f"¡Correcto! {card.name} entra al campo."
        else:
            self.player.energy = max(0, self.player.energy - 1)
            self.message = "Respuesta incorrecta: pierdes 1 de energía. ¡Inténtalo de nuevo!"
        self.selected = None

    def spawn_hits(self, events, board_y, hud_y):
        """Crea los números de daño flotantes a partir de los eventos de combate."""
        for lane, amount, direct in events:
            if direct:
                pos, color, size = (WIDTH // 2, hud_y + HUD_H // 2), RED, 36
            else:
                pos, color, size = self.lane_rect(lane, board_y).center, GOLD, 30
            self.floaters.append(FloatingText(f"-{amount}", pos, color, size))

    def end_turn(self):
        self.selected = None
        events = []
        log = resolve_attacks(self.player, self.enemy, events)
        self.spawn_hits(events, ENEMY_Y, ENEMY_HUD_Y)
        if self.check_winner():
            return
        ai.play_turn(self.enemy)
        events = []
        log += resolve_attacks(self.enemy, self.player, events)
        self.spawn_hits(events, PLAYER_Y, PLAYER_HUD_Y)
        if self.check_winner():
            return
        self.player.start_turn()
        self.message = " | ".join(log[-2:]) if log else "Nuevo turno."

    def check_winner(self):
        self.winner = winner(self.player, self.enemy)
        return self.winner is not None

    # ---------- eventos ----------
    def on_click(self, pos):
        if self.state == "menu":
            if self.play_btn.collidepoint(pos):
                self.start_game()
            return
        if self.quiz:
            if self.quiz.handle_click(pos):
                self.quiz = None
            return
        if self.winner:
            return
        if self.end_btn.collidepoint(pos):
            self.end_turn()
            return
        n = len(self.player.hand)
        for i, card in enumerate(self.player.hand):
            if self.hand_hit_rect(i, n).collidepoint(pos):
                self.selected = card
                return
        if self.selected:
            for i in range(LANES):
                if self.lane_rect(i, PLAYER_Y).collidepoint(pos):
                    self.try_play(i)
                    return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.state == "menu" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_game()
                elif self.state == "playing" and self.winner and event.key == pygame.K_r:
                    self.start_game()
                elif self.state == "playing" and self.winner and event.key == pygame.K_m:
                    self.state = "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_click(event.pos)

    def update(self, dt):
        for f in self.floaters:
            f.update(dt)
        self.floaters = [f for f in self.floaters if f.alive]

    # ---------- dibujo: tablero ----------
    def draw_board(self, player, y, is_player):
        mouse = pygame.mouse.get_pos()
        pulse = (math.sin(pygame.time.get_ticks() / 220) + 1) / 2
        for i in range(LANES):
            rect = self.lane_rect(i, y)
            card = player.board[i]
            usable = (is_player and card is None and self.selected is not None
                      and self.player.can_play(self.selected) and not self.quiz)
            pygame.draw.rect(self.screen, (24, 28, 54), rect, border_radius=12)
            pygame.draw.rect(self.screen, GRAY_DARK, rect, 2, border_radius=12)
            if card:
                draw_card(self.screen, card, rect)
            else:
                draw_text(self.screen, str(i + 1), rect.center, 44, (58, 64, 100), True, True)
            if usable:
                width = 4 if rect.collidepoint(mouse) else 2
                pygame.draw.rect(self.screen, lighten(GOLD, 0.5 * pulse), rect, width, border_radius=12)

    def draw_ribbon(self):
        rect = pygame.Rect(0, RIBBON_Y, 780, 36)
        rect.centerx = WIDTH // 2
        draw_panel(self.screen, rect, PANEL_DARK, GOLD, 18, shadow=False)
        draw_fitted_text(self.screen, self.message, rect.center, rect.w - 40, 17, WHITE, False)

    def draw_hand(self):
        mouse = pygame.mouse.get_pos()
        n = len(self.player.hand)
        for i, card in enumerate(self.player.hand):
            rect = self.hand_rect(i, n)
            hovered = self.hand_hit_rect(i, n).collidepoint(mouse) and not self.quiz and not self.winner
            if card is self.selected:
                rect.y -= 18
            elif hovered:
                rect.y -= 10
            draw_card(self.screen, card, rect, card is self.selected)
            if not self.player.can_play(card):
                draw_dim(self.screen, rect, 130)

    def draw_playing(self):
        mouse = pygame.mouse.get_pos()
        self.screen.blit(self.bg, (0, 0))
        draw_hud(self.screen, pygame.Rect(HUD_X, ENEMY_HUD_Y, HUD_W, HUD_H), self.enemy, RED)
        draw_hud(self.screen, pygame.Rect(HUD_X, PLAYER_HUD_Y, HUD_W, HUD_H), self.player, BLUE)

        # mazos a la izquierda del tablero
        draw_card_back(self.screen, pygame.Rect(80, ENEMY_Y, CARD_W, CARD_H), len(self.enemy.deck))
        draw_text(self.screen, f"Mano del rival: {len(self.enemy.hand)}",
                  (80 + CARD_W // 2, ENEMY_Y + CARD_H + 16), 14, GRAY, True)
        draw_card_back(self.screen, pygame.Rect(80, PLAYER_Y, CARD_W, CARD_H), len(self.player.deck))
        draw_text(self.screen, "Tu mazo", (80 + CARD_W // 2, PLAYER_Y + CARD_H + 16), 14, GRAY, True)

        self.draw_board(self.enemy, ENEMY_Y, False)
        self.draw_ribbon()
        self.draw_board(self.player, PLAYER_Y, True)

        enabled = not self.quiz and not self.winner
        draw_button(self.screen, self.end_btn, "Terminar turno", mouse, GREEN, BLACK, 20, enabled)
        self.draw_hand()

        for f in self.floaters:
            f.draw(self.screen)
        if self.quiz:
            self.quiz.draw(self.screen)
        if self.winner:
            self.draw_game_over()

    # ---------- dibujo: menú y fin de partida ----------
    def draw_menu(self):
        mouse = pygame.mouse.get_pos()
        self.screen.blit(self.bg, (0, 0))
        draw_text(self.screen, "MATH WARS", (WIDTH // 2, 110), 88, GOLD, True, True, shadow=True)
        draw_text(self.screen, "El duelo de cartas donde las matemáticas son tu poder",
                  (WIDTH // 2, 178), 22, WHITE, True)
        for k, card in enumerate(self.menu_cards):
            x = WIDTH // 2 + (k - 1) * (CARD_W + 40) - CARD_W // 2
            draw_card(self.screen, card, pygame.Rect(x, 225, CARD_W, CARD_H))
        draw_button(self.screen, self.play_btn, "Jugar", mouse, GOLD, BLACK, 32)

        panel = pygame.Rect(0, 0, 780, 92)
        panel.center = (WIDTH // 2, 590)
        draw_panel(self.screen, panel, PANEL_DARK, GRAY_DARK, 16)
        steps = ["Elige una carta", "Colócala en una línea", "Resuelve el reto", "Termina turno y ataca"]
        col = panel.w // len(steps)
        for i, text in enumerate(steps):
            cx = panel.left + col * i + col // 2
            pygame.draw.circle(self.screen, GOLD, (cx, panel.top + 30), 14)
            draw_text(self.screen, str(i + 1), (cx, panel.top + 30), 18, BLACK, True, True)
            draw_fitted_text(self.screen, text, (cx, panel.top + 64), col - 16, 16, WHITE, False)
        draw_text(self.screen, "Pulsa Enter para jugar o Esc para salir",
                  (WIDTH // 2, 676), 14, GRAY, True)

    def draw_game_over(self):
        dim_screen(self.screen, 185)
        won = self.winner == "player"
        panel = pygame.Rect(0, 0, 600, 240)
        panel.center = (WIDTH // 2, HEIGHT // 2)
        draw_panel(self.screen, panel, PANEL, GOLD if won else RED, 20)
        draw_text(self.screen, "¡Ganaste, crack de las mates!" if won else "El rival ganó esta vez",
                  (panel.centerx, panel.top + 70), 36, GOLD if won else RED, True, True, shadow=True)
        draw_text(self.screen,
                  "Tus criaturas dominaron el tablero." if won else "Practica un poco más y vuelve a intentarlo.",
                  (panel.centerx, panel.top + 125), 18, WHITE, True)
        draw_text(self.screen, "Pulsa R para jugar de nuevo o M para volver al menú.",
                  (panel.centerx, panel.top + 190), 16, GRAY, True)

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        else:
            self.draw_playing()
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

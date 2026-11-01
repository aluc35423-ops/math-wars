import pygame
from src.settings import *
from src.player import Player
from src.ui import draw_card, draw_text
from src.questions import generate_question
from src.quiz import QuizModal
from src.combat import resolve_attacks, winner
from src import ai

ENEMY_Y = 70
PLAYER_Y = 280


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.end_btn = pygame.Rect(WIDTH - 190, PLAYER_Y + 50, 160, 50)
        self.new_game()

    def new_game(self):
        self.player = Player("Jugador")
        self.enemy = Player("Rival")
        self.selected = None
        self.quiz = None
        self.winner = None
        self.message = "Elige una carta de tu mano y luego una línea libre."
        self.player.start_turn()

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

    def end_turn(self):
        self.selected = None
        log = resolve_attacks(self.player, self.enemy)
        if self.check_winner():
            return
        ai.play_turn(self.enemy)
        log += resolve_attacks(self.enemy, self.player)
        if self.check_winner():
            return
        self.player.start_turn()
        self.message = " | ".join(log[-2:]) if log else "Nuevo turno."

    def check_winner(self):
        self.winner = winner(self.player, self.enemy)
        return self.winner is not None

    def on_click(self, pos):
        if self.winner:
            return
        if self.quiz:
            if self.quiz.handle_click(pos):
                self.quiz = None
            return
        if self.end_btn.collidepoint(pos):
            self.end_turn()
            return
        n = len(self.player.hand)
        for i, card in enumerate(self.player.hand):
            if self.hand_rect(i, n).collidepoint(pos):
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.winner:
                self.new_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_click(event.pos)

    def update(self):
        pass

    # ---------- dibujo ----------
    def draw_board(self, player, y):
        for i in range(LANES):
            rect = self.lane_rect(i, y)
            pygame.draw.rect(self.screen, PANEL, rect, border_radius=10)
            pygame.draw.rect(self.screen, GRAY, rect, 2, border_radius=10)
            card = player.board[i]
            if card:
                draw_card(self.screen, card, rect)

    def draw_hud(self, player, y):
        draw_text(self.screen, f"{player.name}   Vida: {player.hp}   Energía: {player.energy}/{player.max_energy}",
                  (30, y), 22, WHITE, bold=True)

    def draw(self):
        self.screen.fill(BG)
        self.draw_board(self.enemy, ENEMY_Y)
        self.draw_board(self.player, PLAYER_Y)
        self.draw_hud(self.enemy, 20)
        self.draw_hud(self.player, PLAYER_Y + CARD_H + 15)
        draw_text(self.screen, self.message, (30, PLAYER_Y + CARD_H + 50), 18, GOLD)
        pygame.draw.rect(self.screen, GREEN, self.end_btn, border_radius=10)
        draw_text(self.screen, "Terminar turno", self.end_btn.center, 18, BLACK, True, True)
        n = len(self.player.hand)
        for i, card in enumerate(self.player.hand):
            rect = self.hand_rect(i, n)
            if card is self.selected:
                rect.y -= 18
            draw_card(self.screen, card, rect, card is self.selected)
        if self.quiz:
            self.quiz.draw(self.screen)
        if self.winner:
            self.draw_game_over()
        pygame.display.flip()

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        won = self.winner == "player"
        draw_text(self.screen, "¡Ganaste, crack de las mates!" if won else "El rival ganó esta vez",
                  (WIDTH // 2, HEIGHT // 2 - 20), 40, GOLD if won else RED, True, True)
        draw_text(self.screen, "Presiona R para jugar de nuevo",
                  (WIDTH // 2, HEIGHT // 2 + 30), 22, WHITE, True)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

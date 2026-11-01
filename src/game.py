import pygame
from src.settings import *
from src.player import Player
from src.ui import draw_card, draw_text

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
            self.player.play_card(card, lane)
            self.message = f"{card.name} entra al campo."
            self.selected = None

    def end_turn(self):
        self.selected = None
        self.player.start_turn()
        self.message = "Nuevo turno."

    def on_click(self, pos):
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
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

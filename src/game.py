import pygame
from src.settings import *
from src.deck import Deck
from src.ui import draw_card, draw_text


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        # Demo temporal: una mano de prueba para ver las cartas
        deck = Deck()
        self.hand = [deck.draw() for _ in range(5)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BG)
        draw_text(self.screen, "Math Wars - demo de cartas", (WIDTH // 2, 60), 32, GOLD, True, True)
        total = len(self.hand) * (CARD_W + 12) - 12
        x = (WIDTH - total) // 2
        for card in self.hand:
            draw_card(self.screen, card, pygame.Rect(x, HEIGHT // 2 - CARD_H // 2, CARD_W, CARD_H))
            x += CARD_W + 12
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

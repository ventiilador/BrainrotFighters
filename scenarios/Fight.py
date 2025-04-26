import pygame
from functions import position, size
from components.Character import Character, Tralalero

class Fight:
    def __init__(self, game):
        self.game = game
        self.status = False
        self.map = None

    def create_display_components(self):
        if self.map:
            self.map = pygame.transform.scale(self.map, size(100, 100))
            self.map_rect = self.map.get_rect()
            self.map_rect.center = position(50, 50)
    
    def create_characters(self, wasd_character_name, ijkl_character_name):
        self.player1 = Tralalero(self, "player1", (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_q, pygame.K_e))
        self.player2 = Tralalero(self, "player2", (pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_u, pygame.K_o))

    def manage_events(self, dt):
        self.player1.manage_events(dt)
        self.player2.manage_events(dt)
    
    def draw(self, screen):
        screen.blit(self.map, self.map_rect)
        self.player1.draw(screen)
        self.player2.draw(screen)
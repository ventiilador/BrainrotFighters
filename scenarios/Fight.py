import pygame
from functions import position, size

class Fight:
    def __init__(self, game):
        self.game = game
        self.status = False
        self.map = None

    def create_display_components(self):
        if self.map:
            self.map = pygame.transform.scale(self.map, size(100, 100))
            self.map_rect = self.map.get_rect()
            self.map_rect.center = position()
    
    def draw(self, screen):
        screen.blit(self)
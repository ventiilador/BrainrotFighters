import pygame
from functions import position, size
from characters.Tralalero import Tralalero
from characters.Bombardiro import Bombardiro
from components.CharacterBar import CharacterBar

class Fight:
    def __init__(self, game):
        # We associate the scene with the game / control
        self.game = game
        self.status = False
        self.map = None

    def create_display_components(self):
        if self.map:
            self.map = pygame.transform.scale(self.map, size(100, 100))
            self.map_rect = self.map.get_rect()
            self.map_rect.center = position(50, 50)
    
    def create_characters(self, player1_name, player2_name):
        pygame.time.wait(1000)
        self.player1 = Bombardiro(self, "player1", (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_q, pygame.K_e, pygame.K_r))
        self.character_bar1 = CharacterBar(self.player1, position(25, 15))
        self.player2 = Tralalero(self, "player2", (pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_u, pygame.K_o, pygame.K_p))
        self.player1.set_enemy(self.player2)
        self.player2.set_enemy(self.player1)
        self.character_bar2 = CharacterBar(self.player2, position(75, 15))

    def manage_events(self, dt):
        self.player1.manage_events(dt)
        self.player2.manage_events(dt)
        self.character_bar1.update(dt)
        self.character_bar2.update(dt)
    
    def draw(self, screen):
        screen.blit(self.map, self.map_rect)
        self.player1.draw(screen)
        self.player2.draw(screen)
        self.character_bar1.draw(screen)
        self.character_bar2.draw(screen)
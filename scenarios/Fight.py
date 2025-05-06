import pygame
import math
from functions import position, size, grayscale_image
from characters.Tralalero import Tralalero
from characters.Bombardiro import Bombardiro
from characters.Tungtung import TungTung
from characters.Patapim import Patapim
from characters.Lirililarila import Lirililarila
from components.CharacterBar import CharacterBar

class Fight:
    def __init__(self, game):
        # We associate the scene with the game / control
        self.game = game
        self.status = False
        self.map = None
        self.time_running = True
        self.player1 = None
        self.player2 = None
        
        # Clock
        self.total_time = 100000
        self.time_elapsed = 0
        self.start_time = pygame.time.get_ticks()
        self.clock_center = position(50, 10)
        self.clock_radius = 40
        self.clock_background = pygame.transform.scale(pygame.image.load("assets/images/fight/extras/clock.png"), size(10, 15))
        self.clock_background_rect = self.clock_background.get_rect(center=self.clock_center)

    def create_display_components(self):
        if self.map:
            self.map = pygame.transform.scale(self.map, size(100, 100))
            self.stopped_map = grayscale_image(self.map)
            self.map_rect = self.map.get_rect()
            self.map_rect.center = position(50, 50)
    
    def create_characters(self, characters=()):
        pygame.time.wait(1000)
        for i in range(len(characters)):
            controls = (pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_u, pygame.K_o, pygame.K_p) if i else (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_q, pygame.K_e, pygame.K_r)
            pos = position(80, 90) if i else position(10, 90)
            if characters[i] == "tralalero":
                setattr(self, f"player{i + 1}", Tralalero(self, controls, pos))
            elif characters[i] == "bombardiro":
                setattr(self, f"player{i + 1}", Bombardiro(self, controls, pos))
            elif characters[i] == "tungtung":
                setattr(self, f"player{i + 1}", TungTung(self, controls, pos))
            elif characters[i] == "patapim":
                setattr(self, f"player{i + 1}", Patapim(self, controls, pos))
            elif characters[i] == "lirililarila":
                setattr(self, f"player{i + 1}", Lirililarila(self, controls, pos))

        self.player1.set_enemy(self.player2)
        self.character_bar1 = CharacterBar(self.player1, position(25, 15))
        self.player2.set_enemy(self.player1)
        self.character_bar2 = CharacterBar(self.player2, position(75, 15))


    def manage_events(self, dt):
        
        if self.time_running:
            self.player1.manage_events(dt)
            self.player2.manage_events(dt)
            self.character_bar1.update(dt)
            self.character_bar2.update(dt)
            self.time_elapsed += dt * 1000
        if not self.time_running and isinstance(self.player1, Lirililarila):
            self.player1.manage_events(dt)
        if not self.time_running and isinstance(self.player2, Lirililarila):
            self.player2.manage_events(dt)
    
    def draw(self, screen):
        map_img = self.map if self.time_running else self.stopped_map
        screen.blit(map_img, self.map_rect)
        self.player1.draw(screen)
        self.player2.draw(screen)
        self.character_bar1.draw(screen)
        self.character_bar2.draw(screen)

        # ------- Update and Draw clock -----------
        angle_deg = (self.time_elapsed / self.total_time) * 360
        angle_rad = math.radians(angle_deg)
        end_x = self.clock_center[0] + self.clock_radius * math.sin(angle_rad)
        end_y = self.clock_center[1] - self.clock_radius * math.cos(angle_rad)
        screen.blit(self.clock_background, self.clock_background_rect)
        pygame.draw.circle(screen, (255, 255, 255), self.clock_center, self.clock_radius, 2)
        pygame.draw.line(screen, (255, 100, 100), self.clock_center, (end_x, end_y), 4)
        pygame.draw.circle(screen, (255, 255, 255), self.clock_center, 5)
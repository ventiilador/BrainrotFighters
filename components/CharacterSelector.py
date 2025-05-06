import pygame
from functions import size as sz

class CharacterSelector:
    def __init__(self, game, position:tuple, size:tuple, rows, columns, controls:tuple):
        # We associate the component with the game
        self.game = game

        """
        Creation of subcomponents
        """
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])
        self.rect.center = position
        self.slot_size = (size[0] // columns, size[1] // rows)
        self.slots = []
        self.characters = [[pygame.transform.scale(pygame.image.load("assets/images/character_selection/bombardiro_crocodilo.jpg"), self.slot_size), "bombardiro"], [pygame.transform.scale(pygame.image.load("assets/images/character_selection/br_patapim.jpg"), self.slot_size), "patapim"],
                    [pygame.transform.scale(pygame.image.load("assets/images/character_selection/tralalero_tralala.jpg"), self.slot_size), "tralalero"], [pygame.transform.scale(pygame.image.load("assets/images/character_selection/tung_sahur.jpeg"), self.slot_size), "tungtung"],
                    [pygame.transform.scale(pygame.image.load("assets/images/character_selection/lirili_larila.jpg"), self.slot_size), "lirililarila"]]
        counter = 0
        for row in range(rows):
            for column in range(columns):
                slot = pygame.rect.Rect(self.rect.left + self.slot_size[0] * column,
                                              self.rect.top + self.slot_size[1] * row, self.slot_size[0], self.slot_size[1])
                self.slots.append([slot, self.characters[counter]]) if counter < len(self.characters) else self.slots.append([slot])
                counter += 1
        
        self.cursor = pygame.transform.scale(pygame.image.load("assets/images/character_selection/cursor.png"), self.slot_size)
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_rect.center = self.slots[0][0].center
        self.cursor_last_time = 0
        self.game.sound_manager.load_sound("Switch", "assets/sounds/Switch.wav")
        self.check_image = pygame.transform.scale(pygame.image.load("assets/images/character_selection/tick.png").convert_alpha(), sz(10, 15))
        self.check_image_rect = self.check_image.get_rect()
        self.check_image_rect.center = (position[0], position[1] + size[1] * 1.5)
        self.character_selected = False
        self.check_last_time = 0
        self.current_x = 0
        self.current_y = 0
        self.controls = controls
    
    def draw(self, screen):
        """
        This function draws the component in the screen
        """
        pygame.draw.rect(screen, (255,180,0), self.rect.inflate(20, 20))
        for slot in self.slots:
            pygame.draw.rect(screen, (255,180,0), slot[0])
            if len(slot) > 1:
                screen.blit(slot[1][0], slot[0])
        screen.blit(self.cursor, self.cursor_rect)
        if self.character_selected:
            screen.blit(self.check_image, self.check_image_rect)
    
    def check_input(self):
        """
        This function manages the component main logic
        """
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if not self.character_selected:
            if keys[self.controls[0]] and self.cursor_rect.center[1] - self.slot_size[1] >= self.rect.top and current_time - self.cursor_last_time > 200:
                self.cursor_rect.y -= self.slot_size[1]
                self.game.sound_manager.play_sound("Switch")
                self.current_y -= 1
                self.cursor_last_time = current_time
            if keys[self.controls[1]] and self.cursor_rect.center[0] - self.slot_size[0] >= self.rect.left and current_time - self.cursor_last_time > 200:
                self.cursor_rect.x -= self.slot_size[0]
                self.game.sound_manager.play_sound("Switch")
                self.current_x -= 1
                self.cursor_last_time = current_time
            if keys[self.controls[2]] and self.cursor_rect.center[1] + self.slot_size[1] <= self.rect.bottom and current_time - self.cursor_last_time > 200:
                self.cursor_rect.y += self.slot_size[1]
                self.game.sound_manager.play_sound("Switch")
                self.current_y += 1
                self.cursor_last_time = current_time
            if keys[self.controls[3]] and self.cursor_rect.center[0] + self.slot_size[0] <= self.rect.right and current_time - self.cursor_last_time > 200:
                self.cursor_rect.x += self.slot_size[0]
                self.game.sound_manager.play_sound("Switch")
                self.current_x += 1
                self.cursor_last_time = current_time
        if keys[self.controls[4]] and current_time - self.check_last_time > 200:
            self.character_selected = False if self.character_selected else True
            self.check_last_time = current_time

    def get_character_name(self):
        """
        This function returns the name of the selected character
        """
        return self.characters[self.current_x][1]
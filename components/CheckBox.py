import pygame
from functions import position, size, get_fullscreen, set_fullscreen, get_showfps, set_showfps

class CheckBox:
    def __init__(self, position, size, game):
        self.game = game
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])
        self.rect.center = position

        self.checkbox_on = pygame.transform.scale(
            pygame.image.load("assets/images/config_menu/checkbox_on.png").convert_alpha(),
            size
        )
        self.checkbox_off = pygame.transform.scale(
            pygame.image.load("assets/images/config_menu/checkbox_off.png").convert_alpha(),
            size
        )

        self.status = False
        self.last_time = 0
    
    def draw(self, screen):
        image = self.checkbox_on if self.status else self.checkbox_off
        screen.blit(image, self.rect)
    
    def check_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0] and (current_time - self.last_time > 300):
            self.status = False if self.status else True
            self.last_time = current_time
            self.change_variable()
        
    def change_variable(self):
        pass


class FullscreenCheckBox(CheckBox):
    def __init__(self, position, size, game):
        super().__init__(position, size, game)
        self.status = get_fullscreen()
    
    def change_variable(self):
        set_fullscreen(self.status)
        self.game.update_display_components()

class ShowFpsCheckBox(CheckBox):
    def __init__(self, position, size, game):
        super().__init__(position, size, game)
        self.status = get_showfps()
    
    def change_variable(self):
        set_showfps(self.status)
        self.game.show_fps = self.status
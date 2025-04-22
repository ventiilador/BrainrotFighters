import pygame
from functions import get_resolution, set_resolution, get_fps, set_fps

class ComboBox:
    def __init__(self, position, size, options, game):
        # We asociate the component with the game
        self.game = game

        # We load the font
        self.font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 24)

        # Status and cooldown and class variables
        self.expanded = False
        self.last_time = 0
        self.current_time = 0

        # Default option (first)
        self.current_option = options[0]

        # We create the main combobox button
        self.current_option_position = position
        self.current_option_rect = pygame.rect.Rect(0, 0, size[0], size[1])
        self.current_option_rect.center = self.current_option_position

        # We update the text of the main button (current option)
        self.update_current_option_text()

        # We create the list of options (dropdown)
        self.options_list = []
        for i in range(len(options)):
            option_text_str = options[i]
            option_text = self.font.render(option_text_str, True, (255, 255, 255))
            option_rect = pygame.rect.Rect(0, 0, size[0], size[1])
            option_rect.center = (
                self.current_option_position[0],
                self.current_option_rect.bottom + size[1] // 2 + size[1] * i
            )
            option_text_rect = option_text.get_rect()
            option_text_rect.center = option_rect.center
            self.options_list.append([option_rect, option_text, option_text_rect, False, option_text_str])
        
    
    def update_current_option_text(self):
        """
        This function updates the text in the main button
        """
        self.current_option_text = self.font.render(self.current_option, True, (255, 255, 255))
        self.current_option_text_rect = self.current_option_text.get_rect()
        self.current_option_text_rect.center = self.current_option_position
        
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.current_option_rect)
        screen.blit(self.current_option_text, self.current_option_text_rect)
        if self.expanded:
            for option in self.options_list:
                background_color = (0, 0, 0) if option[3] else (50, 50, 60)
                pygame.draw.rect(screen, background_color, option[0])
                screen.blit(option[1], option[2])
    
    def check_input(self):
        # We check the mouse position and its buttons pressed / update the cooldown
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        self.current_time = pygame.time.get_ticks()

        # Expand the options
        if self.current_option_rect.collidepoint(mouse_pos) and mouse_buttons[0] and self.current_time - self.last_time > 200:
            self.expanded = False if self.expanded else True
            self.last_time = self.current_time
        
        # Update the current option when another is pressed
        if self.expanded:
            for option in self.options_list:
                if option[0].collidepoint(mouse_pos):
                    option[3] = True
                    if mouse_buttons[0]:
                        self.current_option = option[4]
                        self.update_current_option_text()
                        self.update_variable()
                else:
                    option[3] = False
        
        # Unexpand the options
        if not self.current_option_rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            self.expanded = False
    
    def update_variable(self):
        pass

class ResolutionComboBox(ComboBox):
    def __init__(self, position, size, options, game):
        super().__init__(position, size, options, game)
        resolution = get_resolution()
        self.current_option = f"{resolution[0]}x{resolution[1]}"
        self.update_current_option_text()
    
    def update_variable(self):
        """
        This function updates the resolution in the config file
        """
        if self.current_option == "1280x720":
            set_resolution([1280, 720])
        elif self.current_option == "1920x1080":
            set_resolution([1920, 1080])
        elif self.current_option == "2560x1440":
            set_resolution([2560, 1440])
        elif self.current_option == "3840x2160":
            set_resolution([3840, 2160])
        
        # We reload all the scenes
        self.game.update_display_components()

class FpsComboBox(ComboBox):
    def __init__(self, position, size, options, game):
        super().__init__(position, size, options, game)
        self.current_option = str(get_fps())
        self.update_current_option_text()
    
    def update_variable(self):
        """
        This function updates the FPS's in the config file
        """
        if self.current_option == "30":
            set_fps(30)
        elif self.current_option == "60":
            set_fps(60)
        elif self.current_option == "120":
            set_fps(120)
        elif self.current_option == "144":
            set_fps(144)
        
        # We reload all the scenes
        self.game.fps = get_fps()
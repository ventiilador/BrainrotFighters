import pygame
from functions import get_resolution, set_resolution, get_fps, set_fps

class ComboBox:
    def __init__(self, position, size, options, game):
        # We associate the component with the game
        self.game = game

        # Load the font for the options
        self.font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 24)

        # Initialize the state and cooldown variables
        self.expanded = False  # Whether the combo box is expanded or not
        self.last_time = 0  # Last time the combo box was interacted with
        self.current_time = 0  # Current time for cooldown management

        # Default option (first one in the list)
        self.current_option = options[0]

        # Create the main combo box button (the one displaying the current option)
        self.current_option_position = position
        self.current_option_rect = pygame.rect.Rect(0, 0, size[0], size[1])
        self.current_option_rect.center = self.current_option_position

        # Update the text on the main button (current option)
        self.update_current_option_text()

        # Create the list of options for the dropdown
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
            # Add option to the list (rectangle, text, text rect, is selected, and option string)
            self.options_list.append([option_rect, option_text, option_text_rect, False, option_text_str])
        
    
    def update_current_option_text(self):
        """
        This function updates the text on the main button (current option)
        """
        self.current_option_text = self.font.render(self.current_option, True, (255, 255, 255))
        self.current_option_text_rect = self.current_option_text.get_rect()
        self.current_option_text_rect.center = self.current_option_position
        
    def draw(self, screen):
        # Draw the main combo box button
        pygame.draw.rect(screen, (50, 50, 50), self.current_option_rect)
        screen.blit(self.current_option_text, self.current_option_text_rect)
        
        # If the combo box is expanded, draw the options
        if self.expanded:
            for option in self.options_list:
                # Draw each option with a different background color depending on whether it's selected
                background_color = (0, 0, 0) if option[3] else (50, 50, 60)
                pygame.draw.rect(screen, background_color, option[0])  # Draw option background
                screen.blit(option[1], option[2])  # Draw the option text
    
    def check_input(self):
        # Check if the mouse position is over the combo box and its buttons pressed / update cooldown
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        self.current_time = pygame.time.get_ticks()

        # Expand or collapse the options when the main button is clicked
        if self.current_option_rect.collidepoint(mouse_pos) and mouse_buttons[0] and self.current_time - self.last_time > 200:
            self.expanded = False if self.expanded else True  # Toggle the expansion state
            self.last_time = self.current_time
        
        # Update the current option when an option is clicked
        if self.expanded:
            for option in self.options_list:
                if option[0].collidepoint(mouse_pos):  # Check if the option is hovered over
                    option[3] = True  # Mark this option as selected
                    if mouse_buttons[0]:
                        self.current_option = option[4]  # Update the current option text
                        self.update_current_option_text()
                        self.update_variable()  # Update the variable based on the selection
                else:
                    option[3] = False  # Mark this option as not selected
        
        # Collapse the options if the mouse is clicked outside the combo box
        if not self.current_option_rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            self.expanded = False
    
    def update_variable(self):
        # Placeholder function to update the variable linked with the selected option (to be implemented in subclasses)
        pass

# Child class for managing the resolution combo box
class ResolutionComboBox(ComboBox):
    def __init__(self, position, size, options, game):
        super().__init__(position, size, options, game)  # Call the parent constructor
        resolution = get_resolution()  # Get the current resolution
        self.current_option = f"{resolution[0]}x{resolution[1]}"  # Set the current option as the current resolution
        self.update_current_option_text()  # Update the current option text
    
    def update_variable(self):
        """
        This function updates the resolution based on the selected option
        """
        if self.current_option == "1280x720":
            set_resolution([1280, 720])  # Set resolution to 1280x720
        elif self.current_option == "1920x1080":
            set_resolution([1920, 1080])  # Set resolution to 1920x1080
        elif self.current_option == "2560x1440":
            set_resolution([2560, 1440])  # Set resolution to 2560x1440
        elif self.current_option == "3840x2160":
            set_resolution([3840, 2160])  # Set resolution to 3840x2160
        
        # Reload all scenes after the resolution change
        self.game.update_display_components()

# Child class for managing the FPS combo box
class FpsComboBox(ComboBox):
    def __init__(self, position, size, options, game):
        super().__init__(position, size, options, game)  # Call the parent constructor
        self.current_option = str(get_fps())  # Get the current FPS setting
        self.update_current_option_text()  # Update the current option text
    
    def update_variable(self):
        """
        This function updates the FPS based on the selected option
        """
        if self.current_option == "30":
            set_fps(30)  # Set FPS to 30
        elif self.current_option == "60":
            set_fps(60)  # Set FPS to 60
        elif self.current_option == "120":
            set_fps(120)  # Set FPS to 120
        elif self.current_option == "144":
            set_fps(144)  # Set FPS to 144
        
        # Update the FPS setting in the game
        self.game.fps = get_fps()
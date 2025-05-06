import pygame
from functions import position, size, get_fullscreen, set_fullscreen, get_showfps, set_showfps

class CheckBox:
    def __init__(self, position, size, game):
        # We associate the component with the game
        self.game = game

        """
        We create the subcomponents: the checkbox's rectangle and images for the 'on' and 'off' states
        """
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])  # Create a rectangle for the checkbox
        self.rect.center = position  # Position the checkbox at the provided position

        # Load images for the checkbox in the 'on' and 'off' states
        self.checkbox_on = pygame.transform.scale(
            pygame.image.load("assets/images/config_menu/checkbox_on.png").convert_alpha(),
            size
        )
        self.checkbox_off = pygame.transform.scale(
            pygame.image.load("assets/images/config_menu/checkbox_off.png").convert_alpha(),
            size
        )

        # Initial status of the checkbox (unchecked by default)
        self.status = False
        self.last_time = 0  # For managing click cooldown (prevent double-clicking too fast)
    
    def draw(self, screen):
        """
        This function draws the component on the screen
        """
        # Draw the appropriate checkbox image based on the status (checked or unchecked)
        image = self.checkbox_on if self.status else self.checkbox_off
        screen.blit(image, self.rect)
    
    def check_input(self):
        """
        This function manages the logic of the checkbox's behavior
        """
        mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
        mouse_buttons = pygame.mouse.get_pressed()  # Get the state of mouse buttons
        current_time = pygame.time.get_ticks()  # Get the current time (for click cooldown)
        
        # If the mouse is clicked inside the checkbox and the cooldown period has passed
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0] and (current_time - self.last_time > 300):
            self.status = not self.status  # Toggle the checkbox status
            self.last_time = current_time  # Update the last click time
            self.change_variable()  # Update the variable associated with the checkbox status
    
    def change_variable(self):
        # Placeholder function to be overridden by subclasses
        pass


# Child class for managing the fullscreen checkbox
class FullscreenCheckBox(CheckBox):
    def __init__(self, position, size, game):
        super().__init__(position, size, game)  # Call the parent constructor
        self.status = get_fullscreen()  # Get the current fullscreen status
    
    def change_variable(self):
        """
        This function updates the fullscreen status based on the checkbox status
        """
        set_fullscreen(self.status)  # Set fullscreen mode based on the checkbox status
        self.game.update_display_components()  # Update display components after the change


# Child class for managing the 'show FPS' checkbox
class ShowFpsCheckBox(CheckBox):
    def __init__(self, position, size, game):
        super().__init__(position, size, game)  # Call the parent constructor
        self.status = get_showfps()  # Get the current 'show FPS' status
    
    def change_variable(self):
        """
        This function updates the 'show FPS' setting based on the checkbox status
        """
        set_showfps(self.status)  # Set whether to show FPS or not based on the checkbox status
        self.game.show_fps = self.status  # Update the game's FPS display status
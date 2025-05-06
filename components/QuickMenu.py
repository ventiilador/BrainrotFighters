import pygame
from functions import position, size, render_text_with_border
from components.Button import Button

class QuickMenu:
    def __init__(self):
        # Define the size and rectangle for the quick menu
        self.size = size(40, 50)  # The quick menu size (width, height)
        self.rect = pygame.rect.Rect(0, 0, self.size[0], self.size[1])  # Create a rectangle for the menu
        self.rect.center = position(50, 50)  # Set the position of the rectangle to the center of the screen
        self.status = False  # The initial status of the quick menu (hidden by default)
        
        # Load fonts for the title and buttons
        self.title_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 64)
        self.buttons_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 32)
        
        # Create the title text with a border
        self.title_text = render_text_with_border("Quick Menu", self.title_font, (0, 0, 0), (255, 255, 0))
        self.title_text_rect = self.title_text.get_rect(center=position(50, 35))  # Position the title text at the top center
        
        # Create buttons for the quick menu with specified positions and sizes
        self.resume_button = Button(position(50, 45), size(15, 7), text="Resume", font=self.buttons_font,
                                     background_color=(255, 255, 255), hover_color=(150, 150, 150))
        self.config_button = Button(position(50, 55), size(15, 7), text="Config", font=self.buttons_font,
                                     background_color=(255, 255, 255), hover_color=(150, 150, 150))
        self.exit_button = Button(position(50, 65), size(15, 7), text="Exit", font=self.buttons_font,
                                     background_color=(255, 255, 255), hover_color=(150, 150, 150))

    def draw(self, screen):
        # Draw the quick menu background rectangle (yellow)
        pygame.draw.rect(screen, (255, 180, 0), self.rect)
        
        # Draw the title text on the screen
        screen.blit(self.title_text, self.title_text_rect)
        
        # Draw the buttons on the screen
        self.resume_button.draw(screen)
        self.config_button.draw(screen)
        self.exit_button.draw(screen)
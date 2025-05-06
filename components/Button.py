import pygame

class Button:
    def __init__(self, position:tuple, size:tuple, radius=0, text=None, font=None, image=None, background_color=None, hover_color=None):
        # Style / creation of the component-subcomponents
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])  # Create a rectangle for the button
        self.rect.center = position  # Set the center of the button to the given position
        
        if font:  # If a font is provided, render the button's text
            self.text = font.render(text, True, (0, 0, 0))  # Render the text in black
        self.image = image  # Store the image if provided
        if self.image:  # If an image is provided, get its rect and position it in the center of the button
            self.image_rect = self.image.get_rect()
            self.image_rect.center = position
            
        self.background_color = background_color  # Background color when button is not hovered or clicked
        self.hover_color = hover_color  # Background color when the button is hovered over
        self.radius = radius  # Border radius for rounded corners

        # Status
        self.checked = False  # Initial status of the button (not clicked)
    
    def draw(self, screen):
        """
        This function draws the button on the screen
        """
        if self.image:  # If the button has an image, draw it
            if self.background_color and not self.checked:  # If no hover color and button is not clicked, draw the background color
                pygame.draw.rect(screen, self.background_color, self.rect, border_radius=10)
            elif self.hover_color and self.checked:  # If hover color is set and button is clicked, draw hover color
                pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=10)
            screen.blit(self.image, self.image_rect)  # Draw the image in the button area
        else:  # If there is no image, just draw a rectangle for the button
            background_color = self.hover_color if self.checked else self.background_color  # Set background color based on hover/clicked state
            pygame.draw.rect(screen, background_color, self.rect, border_radius=self.radius)  # Draw the button rectangle with rounded corners
            text_rect = self.text.get_rect(center=self.rect.center)  # Center the text on the button
            screen.blit(self.text, text_rect)  # Draw the text on the button

    def check_input(self):
        """
        This function manages the events of click and hover
        """
        mouse_buttons = pygame.mouse.get_pressed()  # Get the state of the mouse buttons (if any are pressed)
        mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
        
        # Check if the mouse is over the button (collides with the button's rectangle)
        self.checked = self.rect.collidepoint(mouse_pos[0], mouse_pos[1])
        
        # Return True if the button is clicked (mouse button 0 is pressed)
        return self.checked and mouse_buttons[0]
import sys
import pygame
from functions import set_songs_volume, set_sounds_volume, get_songs_volume, get_sounds_volume
from functions import size as size_func

class Drag:
    def __init__(self, position, size, levels_exclusive, max_value):
        # Create the drag component with subcomponents like the rectangle and the pointer
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])  # The main rectangular area of the drag
        self.rect.center = position  # Centering the rectangle at the given position
        self.pointer = pygame.rect.Rect(0, 0, size[0] // 5, size[1] // 5)  # Pointer of the drag (smaller rectangle)
        self.pointer.center = position  # Initial position of the pointer
        self.points = [self.rect.left + size[0] // levels_exclusive * level for level in range(1, levels_exclusive)]  # Points where the pointer can move
        self.points_rects = []  # Store the rectangle points for visual representation
        point_size = size_func(0.3, 4)  # Size of the points (smaller rectangles)
        self.color_step = int(510 / levels_exclusive - 1)  # Step for changing the color
        self.colors = [0, 255, 0]  # Initial color of the drag (green)
        
        # Create the rectangles for the points along the drag bar
        for point in self.points:
            point_rect = pygame.rect.Rect(0, 0, point_size[0], point_size[1])  # Each point's rectangle
            point_rect.center = (point, position[1])  # Position each point along the horizontal axis
            self.points_rects.append(point_rect)  # Add the point rectangle to the list
        
        self.max_value = max_value  # Maximum value that the pointer can represent
        self.levels_exclusive = levels_exclusive  # Number of levels or steps the drag can have
    
    def draw(self, screen):
        """
        This function draws the drag (bar and pointer) on the screen
        """
        pygame.draw.rect(screen, (50, 50, 50), self.rect, border_radius=5)  # Draw the main drag bar (gray)
        
        # Draw the individual points along the drag bar with changing colors
        for point in self.points_rects:
            pygame.draw.rect(screen, tuple(self.colors), point, border_radius=1)
            
            # Update the color from green to red based on the level of the drag
            if self.colors[0] + self.color_step <= 255:
                self.colors[0] += self.color_step  # Increase the red component
            elif self.colors[1] - self.color_step >= 0:
                self.colors[1] -= self.color_step  # Decrease the green component
        
        self.colors = [0, 255, 0]  # Reset color to green after drawing the points
        pygame.draw.rect(screen, (250, 100, 0), self.pointer, border_radius=5)  # Draw the pointer (orange)
    
    def check_input(self):
        """
        This function manages the user input (dragging the pointer)
        """
        mouse_pos = pygame.mouse.get_pos()  # Get the mouse position
        mouse_buttons = pygame.mouse.get_pressed()  # Get mouse button states (whether clicked)
        
        # If the mouse is within the drag bar and the left button is clicked
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            self.pointer.center = (mouse_pos[0], self.pointer.center[1])  # Move the pointer horizontally with the mouse
            distances = [abs(self.pointer.center[0] - point) for point in self.points]  # Calculate distances to each point
            x_desired = distances.index(min(distances))  # Find the closest point to the pointer
            self.pointer.center = (self.points[x_desired], self.pointer.center[1])  # Move pointer to the closest point
            self.update_variable(x_desired)  # Update the value based on the selected point
            return True  # Return True indicating the drag was updated
    
    def update_variable(self, level):
        # Placeholder function to update the variable linked with the drag (to be implemented in subclasses)
        pass

"""
Child classes of the drag for different purposes (Songs and Sounds Volume)
"""
class SongsVolumeDrag(Drag):
    def __init__(self, position, size, levels_exclusive, max_value):
        super().__init__(position, size, levels_exclusive, max_value)  # Call the parent class constructor
        # Set the initial position of the pointer based on the current song volume
        current_level = int(get_songs_volume() / (1 / (self.levels_exclusive - 1)))
        self.pointer.center = (self.points[current_level], position[1])  # Position the pointer based on the volume
    
    def update_variable(self, level):
        # Update the song volume based on the level selected
        set_songs_volume(self.max_value / (self.levels_exclusive - 1) * level)

class SoundsVolumeDrag(Drag):
    def __init__(self, position, size, levels_exclusive, max_value):
        super().__init__(position, size, levels_exclusive, max_value)  # Call the parent class constructor
        # Set the initial position of the pointer based on the current sound volume
        current_level = int(get_sounds_volume() / (1 / (self.levels_exclusive - 1)))
        self.pointer.center = (self.points[current_level], position[1])  # Position the pointer based on the volume
    
    def update_variable(self, level):
        # Update the sound volume based on the level selected
        set_sounds_volume(self.max_value / (self.levels_exclusive - 1) * level)
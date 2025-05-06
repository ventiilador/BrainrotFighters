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
        self.rect.center = position  # Set the position of the component
        self.slot_size = (size[0] // columns, size[1] // rows)  # Calculate size of each character slot
        self.slots = []  # List to store slots for each character
        self.characters = [[pygame.transform.scale(pygame.image.load("assets/images/character_selection/bombardiro_crocodilo.jpg"), self.slot_size), "bombardiro"], 
                           [pygame.transform.scale(pygame.image.load("assets/images/character_selection/br_patapim.jpg"), self.slot_size), "patapim"],
                           [pygame.transform.scale(pygame.image.load("assets/images/character_selection/tralalero_tralala.jpg"), self.slot_size), "tralalero"], 
                           [pygame.transform.scale(pygame.image.load("assets/images/character_selection/tung_sahur.jpeg"), self.slot_size), "tungtung"],
                           [pygame.transform.scale(pygame.image.load("assets/images/character_selection/lirili_larila.jpg"), self.slot_size), "lirililarila"]]  # List of character images and names
        
        counter = 0  # Counter to track the index of the characters list
        for row in range(rows):
            for column in range(columns):
                # Create each slot's rectangle for character selection
                slot = pygame.rect.Rect(self.rect.left + self.slot_size[0] * column,
                                        self.rect.top + self.slot_size[1] * row, self.slot_size[0], self.slot_size[1])
                # If there is a character to display in the slot, add it to the slots list
                self.slots.append([slot, self.characters[counter]]) if counter < len(self.characters) else self.slots.append([slot])
                counter += 1
        
        # Cursor image and rect
        self.cursor = pygame.transform.scale(pygame.image.load("assets/images/character_selection/cursor.png"), self.slot_size)
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_rect.center = self.slots[0][0].center  # Set initial cursor position
        self.cursor_last_time = 0  # Variable to manage the last time the cursor was moved
        self.game.sound_manager.load_sound("Switch", "assets/sounds/Switch.wav")  # Load sound for cursor movement
        self.check_image = pygame.transform.scale(pygame.image.load("assets/images/character_selection/tick.png").convert_alpha(), sz(10, 15))  # Checkmark image for selection
        self.check_image_rect = self.check_image.get_rect()
        self.check_image_rect.center = (position[0], position[1] + size[1] * 1.5)  # Position the checkmark below the grid
        self.character_selected = False  # Flag to track if a character has been selected
        self.check_last_time = 0  # Timer to manage selection cooldown
        self.current_x = 0  # Current selected x position in the grid
        self.current_y = 0  # Current selected y position in the grid
        self.controls = controls  # Define the control keys for navigation (up, left, down, right, select)
    
    def draw(self, screen):
        """
        This function draws the component on the screen
        """
        pygame.draw.rect(screen, (255,180,0), self.rect.inflate(20, 20))  # Draw the background of the character selection box
        for slot in self.slots:
            pygame.draw.rect(screen, (255,180,0), slot[0])  # Draw each slot in the grid
            if len(slot) > 1:
                screen.blit(slot[1][0], slot[0])  # Draw the character image in each slot
        screen.blit(self.cursor, self.cursor_rect)  # Draw the cursor over the selected slot
        if self.character_selected:
            screen.blit(self.check_image, self.check_image_rect)  # Draw the checkmark if a character is selected
    
    def check_input(self):
        """
        This function handles the main logic for the component (e.g., navigation and selection)
        """
        keys = pygame.key.get_pressed()  # Get the keys currently pressed
        current_time = pygame.time.get_ticks()  # Get the current time to manage input cooldowns
        
        if not self.character_selected:
            # Navigate up (if not at the top row)
            if keys[self.controls[0]] and self.cursor_rect.center[1] - self.slot_size[1] >= self.rect.top and current_time - self.cursor_last_time > 200:
                self.cursor_rect.y -= self.slot_size[1]
                self.game.sound_manager.play_sound("Switch")  # Play the sound on cursor movement
                self.current_y -= 1
                self.cursor_last_time = current_time  # Update the last time the cursor was moved
                
            # Navigate left (if not at the leftmost column)
            if keys[self.controls[1]] and self.cursor_rect.center[0] - self.slot_size[0] >= self.rect.left and current_time - self.cursor_last_time > 200:
                self.cursor_rect.x -= self.slot_size[0]
                self.game.sound_manager.play_sound("Switch")  # Play the sound on cursor movement
                self.current_x -= 1
                self.cursor_last_time = current_time  # Update the last time the cursor was moved
                
            # Navigate down (if not at the bottom row)
            if keys[self.controls[2]] and self.cursor_rect.center[1] + self.slot_size[1] <= self.rect.bottom and current_time - self.cursor_last_time > 200:
                self.cursor_rect.y += self.slot_size[1]
                self.game.sound_manager.play_sound("Switch")  # Play the sound on cursor movement
                self.current_y += 1
                self.cursor_last_time = current_time  # Update the last time the cursor was moved
                
            # Navigate right (if not at the rightmost column)
            if keys[self.controls[3]] and self.cursor_rect.center[0] + self.slot_size[0] <= self.rect.right and current_time - self.cursor_last_time > 200:
                self.cursor_rect.x += self.slot_size[0]
                self.game.sound_manager.play_sound("Switch")  # Play the sound on cursor movement
                self.current_x += 1
                self.cursor_last_time = current_time  # Update the last time the cursor was moved
        
        # Select character if the selection button is pressed (defined by controls[4])
        if keys[self.controls[4]] and current_time - self.check_last_time > 200:
            self.character_selected = False if self.character_selected else True  # Toggle the character selection
            self.check_last_time = current_time  # Update the last time the selection was toggled

    def get_character_name(self):
        """
        This function returns the name of the currently selected character
        """
        return self.characters[self.current_x][1]  # Return the name of the selected character based on the current position

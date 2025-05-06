import pygame
import math
from functions import position, size, grayscale_image, render_text_with_border
from characters.Tralalero import Tralalero
from characters.Bombardiro import Bombardiro
from characters.Tungtung import TungTung
from characters.Patapim import Patapim
from characters.Lirililarila import Lirililarila
from components.CharacterBar import CharacterBar
from components.QuickMenu import QuickMenu

class Fight:
    def __init__(self, game):
        # Associate the fight scene with the game and initialize variables
        self.game = game
        self.status = False
        self.map = None
        self.time_running = True
        self.player1 = None
        self.player2 = None
        self.character_names = None
        self.winner = None
        self.winner_message_time = 5  # Time to display winner message
        self.winner_message_time_elapsed = 0
        self.winner_message_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 90)
        self.game.sound_manager.load_sound("Winner", "assets/sounds/MapWinner.mp3")
        self.winner_sound_played = False

        # Quick menu state tracking
        self.last_quick_menu_time = 0
        
        # Clock and timer initialization
        self.total_time = 100000
        self.time_elapsed = 0
        self.start_time = pygame.time.get_ticks()

    def create_display_components(self):
        """
        Creates and initializes the visual components for the fight scene
        """
        if self.map:
            # Load and scale the map, also create grayscale version for when time stops
            self.map = pygame.transform.scale(self.map, size(100, 100))
            self.stopped_map = grayscale_image(self.map)
            self.map_rect = self.map.get_rect()
            self.map_rect.center = position(50, 50)

            # Set up clock visuals
            self.clock_center = position(50, 10)
            self.clock_radius = 40
            self.clock_background = pygame.transform.scale(pygame.image.load("assets/images/fight/extras/clock.png"), size(10, 15))
            self.clock_background_rect = self.clock_background.get_rect(center=self.clock_center)

        if self.character_names:
            # Initialize players based on the character names provided
            for i in range(len(self.character_names)):
                # Define control keys for each player
                controls = (pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_u, pygame.K_o, pygame.K_p) if i else (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_q, pygame.K_e, pygame.K_r)
                pos = position(60, 90) if i else position(30, 90)
                
                # Assign player character based on name
                if self.character_names[i] == "tralalero":
                    setattr(self, f"player{i + 1}", Tralalero(self, controls, pos))
                elif self.character_names[i] == "bombardiro":
                    setattr(self, f"player{i + 1}", Bombardiro(self, controls, pos))
                elif self.character_names[i] == "tungtung":
                    setattr(self, f"player{i + 1}", TungTung(self, controls, pos))
                elif self.character_names[i] == "patapim":
                    setattr(self, f"player{i + 1}", Patapim(self, controls, pos))
                elif self.character_names[i] == "lirililarila":
                    setattr(self, f"player{i + 1}", Lirililarila(self, controls, pos))

            # Set enemy relationships for players
            self.player1.set_enemy(self.player2)
            self.character_bar1 = CharacterBar(self.player1, position(25, 15))
            self.player2.set_enemy(self.player1)
            self.character_bar2 = CharacterBar(self.player2, position(75, 15))

        self.quick_menu = QuickMenu()  # Initialize quick menu
    
    def quit(self):
        """
        Exit the fight and return to the main menu
        """
        self.game.main_menu.status = True
        self.status = False
        self.quick_menu.status = False
        self.game.game_started = False
        self.game.load_game()
    
    def set_character_names(self, characters=()):
        """
        Set the names of the characters involved in the fight
        """
        self.character_names = characters
        pygame.time.wait(1000)  # Add a brief pause after setting character names
        

    def manage_events(self, dt):
        """
        Manage events during the fight, such as player actions, quick menu, and winner determination
        """
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Handle quick menu toggle when the ESC key is pressed
        if keys[pygame.K_ESCAPE] and current_time - self.last_quick_menu_time >= 200:
            self.quick_menu.status = not self.quick_menu.status  # Toggle quick menu visibility
            self.last_quick_menu_time = current_time

        if self.quick_menu.status:
            # Handle quick menu button inputs
            if self.quick_menu.resume_button.check_input():
                self.quick_menu.status = False
            
            if self.quick_menu.config_button.check_input():
                self.game.config_menu.status = True
                self.status = False

            if self.quick_menu.exit_button.check_input():
                self.quit()
            return
        
        # Check if the total fight time has elapsed and determine the winner
        if self.time_elapsed >= self.total_time:
            if self.player1.health > self.player2.health:
                self.winner = "player1"
            elif self.player1.health < self.player2.health:
                self.winner = "player2"
            else:
                self.winner = "draw"
        
        # Check if either player has lost all health
        if self.player1.health <= 0 and self.player2.health >= 1:
            self.winner = "player2"
        elif self.player2.health <= 0 and self.player1.health >= 1:
            self.winner = "player1"
        elif self.player1.health <= 0 and self.player2.health <= 0:
            self.winner = "draw"
        
        if self.winner:
            # Play winner sound if not already played and stop the fight timer
            if not self.winner_sound_played:
                self.game.sound_manager.play_sound("Winner")
                self.winner_sound_played = True
            self.time_running = False
            self.show_winner_message = True
            self.winner_message_time_elapsed += dt
        
        if self.winner_message_time_elapsed >= self.winner_message_time:
            self.quit()  # Quit the fight after the winner message duration
        
        if self.time_running:
            # Allow players to manage events if the fight is ongoing
            self.player1.manage_events(dt)
            self.player2.manage_events(dt)
            self.character_bar1.update(dt)
            self.character_bar2.update(dt)
            self.time_elapsed += dt * 1000  # Update elapsed time
        
        # Allow Lirililarila to manage events even when time is not running
        if not self.time_running and isinstance(self.player1, Lirililarila):
            self.player1.manage_events(dt)
        if not self.time_running and isinstance(self.player2, Lirililarila):
            self.player2.manage_events(dt)
    
    def draw(self, screen):
        """
        Draw all components of the fight scene to the screen
        """
        # Choose map based on whether the time is running or stopped
        map_img = self.map if self.time_running else self.stopped_map
        screen.blit(map_img, self.map_rect)
        self.player1.draw(screen)
        self.player2.draw(screen)
        self.character_bar1.draw(screen)
        self.character_bar2.draw(screen)

        # Update and draw the clock showing the remaining time
        angle_deg = (self.time_elapsed / self.total_time) * 360
        angle_rad = math.radians(angle_deg)
        end_x = self.clock_center[0] + self.clock_radius * math.sin(angle_rad)
        end_y = self.clock_center[1] - self.clock_radius * math.cos(angle_rad)
        screen.blit(self.clock_background, self.clock_background_rect)
        pygame.draw.circle(screen, (255, 255, 255), self.clock_center, self.clock_radius, 2)
        pygame.draw.line(screen, (255, 100, 100), self.clock_center, (end_x, end_y), 4)
        pygame.draw.circle(screen, (255, 255, 255), self.clock_center, 5)

        # Draw the quick menu if it's visible
        if self.quick_menu.status:
            self.quick_menu.draw(screen)

        # Display the winner message if a winner has been determined
        if self.winner and self.winner_message_time_elapsed <= self.winner_message_time:
            if self.winner == "draw":
                message_text = render_text_with_border("Draw", self.winner_message_font, (255, 180, 0), (0, 0, 0))
            else:
                message_text = render_text_with_border(f"{self.winner} won!", self.winner_message_font, (255, 180, 0), (0, 0, 0))
            message_rect = message_text.get_rect(center=position(50, 50))
            screen.blit(message_text, message_rect)
import pygame
from functions import position, size, get_resolution
from components.CharacterSelector import CharacterSelector

class CharacterSelection:
    def __init__(self, game):
        # We associate the scene with the game / control
        self.game = game
        self.status = False  # The initial status of the scene is set to False
        self.music_played = False  # Flag to check if music has been played

        # Music: Load and prepare the background song for the selection screen
        self.game.sound_manager.load_song("GameSong", "assets/sounds/GameSong.mp3")

        self.create_display_components()  # Call function to create all the UI components
    
    def create_display_components(self):
        """
        This function creates all the components in the Character Selection screen
        """
        # Load and scale the background image to fit the screen resolution
        background_image = pygame.image.load("assets/images/character_selection/character_selection_background.png").convert()
        self.background_image = pygame.transform.scale(background_image, tuple(get_resolution()))

        # Title font and text rendering
        title_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 64)
        self.title = title_font.render("Brainrot Fighters Character Selection", True, (0, 0, 0))
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (position(50, 10))  # Position the title at the top-center

        # Players' titles (Player 1 and Player 2)
        players_font = pygame.font.SysFont("Arial", 46, bold=True)
        self.player1_title = players_font.render("Player 1 (WASD)", True, (0, 0, 0))
        self.player1_title_rect = self.player1_title.get_rect()
        self.player1_title_rect.center = position(25, 25)

        # Player 1 select text ('E' to select)
        player_select_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 36)
        self.player1_select_text = player_select_font.render("'E' to select", True, (0, 0, 0))
        self.player1_select_text_rect = self.player1_select_text.get_rect()
        self.player1_select_text_rect.center = position(25, 35)

        # Player 2 title (Player 2 and the respective keys)
        self.player2_title = players_font.render("Player 2 (IJKL)", True, (0, 0, 0))
        self.player2_title_rect = self.player2_title.get_rect()
        self.player2_title_rect.center = position(75, 25)

        # Player 2 select text ('O' to select)
        self.player2_select_text = player_select_font.render("'O' to select", True, (0, 0, 0))
        self.player2_select_text_rect = self.player2_select_text.get_rect()
        self.player2_select_text_rect.center = position(75, 35)

        # Character selectors for Player 1 and Player 2
        self.character_selector_1 = CharacterSelector(self.game, position(25, 50), size(38, 15), 1, 5, (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_e))
        self.character_selector_2 = CharacterSelector(self.game, position(75, 50), size(38, 15), 1, 5, (pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_o))

    def draw(self, screen):
        """
        This function draws all the components on the screen
        """
        # Draw the background image
        screen.blit(self.background_image, (0, 0))

        # Draw the title with background rectangle
        pygame.draw.rect(screen, (255, 180, 0), self.title_rect.inflate(50, 30))
        screen.blit(self.title, self.title_rect)

        # Draw the player 1 title and its background rectangle
        pygame.draw.rect(screen, (255, 180, 0), self.player1_title_rect.inflate(20, 15))
        screen.blit(self.player1_title, self.player1_title_rect)

        # Draw the "select" text for player 1
        pygame.draw.rect(screen, (255, 180, 0), self.player1_select_text_rect.inflate(20, 15))
        screen.blit(self.player1_select_text, self.player1_select_text_rect)

        # Draw the player 2 title and its background rectangle
        pygame.draw.rect(screen, (255, 180, 0), self.player2_title_rect.inflate(20, 15))
        screen.blit(self.player2_title, self.player2_title_rect)

        # Draw the "select" text for player 2
        pygame.draw.rect(screen, (255, 180, 0), self.player2_select_text_rect.inflate(20, 15))
        screen.blit(self.player2_select_text, self.player2_select_text_rect)

        # Draw the character selectors for both players
        self.character_selector_1.draw(screen)
        self.character_selector_2.draw(screen)

    def manage_events(self):
        """
        This function manages all the events in the Character Selection screen
        """
        # Play background music if not already played
        if not self.music_played:
            self.game.sound_manager.play_song("GameSong", -1)  # Loop the song indefinitely
            self.music_played = True  # Set flag to True once the music is played
        
        # If both players have selected their characters, move to the fight scene
        if self.character_selector_1.character_selected and self.character_selector_2.character_selected:
            self.game.fight.set_character_names((self.character_selector_1.get_character_name(), self.character_selector_2.get_character_name()))
            self.game.fight.create_display_components()  # Create the components for the fight screen
            self.status = False  # Hide the character selection screen
            self.game.fight.status = True  # Show the fight scene
        
        # Check for input from both character selectors
        self.character_selector_1.check_input()
        self.character_selector_2.check_input()
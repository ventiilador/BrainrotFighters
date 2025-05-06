import pygame
from functions import position, size, get_resolution
from components.Button import Button

class MainMenu:
    def __init__(self, game):
        # We associate the scene with the game controller
        self.game = game
        self.status = True

        # Start playing the main menu background music in a loop
        self.game.sound_manager.load_song("MainMenuSong", "assets/sounds/MainMenuSong.mp3")
        self.game.sound_manager.play_song("MainMenuSong", -1)

        self.create_display_components()
    
    def create_display_components(self):
        """
        This function creates all the visual components in the main menu
        """
        # Load and scale the background and title images
        self.background_image = pygame.transform.scale(
            pygame.image.load("assets/images/main_menu/main_menu_background.png").convert(),
            tuple(get_resolution())
        )
        self.title_image = pygame.transform.scale(
            pygame.image.load("assets/images/main_menu/main_menu_title.png"),
            size(40, 35)
        )
        self.title_rect = self.title_image.get_rect()
        self.title_rect.center = position(50, 20)

        # Define the font and create buttons
        buttons_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 50)
        self.play_button = Button(
            position(50, 45),
            size(25, 15),
            0,
            text="Play",
            font=buttons_font,
            background_color=(255, 180, 0),
            hover_color=(255, 255, 0)
        )
        self.config_button = Button(
            position(50, 65),
            size(25, 15),
            0,
            text="Config",
            font=buttons_font,
            background_color=(255, 180, 0),
            hover_color=(255, 255, 0)
        )

    def draw(self, screen):
        """
        This function draws all the components to the screen
        """
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.title_image, self.title_rect)
        self.play_button.draw(screen)
        self.config_button.draw(screen)

    def manage_events(self):
        """
        This function manages all interactions/events in the main menu
        """
        # If Play is clicked, stop the music and switch to map randomizer
        if self.play_button.check_input():
            self.game.sound_manager.stop_song("MainMenuSong")
            self.status = False
            self.game.map_randomizer.status = True
            self.game.game_started = True

        # If Config is clicked, go to config menu
        if self.config_button.check_input():
            self.status = False
            self.game.config_menu.status = True
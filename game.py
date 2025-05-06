import pygame
from functions import get_resolution, get_fps, get_fullscreen, get_showfps, render_text_with_border
from scenarios.MainMenu import MainMenu
from scenarios.ConfigMenu import ConfigMenu
from scenarios.CharacterSelection import CharacterSelection
from scenarios.MapRandomizer import MapRandomizer
from scenarios.Fight import Fight
from SoundManager import SoundManager


class Game:
    def __init__(self):
        # Initialize Pygame and create the game window
        pygame.init()
        pygame.display.set_caption("Brainrot Fighters")
        if get_fullscreen():
            self.screen = pygame.display.set_mode(tuple(get_resolution()), pygame.SCALED + pygame.NOFRAME + pygame.FULLSCREEN, 32)
        else:
            self.screen = pygame.display.set_mode(tuple(get_resolution()), pygame.SCALED, 32)
        
        print("🟡 Game Window Created Successfully!")

        # Load the sound manager
        self.sound_manager = SoundManager()
        print("🔊 Sound Manager Loaded Successfully!")

        self.load_game()
        self.game_started = False

        # Initialize frame rate and game loop control variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = get_fps()
        self.show_fps = get_showfps()
        self.fps_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 24)
        self.last_update_display_time = 0

    def load_game(self):
        self.sound_manager.stop_all()
        # Load all the game scenes
        self.main_menu = MainMenu(self)
        print("📋 Main Menu Loaded Successfully!")
        self.config_menu = ConfigMenu(self)
        print("⚙️  Config Menu Loaded Successfully!")
        self.map_randomizer = MapRandomizer(self)
        print("🗺️  Map Randomizer Loaded Successfully!")
        self.character_selection = CharacterSelection(self)
        print("🕴️  Character Selection Loaded Successfully!")
        self.fight = Fight(self)
        print("👾  Fight Loaded Successfully!")
    
    def update_display_components(self):
        """
        This function rescales the components in the screen
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_display_time > 300:
            # Reinitialize the display with the updated resolution or fullscreen settings
            pygame.display.quit()
            pygame.display.init()
            if get_fullscreen():
                self.screen = pygame.display.set_mode(tuple(get_resolution()), pygame.SCALED + pygame.NOFRAME + pygame.FULLSCREEN, 32)
            else:
                self.screen = pygame.display.set_mode(tuple(get_resolution()), pygame.SCALED, 32)
            
            # Recreate display components for all scenes
            self.main_menu.create_display_components()
            self.config_menu.create_display_components()
            self.map_randomizer.create_display_components()
            self.character_selection.create_display_components()
            self.fight.create_display_components()
            self.last_update_display_time = current_time
            print("🔁 Display Components Reloaded Successfully!")
    

    def run(self):
        """
        Main Bucle
        """
        print("▶️  Main Bucle Started!")
        last_time = pygame.time.get_ticks()
        while self.running:
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 1000
            last_time = current_time

            # Handle window events (e.g., closing the window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("❌ Quiting The Game...")
                    self.running = False
            
            # Determine which scene is currently active and update it
            if self.main_menu.status:
                self.main_menu.manage_events()
                self.main_menu.draw(self.screen)
            
            elif self.config_menu.status:
                self.config_menu.manage_events()
                self.config_menu.draw(self.screen)
            
            elif self.map_randomizer.status:
                self.map_randomizer.manage_events()
                self.map_randomizer.move(delta_time)
                self.map_randomizer.draw(self.screen)
            
            elif self.character_selection.status:
                self.character_selection.manage_events()
                self.character_selection.draw(self.screen)
            
            elif self.fight.status:
                self.fight.manage_events(delta_time)
                if self.fight.status:
                    self.fight.draw(self.screen)

            else:
                # If no scene is active, fill the screen with white
                self.screen.fill((255,255,255))
            
            # If FPS display is enabled, render and display it
            if self.show_fps:
                fps = int(self.clock.get_fps())
                fps_text = render_text_with_border(f"FPS: {fps}", self.fps_font, (255, 215, 0), (0, 0, 0))
                self.screen.blit(fps_text, (10, 10))
                
            # Update the full display surface to the screen
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Game()
    game.run()

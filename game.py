import pygame
from functions import get_resolution, get_fps, get_fullscreen, get_showfps
from scenarios.MainMenu import MainMenu
from scenarios.ConfigMenu import ConfigMenu
from scenarios.CharacterSelection import CharacterSelection
from scenarios.MapRandomizer import MapRandomizer
from SoundManager import SoundManager


class Game:
    def __init__(self):
        # Pygame start / Window creation
        pygame.init()
        pygame.display.set_caption("Brainrot Fighters")
        self.screen = pygame.display.set_mode(tuple(get_resolution()), pygame.FULLSCREEN) if get_fullscreen() else pygame.display.set_mode(tuple(get_resolution()))
        print("🟡 Game Window Created Successfully!")

        # Creation of sound manager
        self.sound_manager = SoundManager()
        print("🔊 Sound Manager Loaded Successfully!")

        # Creation of the scenes
        self.main_menu = MainMenu(self)
        print("📋 Main Menu Loaded Successfully!")
        self.config_menu = ConfigMenu(self)
        print("⚙️  Config Menu Loaded Successfully!")
        self.map_randomizer = MapRandomizer(self)
        print("🗺️  Map Randomizer Loaded Successfully!")
        self.character_selection = CharacterSelection(self)
        print("🕴️  Character Selection Loaded Successfully!")

        # Fps / bucle Conditionals
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = get_fps()
        self.show_fps = get_showfps()
        self.fps_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 24)
        self.last_update_display_time = 0
    
    def update_display_components(self):
        """
        This function rescales the components in the screen
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_display_time > 300:
            pygame.display.quit()
            pygame.display.init()
            if get_fullscreen():
                self.screen = pygame.display.set_mode(tuple(get_resolution()), pygame.SCALED + pygame.NOFRAME + pygame.FULLSCREEN, 32)
            else:
                self.screen = pygame.display.set_mode(tuple(get_resolution()), pygame.SCALED + pygame.RESIZABLE, 32)
            
            self.main_menu.create_display_components()
            self.config_menu.create_display_components()
            self.map_randomizer.create_display_components()
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("❌ Quiting The Game...")
                    self.running = False
            
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

            else:
                self.screen.fill((255,255,255))
            
            if self.show_fps:
                fps = int(self.clock.get_fps())
                fps_text = self.fps_font.render(f"FPS: {fps}", True, (255, 215, 0))
                border_text = self.fps_font.render(f"FPS: {fps}", True, (0, 0, 0))

                self.screen.blit(border_text, (12, 12))
                self.screen.blit(border_text, (8, 12))
                self.screen.blit(border_text, (12, 8))
                self.screen.blit(border_text, (8, 8))

                self.screen.blit(fps_text, (10, 10))

            pygame.display.flip()

            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Game()
    game.run()
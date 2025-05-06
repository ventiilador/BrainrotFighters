import pygame
from functions import position, size, get_songs_volume, get_resolution
from components.Button import Button
from components.Drag import SongsVolumeDrag, SoundsVolumeDrag
from components.ComboBox import ComboBox, ResolutionComboBox, FpsComboBox
from components.CheckBox import CheckBox, FullscreenCheckBox, ShowFpsCheckBox

class ConfigMenu:
    def __init__(self, game):
        # We associate the scene with the game / control
        self.game = game
        self.status = False  # The initial status of the menu is set to False

        self.create_display_components()  # Call function to create UI components
    
    def create_display_components(self):
        """
        This function creates all the components in the config menu
        """
        print(get_resolution())  # Print the current screen resolution
        background_image = pygame.image.load("assets/images/main_menu/main_menu_background.png").convert()
        # Load and convert the background image for the menu
        self.background_image = pygame.transform.scale(background_image, tuple(get_resolution()))
        # Resize the background to match the screen resolution
        backplate_size = size(80, 98)
        self.back_plate = pygame.Surface((backplate_size[0], backplate_size[1]), pygame.SRCALPHA)
        self.back_plate.fill((229, 135, 0))  # Set the background color of the settings panel
        self.back_plate.set_alpha(240)  # Set the transparency of the settings panel
        self.back_plate_rect = self.back_plate.get_rect()
        self.back_plate_rect.center = position(50, 50)  # Position the settings panel at the center
        title_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 72)
        self.title = title_font.render("Brainrot Fighters Config", True, (0, 0, 0))
        # Set up the title font and text
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (position(50, 10))  # Position the title at the top-center
        subtitles_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 36)
        
        # Create volume control components for Songs
        self.songs_volume_title = subtitles_font.render("Songs Volume", True, (0, 0, 0))
        self.songs_volume_title_rect = self.songs_volume_title.get_rect()
        self.songs_volume_title_rect.center = (position(50, 25))
        self.songs_volume_drag = SongsVolumeDrag(position(50, 35), size(10, 5), 9, 1.0)

        # Create volume control components for Sounds
        self.sounds_volume_title = subtitles_font.render("Sounds Volume", True, (0, 0, 0))
        self.sounds_volume_title_rect = self.sounds_volume_title.get_rect()
        self.sounds_volume_title_rect.center = (position(50, 45))
        self.sounds_volume_drag = SoundsVolumeDrag(position(50, 55), size(10, 5), 9, 1.0)

        # Create resolution settings dropdown
        self.resolution_title = subtitles_font.render("Resolution", True, (0, 0, 0))
        self.resolution_title_rect = self.resolution_title.get_rect()
        self.resolution_title_rect.center = position(25, 65)
        self.resolution_box = ResolutionComboBox(position(25, 75), size(10, 5), ["1280x720", "1920x1080", "2560x1440", "3840x2160"], self.game)

        # Create FPS settings dropdown
        self.fps_title = subtitles_font.render("Fps", True, (0, 0, 0))
        self.fps_title_rect = self.fps_title.get_rect()
        self.fps_title_rect.center = position(50, 65)
        self.fps_box = FpsComboBox(position(50, 75), size(10, 5), ["30", "60", "120", "144"], self.game)

        # Create section for other settings like fullscreen and show FPS
        self.others_title = subtitles_font.render("Others", True, (0, 0, 0))
        self.others_title_rect = self.others_title.get_rect()
        self.others_title_rect.center = position(75, 65)
        suboption_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 24)
        self.fullscreen_subtitle = suboption_font.render("Fullscreen:", True, (255, 255, 255))
        self.fullscreen_subtitle_rect = self.fullscreen_subtitle.get_rect()
        self.fullscreen_subtitle_rect.center = position(74, 75)
        self.fullscreen_checkbox = FullscreenCheckBox(position(82, 75), size(4, 7), self.game)
        self.showfps_subtitle = suboption_font.render("Show FPS:", True, (255, 255, 255))
        self.showfps_subtitle_rect = self.showfps_subtitle.get_rect()
        self.showfps_subtitle_rect.center = position(74, 85)
        self.showfps_checkbox = ShowFpsCheckBox(position(82, 85), size(4, 7), self.game)

        # Create a button to return to the previous menu
        image = pygame.transform.scale(pygame.image.load("assets/images/config_menu/return_button.png").convert_alpha(), size(5, 8))
        self.return_button = Button(position(15, 90), size(7, 10), image=image, background_color=(255,255,0), hover_color=(255,220,0))

    def draw(self, screen):
        """
        This function draws all the components in the screen
        """
        screen.blit(self.background_image, (0, 0))  # Draw the background
        screen.blit(self.back_plate, self.back_plate_rect.topleft)  # Draw the settings panel
        pygame.draw.rect(screen, (255, 255, 0), self.title_rect.inflate(50, 30))  # Draw a yellow background behind the title
        screen.blit(self.title, self.title_rect)  # Draw the title text
        pygame.draw.rect(screen, (255, 255, 0), self.songs_volume_title_rect.inflate(25, 15))  # Draw background for songs volume label
        screen.blit(self.songs_volume_title, self.songs_volume_title_rect)  # Draw the songs volume label
        self.songs_volume_drag.draw(screen)  # Draw the songs volume drag element
        pygame.draw.rect(screen, (255, 255, 0), self.sounds_volume_title_rect.inflate(25, 15))  # Draw background for sounds volume label
        screen.blit(self.sounds_volume_title, self.sounds_volume_title_rect)  # Draw the sounds volume label
        self.sounds_volume_drag.draw(screen)  # Draw the sounds volume drag element
        pygame.draw.rect(screen, (255, 255, 0), self.resolution_title_rect.inflate(25, 15))  # Draw background for resolution label
        screen.blit(self.resolution_title, self.resolution_title_rect)  # Draw the resolution label
        self.resolution_box.draw(screen)  # Draw the resolution dropdown
        pygame.draw.rect(screen, (255, 255, 0), self.fps_title_rect.inflate(25, 15))  # Draw background for fps label
        screen.blit(self.fps_title, self.fps_title_rect)  # Draw the fps label
        self.fps_box.draw(screen)  # Draw the fps dropdown
        pygame.draw.rect(screen, (255, 255, 0), self.others_title_rect.inflate(25, 15))  # Draw background for "Others" label
        screen.blit(self.others_title, self.others_title_rect)  # Draw the "Others" label
        screen.blit(self.fullscreen_subtitle, self.fullscreen_subtitle_rect)  # Draw the fullscreen subtitle
        self.fullscreen_checkbox.draw(screen)  # Draw the fullscreen checkbox
        screen.blit(self.showfps_subtitle, self.showfps_subtitle_rect)  # Draw the show FPS subtitle
        self.showfps_checkbox.draw(screen)  # Draw the show FPS checkbox
        self.return_button.draw(screen)  # Draw the return button

    def manage_events(self):
        """
        This function manages all the events in the config menu
        """
        # Check if the volume sliders have been interacted with
        if self.songs_volume_drag.check_input() or self.sounds_volume_drag.check_input():
            self.game.sound_manager.update_volumes()
        
        # Check if the combo boxes (resolution, FPS) have been interacted with
        self.resolution_box.check_input()
        self.fps_box.check_input()

        # Check if the checkboxes (fullscreen, show FPS) have been toggled
        self.fullscreen_checkbox.check_input()
        self.showfps_checkbox.check_input()

        # Check if the return button has been pressed
        if self.return_button.check_input():
            self.status = False  # Close the config menu
            if self.game.game_started:
                self.game.fight.status = True  # If the game has started, go to the fight scene
            else:
                self.game.main_menu.status = True  # Otherwise, go back to the main menu
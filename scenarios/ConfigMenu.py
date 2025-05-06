import pygame
from functions import position, size, get_songs_volume, get_resolution
from components.Button import Button
from components.Drag import SongsVolumeDrag, SoundsVolumeDrag
from components.ComboBox import ComboBox, ResolutionComboBox, FpsComboBox
from components.CheckBox import CheckBox, FullscreenCheckBox, ShowFpsCheckBox

class ConfigMenu:
    def __init__(self, game):
        # We associate the scene with de game / control
        self.game = game
        self.status = False

        self.create_display_components()
    
    def create_display_components(self):
        """
        This function creates all the components in the config menu
        """
        print(get_resolution())
        background_image = pygame.image.load("assets/images/main_menu/main_menu_background.png").convert()
        self.background_image = pygame.transform.scale(background_image, tuple(get_resolution()))
        backplate_size = size(80, 98)
        self.back_plate = pygame.Surface((backplate_size[0], backplate_size[1]), pygame.SRCALPHA)
        self.back_plate.fill((229, 135, 0))
        self.back_plate.set_alpha(240)
        self.back_plate_rect = self.back_plate.get_rect()
        self.back_plate_rect.center = position(50, 50)
        title_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 72)
        self.title = title_font.render("Brainrot Fighters Config", True, (0, 0, 0))
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (position(50, 10))
        subtitles_font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 36)
        self.songs_volume_title = subtitles_font.render("Songs Volume", True, (0, 0, 0))
        self.songs_volume_title_rect = self.songs_volume_title.get_rect()
        self.songs_volume_title_rect.center = (position(50, 25))
        self.songs_volume_drag = SongsVolumeDrag(position(50, 35), size(10, 5), 9, 1.0)
        self.sounds_volume_title = subtitles_font.render("Sounds Volume", True, (0, 0, 0))
        self.sounds_volume_title_rect = self.sounds_volume_title.get_rect()
        self.sounds_volume_title_rect.center = (position(50, 45))
        self.sounds_volume_drag = SoundsVolumeDrag(position(50, 55), size(10, 5), 9, 1.0)
        self.resolution_title = subtitles_font.render("Resolution", True, (0, 0, 0))
        self.resolution_title_rect = self.resolution_title.get_rect()
        self.resolution_title_rect.center = position(25, 65)
        self.resolution_box = ResolutionComboBox(position(25, 75), size(10, 5), ["1280x720", "1920x1080", "2560x1440", "3840x2160"], self.game)
        self.fps_title = subtitles_font.render("Fps", True, (0, 0, 0))
        self.fps_title_rect = self.fps_title.get_rect()
        self.fps_title_rect.center = position(50, 65)
        self.fps_box = FpsComboBox(position(50, 75), size(10, 5), ["30", "60", "120", "144"], self.game)
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
        image = pygame.transform.scale(pygame.image.load("assets/images/config_menu/return_button.png").convert_alpha(), size(5, 8))
        self.return_button = Button(position(15, 90), size(7, 10), image=image, background_color=(255,255,0), hover_color=(255,220,0))


    def draw(self, screen):
        """
        This function draws all the components in the screen
        """
        screen.blit(self.background_image, (0,0))
        screen.blit(self.back_plate, self.back_plate_rect.topleft)
        pygame.draw.rect(screen, (255, 255, 0), self.title_rect.inflate(50, 30))
        screen.blit(self.title, self.title_rect)
        pygame.draw.rect(screen, (255, 255, 0), self.songs_volume_title_rect.inflate(25, 15))
        screen.blit(self.songs_volume_title, self.songs_volume_title_rect)
        self.songs_volume_drag.draw(screen)
        pygame.draw.rect(screen, (255, 255, 0), self.sounds_volume_title_rect.inflate(25, 15))
        screen.blit(self.sounds_volume_title, self.sounds_volume_title_rect)
        self.sounds_volume_drag.draw(screen)
        pygame.draw.rect(screen, (255, 255, 0), self.resolution_title_rect.inflate(25, 15))
        screen.blit(self.resolution_title, self.resolution_title_rect)
        self.resolution_box.draw(screen)
        pygame.draw.rect(screen, (255, 255, 0), self.fps_title_rect.inflate(25, 15))
        screen.blit(self.fps_title, self.fps_title_rect)
        self.fps_box.draw(screen)
        pygame.draw.rect(screen, (255, 255, 0), self.others_title_rect.inflate(25, 15))
        screen.blit(self.others_title, self.others_title_rect)
        screen.blit(self.fullscreen_subtitle, self.fullscreen_subtitle_rect)
        self.fullscreen_checkbox.draw(screen)
        screen.blit(self.showfps_subtitle, self.showfps_subtitle_rect)
        self.showfps_checkbox.draw(screen)
        self.return_button.draw(screen)


    def manage_events(self):
        """
        This function manages all the events in the config menu
        """
        if self.songs_volume_drag.check_input() or self.sounds_volume_drag.check_input():
            self.game.sound_manager.update_volumes()
        self.resolution_box.check_input()
        self.fps_box.check_input()
        self.fullscreen_checkbox.check_input()
        self.showfps_checkbox.check_input()
        if self.return_button.check_input():
            self.status = False
            if self.game.game_started:
                self.game.fight.status = True
            else:
                self.game.main_menu.status = True
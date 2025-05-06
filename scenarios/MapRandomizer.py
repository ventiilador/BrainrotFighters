import pygame
from functions import position, size, position_x, position_y, size_x, size_y
from random import randint

class MapRandomizer:
    def __init__(self, game):
        # We associate the game
        self.game = game

        # Control variables
        self.status = False
        self.velocity = randint(3000, 5000)
        self.winner_map = None
        self.show_message = False
        self.message_started = False
        self.result_checked = False

        # We load sounds
        self.game.sound_manager.load_sound("Roulette", "assets/sounds/RouletteSpin.mp3")
        self.game.sound_manager.load_sound("MapWinner", "assets/sounds/MapWinner.mp3")

        self.create_display_components()
    
    def create_display_components(self):
        """
        This function creates all the components in the Map Randomizer
        """
        self.background_image = pygame.transform.scale(pygame.image.load("assets/images/main_menu/main_menu_background.png").convert(), size(100,100))
        maps_background_size = size(100, 60)
        self.maps_background = pygame.rect.Rect(0, 0, maps_background_size[0], maps_background_size[1])
        self.maps_background.center = position(50, 50)
        self.title_image = pygame.transform.scale(pygame.image.load("assets/images/map_randomizer/title.png").convert_alpha(), size(25, 20))
        self.title_rect = self.title_image.get_rect()
        self.title_rect.center = position(50, 10)
        map_size = size(50,50)
        self.map_images = [[pygame.transform.scale(pygame.image.load("assets/images/map_randomizer/venice.png").convert(), map_size),"venice"],
                           [pygame.transform.scale(pygame.image.load("assets/images/map_randomizer/florence.png").convert(), map_size),"florence"]]
        self.maps = []
        x = position_x(100) - size_x(50) // 2
        for _ in range(100):
            map = self.map_images[randint(0, len(self.map_images) - 1)]
            image, title = map[0], map[1]
            rect = image.get_rect()
            rect.center = (x, position_y(50))
            self.maps.append([image, rect, title])
            x -= size_x(52)
        self.maps_colliding = [False] * len(self.maps)
        self.cursor_image = pygame.transform.scale(pygame.image.load("assets/images/map_randomizer/cursor.png"), size(10, 20))
        self.cursor_rect = self.cursor_image.get_rect()
        self.cursor_rect.center = position(50, 80)
        self.winner_map_image = None
        self.winner_map_image_usable = None
        self.winner_map_rect = pygame.rect.Rect(0, 0, 1, 1)
        self.winner_map_rect.center = position(50, 50)
        self.font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 55)
    
    def manage_events(self):
        """
        This function manages the principal logic
        """
        # We check de collision of the maps with the cursor (it makes a noise)
        for i, map_data in enumerate(self.maps):
            map_rect = map_data[1]
            collision = self.cursor_rect.colliderect(map_rect)

            if not self.maps_colliding[i] and collision:
                self.game.sound_manager.play_sound("Roulette")

            self.maps_colliding[i] = collision
        
        # We check the result if the wheel stops spinning
        if self.velocity <= 0 and not self.result_checked:
            self.check_result()
            self.result_checked = True
        
        # We show the winner map missage
        if self.winner_map and not self.message_started:
            self.message = self.font.render(f"Winner map: {self.winner_map}", True, (255, 255, 0))
            self.message_rect = self.message.get_rect()
            self.message_rect.center = position(50, 50)
            self.show_message = True
            self.start_time = pygame.time.get_ticks()
            self.message_started = True
        
        # We kill this window when the message ends
        if self.show_message and pygame.time.get_ticks() - self.start_time > 3000:
            self.status = False
            self.game.character_selection.status = True
            self.game.fight.map = self.winner_map_image_usable
            self.game.fight.create_display_components()


    def check_result(self):
        """
        This function check which map is the selected
        """
        distances = [(map[0] , abs(self.cursor_rect.center[0] - map[1].center[0]), map[2]) for map in self.maps]
        winner_tuple = min(distances, key=lambda x: x[1])
        self.winner_map = winner_tuple[2]
        self.winner_map_image = winner_tuple[0]
        self.winner_map_image_usable = winner_tuple[0]
        self.game.sound_manager.play_sound("MapWinner")
    
        
    def move(self, dt):
        """
        This function manages the animations / movement
        """
        # We move and rest velocity
        if self.velocity > 0:  
            for i in range(len(self.maps)):
                self.maps[i][1].x += self.velocity * dt
            self.velocity -= 550 * dt
        # This animate the winner map window when there's a winner
        if self.winner_map:
            if self.winner_map_rect.width < size_x(50) or self.winner_map_rect.height < size_y(50):
                center = self.winner_map_rect.center
                new_width = self.winner_map_rect.width + size_x(100) * dt
                new_height = self.winner_map_rect.height + size_y(100) * dt
                self.winner_map_image_usable = pygame.transform.scale(self.winner_map_image, (int(new_width), int(new_height)))
                self.winner_map_rect = self.winner_map_image_usable.get_rect()
                self.winner_map_rect.center = center


    def draw(self, screen):
        """
        This function draws all the components
        """
        screen.blit(self.background_image, (0, 0))
        pygame.draw.rect(screen, (25, 25, 25), self.maps_background)
        pygame.draw.rect(screen, (255, 180, 0), self.title_rect)
        screen.blit(self.title_image, self.title_rect)
        for map in self.maps:
            screen.blit(map[0], map[1])
        screen.blit(self.cursor_image, self.cursor_rect)
        if self.winner_map:
            pygame.draw.rect(screen, (255, 180, 0), self.winner_map_rect.inflate(40, 40))
            screen.blit(self.winner_map_image_usable, self.winner_map_rect)
        if self.show_message:
            screen.blit(self.message, self.message_rect)
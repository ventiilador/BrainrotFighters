import pygame
from characters.Character import Character
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
from characters.Projectile import Proyectile

# Lirililarila class that inherits from the Character class
class Lirililarila(Character):
    def __init__(self, fight, controls, pos):
        # Set sprite size for the character
        self.sprite_size = size(25, 35)

        # ASIGNARRRR!!! (This seems to be a comment or placeholder for "assign")
        # Load profile and skill images and scale them to fit the sprite size
        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/lirili_larila/marco_lirili_larila.png"), size(7, 12))
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/lirili_larila/lirili_larila_basic_skill_image.png"), size(7, 10))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/lirili_larila/lirili_larila_elemental_skill_image.png"), size(7, 10))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/lirili_larila/lirili_larila_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites for movement animations (left, right) and idle animations
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_left_{}.png", 3, self.sprite_size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_right_{}.png", 3, self.sprite_size)
        
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_idle_left_{}.png", 3, self.sprite_size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_idle_right_{}.png", 3, self.sprite_size)
        
        # Load sprites for each skill animation (basic, elemental, ultimate)
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_left_{}.png", 3, self.sprite_size)
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_right_{}.png", 3, self.sprite_size)

        # ASIGNAR SUS SPRITES (Assigning the elemental and ultimate skill sprites)
        self.elemental_skill_left_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_left_{}.png", 3, self.sprite_size)
        self.elemental_skill_right_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_right_{}.png", 3, self.sprite_size)
        self.ultimate_skill_left_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_left_{}.png", 3, self.sprite_size)
        self.ultimate_skill_right_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_right_{}.png", 3, self.sprite_size)

        # Initialize sprite indexes for each animation type
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Set character's hitbox size
        self.size = size(15, 20)

        # Initialize the base class (Character) with provided parameters
        super().__init__(fight, controls, pos)

        # Load sound effects for various actions (like punching and special skills)
        self.fight.game.sound_manager.load_sound("LiriliLarilaPunch", "assets/sounds/lirili_larila_stand_punch.mp3")
        self.fight.game.sound_manager.load_sound("TomaApisonadora", "assets/sounds/toma_apisonadora.mp3")
        self.fight.game.sound_manager.load_sound("ExplosionApisonadora", "assets/sounds/bombardiro_missile_explosion.mp3")
        self.fight.game.sound_manager.load_sound("ZaWarudo", "assets/sounds/zawarudo.mp3")

        # Initialize skills
        self.stand = None
        self.basic_skill_cooldown = 7000  # Cooldown for basic skill in milliseconds
        self.basic_skill_damage = 10

        self.apisonadora = None  # The elemental skill projectile
        self.elemental_skill_update_time = 700  # Time interval for elemental skill updates
        self.elemental_skill_cooldown = 5000  # Cooldown for elemental skill
        self.elemental_skill_damage = 15

        self.time_stop = 12  # Time duration for ultimate skill (time stop)
        self.elapsed_time_stop = 0  # Track elapsed time for time stop effect
        self.ultimate_skill_cooldown = 30000  # Cooldown for ultimate skill

        # Initialize skill cooldown timers
        current_time = pygame.time.get_ticks()
        self.basic_skill_last_time = current_time - self.basic_skill_cooldown
        self.elemental_skill_last_time = current_time - self.elemental_skill_cooldown
        self.ultimate_skill_last_time = current_time - self.ultimate_skill_cooldown

        # Set the initial sprite for the character
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]

    # Manage game events, including movement of projectiles and time stop
    def manage_events(self, dt):
        super().manage_events(dt)
        current_time = pygame.time.get_ticks()

        # Handle movement and status of the elemental skill projectile
        if self.apisonadora:
            if self.apisonadora.status:
                self.apisonadora.move(dt)
            else:
                self.apisonadora = None
        
        # Handle movement and status of the basic skill projectile
        if self.stand:
            if self.stand.status:
                self.stand.move(dt)

        # If time stop is active, track its duration
        if not self.fight.time_running:
            self.elapsed_time_stop += dt
            if self.elapsed_time_stop >= self.time_stop:
                self.fight.time_running = True
                self.elapsed_time_stop = 0

    # Define the basic skill action (creates a projectile)
    def basic_skill(self):
        path = "assets/images/fight/lirili_larila/lirili_larila_stand_" + self.last_direction + "_{}.png"
        pos = (self.rect.center[0] + position_x(10), self.rect.center[1]) if self.last_direction == "left" else (self.rect.center[0] - position_x(10), self.rect.center[1])
        self.stand = Proyectile(pos, size(25, 30), size(15, 15), 200, 9, self.enemy, damage=self.basic_skill_damage, 
                                   animation_path=path, animation_cooldown=150, sprites_count=9, collision_sound="LiriliLarilaPunch",
                                     sound_manager=self.fight.game.sound_manager)

    # Define the elemental skill action (creates a powerful projectile)
    def elemental_skill(self):
        self.apisonadora = Proyectile((0, 0), size(30, 35), size(20, 20), 500, 5, self.enemy, damage=self.elemental_skill_damage, 
                                   animation_path="assets/images/fight/lirili_larila/apisonadora_{}.png", animation_cooldown=200, sprites_count=1, rotate=True,
                                   collision_sound="ExplosionApisonadora", sound_manager=self.fight.game.sound_manager)
        self.fight.game.sound_manager.play_sound("TomaApisonadora")
    
    # Define the ultimate skill action (stops time)
    def ultimate_skill(self):
        self.fight.time_running = False
        self.fight.game.sound_manager.play_sound("ZaWarudo")

    # Draw the character and its projectiles on the screen
    def draw(self, screen):
        img_rect = self.current_sprite.get_rect()
        img_rect.center = self.rect.center
        screen.blit(self.current_sprite, img_rect)
        
        # Draw projectiles if they exist and are active
        if self.apisonadora:
            if self.apisonadora.status:
                self.apisonadora.draw(screen)
        
        if self.stand:
            if self.stand.status:
                self.stand.draw(screen)
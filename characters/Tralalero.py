import pygame
from characters.Character import Character
from characters.Projectile import Proyectile
from functions import load_sprites, size, position_x, position_y
from random import randint

class Tralalero(Character):
    def __init__(self, fight, character_name, controls):
        self.sprite_size = size(20, 25)

        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/marco_tralalalero.png").convert(), size(7, 12))
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/tralalero_basic_skill_image.png"), size(10, 15))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/tralalero_elemental_skill_image.png"), size(7, 10))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/tralalero_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_left_{}.png", 3, self.sprite_size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_right_{}.png", 3, self.sprite_size)
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_idle_left_{}.png", 2, self.sprite_size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_idle_right_{}.png", 2, self.sprite_size)
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_basic_skill_left_{}.png", 4, self.sprite_size
        )
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_basic_skill_right_{}.png", 4, self.sprite_size
        )
        self.elemental_skill_left_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_elemental_skill_left_{}.png", 5, self.sprite_size
        )
        self.elemental_skill_right_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_elemental_skill_right_{}.png", 5, self.sprite_size
        )

        self.ultimate_skill_left_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_elemental_skill_left_{}.png", 5, self.sprite_size
        )
        self.ultimate_skill_right_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_elemental_skill_right_{}.png", 5, self.sprite_size
        )

        # Indexs
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Elemental skill
        self.bubbles = []

        # Ultimate skill
        self.wave = None

        self.size = size(10, 15)
        super().__init__(fight, character_name, controls)

        # Set initial sprite
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]
    
    def manage_events(self, dt):
        super().manage_events(dt)
        for bubble in self.bubbles:
            if bubble.status:
                bubble.move(dt)
        
        if self.wave:
            if self.wave.status:
                self.wave.move(dt)
    
    def basic_skill(self):
        if self.rect.colliderect(self.enemy.rect):
            self.enemy.health -= self.basic_skill_damage
    
    def elemental_skill(self):
        for i in range(randint(2, 4)):
            bubble = Proyectile((randint(self.rect.center[0] - position_x(5), self.rect.center[0] + position_x(5)), randint(self.rect.center[1] - position_y(5), self.rect.center[1] + position_y(5))),
                                size(3, 5), size(3, 4), 300, 4, self.enemy, damage=10, animation_path="assets/images/fight/tralalero_tralala/bubble_{}.png", animation_cooldown=200, sprites_count=1)
            self.bubbles.append(bubble)
    
    def ultimate_skill(self):
        objective = (self.rect.center[0] - position_x(70), self.rect.center[1]) if self.last_direction == "left" else (self.rect.center[0] + position_x(40), self.rect.center[1])
        self.wave = Proyectile(self.rect.topleft, size(20, 25), size(16, 23), 300, 6, self.enemy, damage=20, debuff=("x_velocity", 400, 3), objective=objective,
                                animation_path="assets/images/fight/tralalero_tralala/"+self.last_direction+"_wave_{}.png", animation_cooldown=500, sprites_count=3)
    
    def draw(self, screen):
        img_rect = self.current_sprite.get_rect()
        img_rect.center = self.rect.center
        screen.blit(self.current_sprite, img_rect)
        for bubble in self.bubbles:
            if bubble.status:
                bubble.draw(screen)
        if self.wave:
            if self.wave.status:
                self.wave.draw(screen)
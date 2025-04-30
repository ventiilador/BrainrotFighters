import pygame
from characters.Character import Character
from characters.Projectile import Proyectile
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
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
        self.left_wave_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/left_wave.png").convert_alpha(), size(20, 70))
        self.right_wave_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/right_wave.png").convert_alpha(), size(20, 70))
        self.wave_rect = self.left_wave_img.get_rect()
        self.wave_direction = None
        self.wave_status = False
        self.wave_speed = 500
        self.wave_lifetime = 5
        self.wave_time = 0

        self.size = size(10, 15)
        super().__init__(fight, character_name, controls)

        # Set initial sprite
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]
    
    def manage_events(self, dt):
        super().manage_events(dt)
        for bubble in self.bubbles:
            if bubble.status:
                bubble.move(dt)
        
        if self.wave_status:
            enemy_colliding = self.wave_rect.colliderect(self.enemy.rect)
            if enemy_colliding:
                self.enemy.debuff("x_velocity", 200, 4)
                self.enemy.health -= self.ultimate_skill_damage
            if self.wave_time >= self.wave_lifetime or enemy_colliding:
                self.wave_time = 0
                self.wave_status = False
                return
            self.wave_time += dt
            if self.wave_direction == "left":
                self.wave_rect.x -= self.wave_speed * dt
            else:
                self.wave_rect.x += self.wave_speed * dt

    def draw(self, screen):
        super().draw(screen)
        for bubble in self.bubbles:
            if bubble.status:
                bubble.draw(screen)
        if self.wave_status:
            wave = self.left_wave_img if self.wave_direction == "left" else self.right_wave_img
            screen.blit(wave, self.wave_rect)
    
    def basic_skill(self):
        if self.rect.colliderect(self.enemy.rect):
            self.enemy.health -= self.basic_skill_damage
    
    def elemental_skill(self):
        for i in range(randint(2, 4)):
            bubble = Proyectile((randint(self.rect.center[0] - position_x(5), self.rect.center[0] + position_x(5)), randint(self.rect.center[1] - position_y(5), self.rect.center[1] + position_y(5))),
                                size(3, 5), 300, 4, 200, self.enemy, damage=10, animation_path="assets/images/fight/tralalero_tralala/bubble_{}.png", sprites_count=1)
            self.bubbles.append(bubble)
    
    def ultimate_skill(self):
        self.wave_direction = self.last_direction
        self.wave_rect.center = self.rect.center
        self.wave_status = True
    
    def draw(self, screen):
        screen.blit(self.current_sprite, (self.rect.x - self.rect.size[0] // 2, self.rect.y - size_y(5)))
from random import randint
import pygame
from characters.Character import Character
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
from characters.Projectile import Proyectile

class Tumtum(Character):
    def __init__(self, fight, character_name, controls):
        self.sprite_size = size(20, 25)

        # ASIGNARRRR!!!
        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/tumtum_sahur/marco_tumtum.png").convert(), size(7, 12))
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tumtum_sahur/tum_tum_basic_skill_image.png"), size(7, 10))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/bombardiro_crocodilo/bombardiro_elemental_skill_image.png"), size(7, 10))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/bombardiro_crocodilo/bombardiro_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/tumtum_sahur/tum_tum_left_{}.png", 5, self.sprite_size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/tumtum_sahur/tum_tum_right_{}.png", 5, self.sprite_size)
        
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/tumtum_sahur/tum_tum_idle_left_{}.png", 3, self.sprite_size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/tumtum_sahur/tum_tum_idle_right_{}.png", 3, self.sprite_size)
        
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/tumtum_sahur/tum_tum_basic_skill_left_{}.png", 3, self.sprite_size
        )
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/tumtum_sahur/tum_tum_basic_skill_right_{}.png", 3, self.sprite_size
        )
        # ASIGNAR SUS SPRITES
        self.elemental_skill_left_animation = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_elemental_skill_left_{}.png", 3, self.sprite_size
        )
        self.elemental_skill_right_animation = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_elemental_skill_right_{}.png", 3, self.sprite_size
        )
        self.ultimate_skill_left_animation = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_ultimate_skill_left_{}.png", 5, self.sprite_size
        )
        self.ultimate_skill_right_animation = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_ultimate_skill_right_{}.png", 5, self.sprite_size
        )

        # Indexs
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Hitbox_size
        self.size = size(10, 25)
        super().__init__(fight, character_name, controls)

        # Basic skill

        # Elemental skill
        self.stick = None

        # Ultimate skill

        # 0 cooldowns
        current_time = pygame.time.get_ticks()
        self.basic_skill_last_time = current_time - self.basic_skill_cooldown
        self.elemental_skill_last_time = current_time - self.elemental_skill_cooldown
        self.ultimate_skill_last_time = current_time - self.ultimate_skill_cooldown

        # Set initial sprite
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]

    def manage_events(self, dt):
        super().manage_events(dt)
        if self.stick:
            if self.stick.status:
                self.stick.move(dt)
            else:
                self.stick = None

    def basic_skill(self):
        if self.rect.colliderect(self.enemy.rect):
            self.enemy.health -= self.basic_skill_damage
    
    def elemental_skill(self):
        self.stick = Proyectile(self.rect.center, size(10, 15), size(6, 6), 1000, 3, self.enemy, damage=10, 
                    animation_path="assets/images/fight/tumtum_sahur/stick_{}.png", animation_cooldown=200, sprites_count=3, rotate=True)
    
    def ultimate_skill(self):
        pass

    def draw(self, screen):
        img_rect = self.current_sprite.get_rect()
        img_rect.center = self.rect.center
        screen.blit(self.current_sprite, img_rect)
        if self.stick:
            if self.stick.status:
                self.stick.draw(screen)
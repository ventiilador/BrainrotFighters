import pygame
from characters.Character import Character
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
from characters.Projectile import Proyectile

class Bombardiro(Character):
    def __init__(self, fight, character_name, controls):
        self.sprite_size = size(25, 20)

        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/marco_tralalalero.png").convert(), size(7, 12))
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/tralalero_basic_skill_image.png"), size(10, 15))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/tralalero_elemental_skill_image.png"), size(7, 10))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/tralalero_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_left_{}.png", 2, self.sprite_size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_right_{}.png", 2, self.sprite_size)
        
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_idle_left_{}.png", 2, self.sprite_size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_idle_right_{}.png", 2, self.sprite_size)
        
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

        self.size = size(20, 15)
        super().__init__(fight, character_name, controls)

        self.missile = None

        # Set initial sprite
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]
    
    def manage_events(self, dt):
        super().manage_events(dt)
        if self.missile:
            if self.missile.status:
                self.missile.move(dt)

    def draw(self, screen):
        super().draw(screen)
        if self.missile:
            if self.missile.status:
                self.missile.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

    def basic_skill(self):
        self.missile = Proyectile(self.rect.center, size(30, 30), 1000, 3, 200, self.enemy, damage=10,
                                   animation_path="assets/images/fight/bombardiro_crocodilo/missile_{}.png", sprites_count=4, rotate=True)
    
    def elemental_skill(self):
        pass
    
    def ultimate_skill(self):
        pass

    def draw(self, screen):
        screen.blit(self.current_sprite, (self.rect.x - self.rect.size[0] // 2, self.rect.y - size_y(5)))
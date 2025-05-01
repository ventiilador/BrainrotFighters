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
            "assets/images/fight/bombardiro_crocodilo/bombardiro_basic_skill_left_{}.png", 3, self.sprite_size
        )
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_basic_skill_right_{}.png", 3, self.sprite_size
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

        self.fly_time = 10
        self.flying_time = 0
        self.can_fly = False

        # Set initial sprite
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]
    
    def manage_events(self, dt):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.rect.bottom >= self.ground_y and not self.can_fly:
            if keys[self.controls[0]] and self.rect.bottom >= self.ground_y and not self.can_fly:
                self.y_velocity = self.jump_strength

        if keys[self.controls[1]] and not keys[self.controls[3]]:
            if self.rect.left >= 0:
                self.rect.x -= self.x_velocity * dt
            self.last_direction = "left"
            self.left_animation()

        if keys[self.controls[3]] and not keys[self.controls[1]]:
            if self.rect.right <= position_x(100):
                self.rect.x += self.x_velocity * dt
            self.last_direction = "right"
            self.right_animation()
        
        if keys[self.controls[4]] and current_time - self.basic_skill_last_time > self.basic_skill_cooldown:
            self.doing_basic_skill = True
            self.basic_skill_last_time = current_time
            self.basic_skill()
        self.skill("basic_skill")

        if keys[self.controls[5]] and current_time - self.elemental_skill_last_time > self.elemental_skill_cooldown:
            self.doing_elemental_skill = True
            self.elemental_skill_last_time = current_time
            self.elemental_skill()
        self.skill("elemental_skill")

        if keys[self.controls[6]] and current_time - self.ultimate_skill_last_time > self.ultimate_skill_cooldown:
            self.doing_ultimate_skill = True
            self.ultimate_skill_last_time = current_time
            self.ultimate_skill()
        self.skill("ultimate_skill")
        
        if self.rect.bottom >= self.ground_y and not keys[self.controls[1]] and not keys[self.controls[3]] and not self.doing_basic_skill and not self.doing_elemental_skill:
            self.idle_animation()

        if (self.rect.bottom < self.ground_y or self.y_velocity < 0) and not self.can_fly:
            self.y_velocity += self.gravity * dt
            self.rect.y += self.y_velocity * dt

        if self.rect.bottom >= self.ground_y and not self.can_fly:
            self.rect.bottom = self.ground_y
            self.y_velocity = 0
        
        if self.x_velocity_debuffed:
            self.x_velocity_debuffed_time += dt
            if self.x_velocity_debuffed_time >= self.x_velocity_cooldown:
                self.x_velocity_debuffed = False
                self.x_velocity_debuffed_time = 0
                self.x_velocity = 800
                return
            
        # --------------------------------------------------

        if self.missile:
            if self.missile.status:
                self.missile.move(dt)
        
        if self.can_fly:
            self.flying_time += dt
            if self.flying_time >= self.fly_time:
                self.can_fly = False
                self.flying_time = 0
            else:
                self.rect.y -= 1000 * dt

    def draw(self, screen):
        super().draw(screen)
        if self.missile:
            if self.missile.status:
                self.missile.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

    def basic_skill(self):
        self.missile = Proyectile(self.rect.center, size(15, 15), size(7, 7), 1000, 3, self.enemy, damage=10, 
                                   animation_path="assets/images/fight/bombardiro_crocodilo/missile_{}.png", animation_cooldown=200, sprites_count=4, rotate=True)
    
    def elemental_skill(self):
        self.can_fly = True
    
    def ultimate_skill(self):
        pass

    def draw(self, screen):
        img_rect = self.current_sprite.get_rect()
        img_rect.center = self.rect.center
        screen.blit(self.current_sprite, img_rect)
        if self.missile:
            if self.missile.status:
                self.missile.draw(screen)
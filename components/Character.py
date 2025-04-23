import pygame
from functions import size, position_y, position_x, load_sprites

class Character:
    def __init__(self, fight, character_name, controls: tuple):
        self.fight = fight

        self.controls = controls

        self.rect = pygame.rect.Rect(position_x(90), 0, self.size[0], self.size[1])

        # Movement physics
        self.gravity = 2200
        self.jump_strength = -1000
        self.y_velocity = 0
        self.x_velocity = 800

        # Ground position limit
        self.ground_y = position_y(90)

        # Animation timing
        self.animations_cooldown = 300
        self.last_left_animation_time = 0
        self.last_right_animation_time = 0
        self.last_idle_animation_time = 0
        self.last_direction = "left"

        # Skills
        self.basic_skill_cooldown = 1000
        self.doing_basic_skill = False
        self.basic_skill_last_time = 0
        self.basic_skill_damage = 7

        # Stats
        self.health = 100

    def animate(self, sprites, current_index_attr, cooldown_attr, time_attr):
        current_time = pygame.time.get_ticks()
        if current_time - getattr(self, time_attr) >= getattr(self, cooldown_attr):
            index = getattr(self, current_index_attr)
            index = 0 if index + 1 >= len(sprites) else index + 1
            setattr(self, current_index_attr, index)
            self.current_sprite = sprites[index]
            setattr(self, time_attr, current_time)

    def move(self, dt):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if keys[self.controls[0]] and self.rect.bottom >= self.ground_y:
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
        
        if self.rect.bottom >= self.ground_y and not keys[self.controls[1]] and not keys[self.controls[3]] and not self.doing_basic_skill:
            self.idle_animation()

        if self.rect.bottom < self.ground_y or self.y_velocity < 0:
            self.y_velocity += self.gravity * dt
            self.rect.y += self.y_velocity * dt

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.y_velocity = 0

    def left_animation(self):
        self.animate(self.left_animation_sprites, 'current_left_sprite', 'animations_cooldown', 'last_left_animation_time')

    def right_animation(self):
        self.animate(self.right_animation_sprites, 'current_right_sprite', 'animations_cooldown', 'last_right_animation_time')
    
    def idle_animation(self):
        if self.last_direction == "left":
            self.animate(self.idle_left_animation_sprites, 'current_left_idle_sprite', 'animations_cooldown', 'last_idle_animation_time')
        elif self.last_direction == "right":
            self.animate(self.idle_right_animation_sprites, 'current_right_idle_sprite', 'animations_cooldown', 'last_idle_animation_time')
    
    def basic_skill(self):
        pass

    def deal_damage(dmg):
        pass

    def draw(self, screen):
        screen.blit(self.current_sprite, self.rect)


class Tralalero(Character):
    def __init__(self, fight, character_name, controls):
        self.size = size(20, 25)

        # Load character sprites
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_left_{}.png", 3, self.size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_right_{}.png", 3, self.size)
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_idle_left_{}.png", 2, self.size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_idle_right_{}.png", 2, self.size)
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_basic_skill_left_{}.png", 4, self.size
        )
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_basic_skill_right_{}.png", 4, self.size
        )

        self.current_left_sprite = 0
        self.current_right_sprite = 0
        self.current_left_idle_sprite = 0
        self.current_right_idle_sprite = 0
        self.current_left_basic_skill_sprite = 0
        self.current_right_basic_skill_sprite = 0

        super().__init__(character_name, controls)

        # Set initial sprite
        self.current_sprite = self.left_animation_sprites[self.current_left_sprite]
    
        
    def basic_skill(self):
        if not self.doing_basic_skill:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.basic_skill_last_time <= self.animations_cooldown:
            return

        side = self.last_direction
        anim_attr = f"basic_skill_{side}_animation"
        index_attr = f"current_{side}_basic_skill_sprite"

        current_index = getattr(self, index_attr)
        animation_frames = getattr(self, anim_attr)

        if current_index + 1 >= len(animation_frames):
            setattr(self, index_attr, 0)
            self.doing_basic_skill = False
            self.deal_damage(self.basic_skill_damage)
        else:
            setattr(self, index_attr, current_index + 1)

        self.current_sprite = animation_frames[getattr(self, index_attr)]
        self.basic_skill_last_time = current_time
    
    def deal_damage(self, dmg):
        pass
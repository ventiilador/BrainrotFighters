from random import randint
import pygame
from functions import size, position_y, position_x, load_sprites, size_x, size_y

class Character:
    def __init__(self, fight, player_name, controls: tuple):
        self.fight = fight
        self.player_name = player_name

        self.controls = controls

        self.rect = pygame.rect.Rect(position_x(90), 0, self.size[0], self.size[1])

        # Movement physics
        self.gravity = 2200
        self.jump_strength = -1000
        self.y_velocity = 0
        self.x_velocity = 800
        self.x_velocity_debuffed = False
        self.x_velocity_debuffed_time = 0

        # Ground position limit
        self.ground_y = position_y(90)

        # Animation timing
        self.animations_cooldown = 300
        self.last_left_walk_animation_time = 0
        self.last_right_walk_animation_time = 0
        self.last_idle_animation_time = 0
        self.last_direction = "left"

        # Skills
        self.basic_skill_cooldown = 1000
        self.basic_skill_update_time = 200
        self.doing_basic_skill = False
        self.basic_skill_last_time = 0
        self.basic_skill_damage = 7

        self.elemental_skill_cooldown = 5000
        self.elemental_skill_update_time = 200
        self.doing_elemental_skill = False
        self.elemental_skill_last_time = 0
        self.elemental_skill_damage = 7
        
        self.ultimate_skill_cooldown = 10000
        self.ultimate_skill_update_time = 200
        self.doing_ultimate_skill = False
        self.ultimate_skill_last_time = 0
        self.ultimate_skill_damage = 7

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

    def manage_events(self, dt):
        print(self.health)
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

        if self.rect.bottom < self.ground_y or self.y_velocity < 0:
            self.y_velocity += self.gravity * dt
            self.rect.y += self.y_velocity * dt

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.y_velocity = 0
        
        if self.x_velocity_debuffed:
            self.x_velocity_debuffed_time += dt
            if self.x_velocity_debuffed_time >= self.x_velocity_cooldown:
                self.x_velocity_debuffed = False
                self.x_velocity_debuffed_time = 0
                self.x_velocity = 800
                return
            
            

    def left_animation(self):
        self.animate(self.left_animation_sprites, 'current_walk_sprite', 'animations_cooldown', 'last_left_walk_animation_time')

    def right_animation(self):
        self.animate(self.right_animation_sprites, 'current_walk_sprite', 'animations_cooldown', 'last_right_walk_animation_time')
    
    def idle_animation(self):
        if self.last_direction == "left":
            self.animate(self.idle_left_animation_sprites, 'current_idle_sprite', 'animations_cooldown', 'last_idle_animation_time')
        elif self.last_direction == "right":
            self.animate(self.idle_right_animation_sprites, 'current_idle_sprite', 'animations_cooldown', 'last_idle_animation_time')
    
    def skill(self, skill_name):
        if not getattr(self, f"doing_{skill_name}", False):
            return

        current_time = pygame.time.get_ticks()
        
        last_skill_time = getattr(self, f"{skill_name}_last_time")

        if current_time - last_skill_time <= getattr(self, skill_name + "_update_time"):
            return

        side = self.last_direction

        anim_attr = f"{skill_name}_{side}_animation"
        index_attr = f"current_{skill_name}_sprite"
        damage_attr = f"{skill_name}_damage"

        animation_frames = getattr(self, anim_attr)
        current_index = getattr(self, index_attr)

        if current_index + 1 >= len(animation_frames):
            setattr(self, index_attr, 0)
            setattr(self, f"doing_{skill_name}", False)
        else:
            setattr(self, index_attr, current_index + 1)

        self.current_sprite = animation_frames[getattr(self, index_attr)]

        setattr(self, f"{skill_name}_last_time", current_time)
    
    def debuff(self, attr, debff, time):
        if getattr(self, attr):
            setattr(self, attr, debff)
            setattr(self, attr+"_debuffed", True)
            setattr(self, attr+"_cooldown", time)

    def draw(self, screen):
        screen.blit(self.current_sprite, (self.rect.x - self.rect.size[0] // 2, self.rect.y - size_y(5)))


class Tralalero(Character):
    def __init__(self, fight, character_name, controls):
        self.sprite_size = size(20, 25)

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
        self.bubble_speed = 100
        self.bubbles_status = False
        self.bubbles_lifetime = 4

        # Ultimate skill
        self.wave_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/wave.png"), size(10, 70))
        self.wave_rect = self.wave_img.get_rect()
        self.wave_direction = None
        self.wave_status = False
        self.wave_speed = 1000
        self.wave_lifetime = 5
        self.wave_time = 0

        self.size = size(10, 15)
        super().__init__(fight, character_name, controls)

        # Set initial sprite
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]
    
    def manage_events(self, dt):
        super().manage_events(dt)
        enemy = self.fight.player2 if self.player_name == "player1" else self.fight.player1
        if self.bubbles_status:
            if not len(self.bubbles):
                self.bubbles_status = False
                return
            bubbles_new = []
            for i in range(len(self.bubbles)):
                self.bubbles[i][2] += dt
                print(self.bubbles[i][2])
                if self.bubbles[i][2] >= self.bubbles_lifetime:
                    continue
                if self.bubbles[i][1].colliderect(enemy.rect):
                    enemy.health -= self.elemental_skill_damage
                else:
                    bubbles_new.append(self.bubbles[i])

                dx = enemy.rect.center[0] - self.bubbles[i][1].x
                dy = enemy.rect.center[1] - self.bubbles[i][1].y
                
                length = (dx**2 + dy**2)**0.5
                if length != 0:
                    dx /= length
                    dy /= length
                vx = dx * self.bubble_speed
                vy = dy * self.bubble_speed
                self.bubbles[i][1].x += vx * dt
                self.bubbles[i][1].y += vy * dt
            self.bubbles = bubbles_new
        
        if self.wave_status:
            enemy_colliding = self.wave_rect.colliderect(enemy)
            if enemy_colliding:
                enemy.debuff("x_velocity", 200, 4)
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
            screen.blit(bubble[0], bubble[1])
        if self.wave_status:
            screen.blit(self.wave_img, self.wave_rect)
    
    def basic_skill(self):
        enemy = self.fight.player2 if self.player_name == "player1" else self.fight.player1
        if self.rect.colliderect(enemy.rect):
            enemy.health -= self.basic_skill_damage
    
    def elemental_skill(self):
        for i in range(randint(2, 4)):
            img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/bubble.png"), size(3, 3))
            rect = img.get_rect()
            center = self.rect.center
            rect.center = (randint(center[0] - position_x(5), center[0] + position_x(5)), randint(center[1] - position_y(5), center[1] + position_y(5)))
            self.bubbles.append([img, rect, 0])
        self.bubbles_status = True
    
    def ultimate_skill(self):
        self.wave_direction = self.last_direction
        self.wave_rect.center = self.rect.center
        self.wave_status = True
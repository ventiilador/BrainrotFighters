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
        self.basic_skill_objective_ticks = 0
        self.doing_basic_skill = False
        self.basic_skill_last_time = 0
        self.basic_skill_damage = 7

        self.elemental_skill_cooldown = 5000
        self.elemental_skill_update_time = 200
        self.elemental_skill_objective_ticks = 0
        self.doing_elemental_skill = False
        self.elemental_skill_last_time = 0
        self.elemental_skill_damage = 7
        
        self.ultimate_skill_cooldown = 10000
        self.ultimate_skill_update_time = 200
        self.ultimate_skill_objective_ticks = 0
        self.doing_ultimate_skill = False
        self.ultimate_skill_last_time = 0
        self.ultimate_skill_damage = 20

        # Stats
        self.health = 100
    
    def set_enemy(self, enemy):
        self.enemy = enemy

    def animate(self, sprites, current_index_attr, cooldown_attr, time_attr):
        current_time = pygame.time.get_ticks()
        if current_time - getattr(self, time_attr) >= getattr(self, cooldown_attr):
            index = getattr(self, current_index_attr)
            index = 0 if index + 1 >= len(sprites) else index + 1
            setattr(self, current_index_attr, index)
            self.current_sprite = sprites[index]
            setattr(self, time_attr, current_time)

    def manage_events(self, dt):
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

        if keys[self.controls[5]]: 
            if current_time - self.elemental_skill_last_time > self.elemental_skill_cooldown:
                self.doing_elemental_skill = True
                self.elemental_skill_last_time = current_time
                self.elemental_skill()
        self.skill("elemental_skill")

        if keys[self.controls[6]] and current_time - self.ultimate_skill_last_time > self.ultimate_skill_cooldown:
            self.doing_ultimate_skill = True
            self.ultimate_skill_last_time = current_time
            self.ultimate_skill()
        self.skill("ultimate_skill")
        
        if (self.rect.bottom >= self.ground_y and not keys[self.controls[1]] and not keys[self.controls[3]] and
             not self.doing_basic_skill and not self.doing_elemental_skill and not self.doing_ultimate_skill):
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
            setattr(self, f"{skill_name}_objective_ticks", pygame.time.get_ticks() + getattr(self, f"{skill_name}_cooldown"))
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
        pass
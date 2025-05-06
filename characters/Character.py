import pygame
from functions import size, position_y, position_x, load_sprites, size_x, size_y

class Character:
    def __init__(self, fight, controls: tuple, pos):
        # Initializes the character with the provided fight object, control keys, and position.
        self.fight = fight

        self.controls = controls

        # Rectangle for the character's position and size
        self.rect = pygame.rect.Rect(pos[0], pos[1], self.size[0], self.size[1])

        # Movement physics
        self.gravity = 2200  # Gravity force
        self.jump_strength = -1000  # Jump strength (negative to make it go up)
        self.y_velocity = 0  # Vertical velocity
        self.x_velocity = 800  # Horizontal velocity
        self.x_velocity_debuffed = False  # Whether the character's horizontal speed is debuffed
        self.x_velocity_debuffed_time = 0  # Time tracking for the debuff

        # Ground position limit
        self.ground_y = position_y(90)  # Position of the ground in the game world

        # Animation timing
        self.animations_cooldown = 300  # Cooldown time between animations (milliseconds)
        self.last_left_walk_animation_time = 0  # Last time the left walking animation was updated
        self.last_right_walk_animation_time = 0  # Last time the right walking animation was updated
        self.last_idle_animation_time = 0  # Last time the idle animation was updated
        self.last_direction = "left"  # Last direction the character moved (for idle animation)

        # Skills' cooldowns and damage
        self.basic_skill_cooldown = 1000  # Cooldown for basic skill
        self.basic_skill_update_time = 200  # Update time for basic skill animation
        self.basic_skill_objective_ticks = 0  # Used for skill duration
        self.doing_basic_skill = False  # Whether the basic skill is being performed
        self.basic_skill_last_time = 0  # Last time the basic skill was used
        self.basic_skill_damage = 7  # Damage for the basic skill

        self.elemental_skill_cooldown = 5000  # Cooldown for elemental skill
        self.elemental_skill_update_time = 200  # Update time for elemental skill animation
        self.elemental_skill_objective_ticks = 0  # Used for elemental skill duration
        self.doing_elemental_skill = False  # Whether the elemental skill is being performed
        self.elemental_skill_last_time = 0  # Last time the elemental skill was used
        self.elemental_skill_damage = 7  # Damage for the elemental skill
        
        self.ultimate_skill_cooldown = 10000  # Cooldown for ultimate skill
        self.ultimate_skill_update_time = 200  # Update time for ultimate skill animation
        self.ultimate_skill_objective_ticks = 0  # Used for ultimate skill duration
        self.doing_ultimate_skill = False  # Whether the ultimate skill is being performed
        self.ultimate_skill_last_time = 0  # Last time the ultimate skill was used
        self.ultimate_skill_damage = 20  # Damage for the ultimate skill

        # Stats
        self.health = 100  # Health of the character
        self.armor = 1  # Armor of the character
    
    def set_enemy(self, enemy):
        # Sets the enemy for the character
        self.enemy = enemy

    def animate(self, sprites, current_index_attr, cooldown_attr, time_attr):
        # Handles animation by cycling through the sprite list based on the time
        current_time = pygame.time.get_ticks()
        if current_time - getattr(self, time_attr) >= getattr(self, cooldown_attr):
            index = getattr(self, current_index_attr)
            index = 0 if index + 1 >= len(sprites) else index + 1  # Loop the animation
            setattr(self, current_index_attr, index)
            self.current_sprite = sprites[index]
            setattr(self, time_attr, current_time)  # Update the last animation time

    def manage_events(self, dt):
        # Handles user input (keyboard events) and updates the character state
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Jumping: Triggered by pressing the jump control key
        if keys[self.controls[0]] and self.rect.bottom >= self.ground_y:
            self.y_velocity = self.jump_strength

        # Moving left: Triggered by pressing the left control key
        if keys[self.controls[1]] and not keys[self.controls[3]]:
            if self.rect.left >= 0:
                self.rect.x -= self.x_velocity * dt  # Move left by velocity * delta time
            self.last_direction = "left"
            self.left_animation()

        # Moving right: Triggered by pressing the right control key
        if keys[self.controls[3]] and not keys[self.controls[1]]:
            if self.rect.right <= position_x(100):
                self.rect.x += self.x_velocity * dt  # Move right by velocity * delta time
            self.last_direction = "right"
            self.right_animation()
        
        # Activating basic skill
        if keys[self.controls[4]] and current_time - self.basic_skill_last_time > self.basic_skill_cooldown and not (self.doing_elemental_skill or self.doing_ultimate_skill):
            self.doing_basic_skill = True
            self.basic_skill_last_time = current_time
            self.basic_skill()
        self.skill("basic_skill")

        # Activating elemental skill
        if keys[self.controls[5]]: 
            if current_time - self.elemental_skill_last_time > self.elemental_skill_cooldown and not (self.doing_basic_skill or self.doing_ultimate_skill):
                self.doing_elemental_skill = True
                self.elemental_skill_last_time = current_time
                self.elemental_skill()
        self.skill("elemental_skill")

        # Activating ultimate skill
        if keys[self.controls[6]] and current_time - self.ultimate_skill_last_time > self.ultimate_skill_cooldown and not (self.doing_basic_skill or self.doing_elemental_skill):
            self.doing_ultimate_skill = True
            self.ultimate_skill_last_time = current_time
            self.ultimate_skill()
        self.skill("ultimate_skill")
        
        # Idle animation when no movement and no skills are active
        if (self.rect.bottom >= self.ground_y and not keys[self.controls[1]] and not keys[self.controls[3]] and
             not self.doing_basic_skill and not self.doing_elemental_skill and not self.doing_ultimate_skill):
            self.idle_animation()

        # Gravity: Apply gravity to the character if it's in the air
        if self.rect.bottom < self.ground_y or self.y_velocity < 0:
            self.y_velocity += self.gravity * dt
            self.rect.y += self.y_velocity * dt

        # Prevent going below the ground
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.y_velocity = 0
        
        # Handling the debuff on the character's horizontal speed
        if self.x_velocity_debuffed:
            self.x_velocity_debuffed_time += dt
            if self.x_velocity_debuffed_time >= self.x_velocity_cooldown:
                self.x_velocity_debuffed = False
                self.x_velocity_debuffed_time = 0
                self.x_velocity = 800  # Reset to normal velocity
                return
            
    def left_animation(self):
        # Animates the character's walking left
        self.animate(self.left_animation_sprites, 'current_walk_sprite', 'animations_cooldown', 'last_left_walk_animation_time')

    def right_animation(self):
        # Animates the character's walking right
        self.animate(self.right_animation_sprites, 'current_walk_sprite', 'animations_cooldown', 'last_right_walk_animation_time')
    
    def idle_animation(self):
        # Animates the character when idle (not moving)
        if self.last_direction == "left":
            self.animate(self.idle_left_animation_sprites, 'current_idle_sprite', 'animations_cooldown', 'last_idle_animation_time')
        elif self.last_direction == "right":
            self.animate(self.idle_right_animation_sprites, 'current_idle_sprite', 'animations_cooldown', 'last_idle_animation_time')
    
    def skill(self, skill_name):
        # Handles skill animations and cooldowns
        if not getattr(self, f"doing_{skill_name}", False):
            return

        current_time = pygame.time.get_ticks()
        
        last_skill_time = getattr(self, f"{skill_name}_last_time")

        # Skip skill animation if it is not yet time to update
        if current_time - last_skill_time <= getattr(self, skill_name + "_update_time"):
            return

        side = self.last_direction

        anim_attr = f"{skill_name}_{side}_animation"
        index_attr = f"current_{skill_name}_sprite"
        damage_attr = f"{skill_name}_damage"

        animation_frames = getattr(self, anim_attr)
        current_index = getattr(self, index_attr)

        # Cycle the animation frames and check if it's time to end the skill animation
        if current_index + 1 >= len(animation_frames):
            setattr(self, index_attr, 0)
            setattr(self, f"doing_{skill_name}", False)
            setattr(self, f"{skill_name}_objective_ticks", pygame.time.get_ticks() + getattr(self, f"{skill_name}_cooldown"))
        else:
            setattr(self, index_attr, current_index + 1)

        self.current_sprite = animation_frames[getattr(self, index_attr)]

        setattr(self, f"{skill_name}_last_time", current_time)
    
    
    def debuff(self, attr, debff, time):
        # Applies a debuff to the character's attribute for a certain amount of time
        if getattr(self, attr):
            setattr(self, attr, debff)
            setattr(self, attr+"_debuffed", True)
            setattr(self, attr+"_cooldown", time)
    
    def deal_damage(self, damage):
        # Reduces the character's health based on the damage received
        self.health -= damage * self.armor

    def draw(self, screen):
        # Placeholder method for drawing the character on the screen (not implemented)
        pass
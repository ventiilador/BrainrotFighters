from random import randint
import pygame
from characters.Character import Character
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
from characters.Projectile import Proyectile

class Bombardiro(Character):
    def __init__(self, fight, controls, pos):
        self.sprite_size = size(25, 20)

        # Load profile image for the character
        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/bombardiro_crocodilo/marco_bombardiro.png").convert_alpha(), size(7, 12))

        # Load images for the character's skills
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/bombardiro_crocodilo/bombardiro_basic_skill_image.png"), size(7, 10))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/bombardiro_crocodilo/bombardiro_elemental_skill_image.png"), size(7, 10))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/bombardiro_crocodilo/bombardiro_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites for walking animations
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_left_{}.png", 2, self.sprite_size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_right_{}.png", 2, self.sprite_size)
        
        # Load idle animations (left and right)
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_idle_left_{}.png", 2, self.sprite_size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_idle_right_{}.png", 2, self.sprite_size)
        
        # Load skill animations (left and right)
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_basic_skill_left_{}.png", 3, self.sprite_size
        )
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/bombardiro_crocodilo/bombardiro_basic_skill_right_{}.png", 3, self.sprite_size
        )
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

        # Initialize sprite indices
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Set hitbox size for the character
        self.size = size(20, 15)
        super().__init__(fight, controls, pos)

        # Load sounds for the character's skills
        self.fight.game.sound_manager.load_sound("BombardiroExplosion", "assets/sounds/bombardiro_missile_explosion.mp3")
        self.fight.game.sound_manager.load_sound("BombardiroLaunch", "assets/sounds/bombardiro_missile_launch.mp3")

        # Initialize basic skill properties
        self.missile = None
        self.basic_skill_damage = 5

        # Initialize elemental skill properties
        self.fly_time = 7
        self.flying_time = 0
        self.can_fly = False
        self.y_fly_velocity = 500
        self.elemental_skill_cooldown = 17000

        # Initialize ultimate skill properties
        self.missiles = []
        self.ultimate_skill_cooldown = 20000
        self.ultimate_skill_damage = 4

        # Initialize cooldowns
        current_time = pygame.time.get_ticks()
        self.basic_skill_last_time = current_time - self.basic_skill_cooldown
        self.elemental_skill_last_time = current_time - self.elemental_skill_cooldown
        self.ultimate_skill_last_time = current_time - self.ultimate_skill_cooldown

        # Set initial sprite to walking left
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]

    def manage_events(self, dt):
        # Handles key events and updates the character's state accordingly
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Jump or fly based on control inputs
        if keys[self.controls[0]]:
            if self.rect.bottom >= self.ground_y and not self.can_fly:
                self.y_velocity = self.jump_strength
            elif self.can_fly:
                self.rect.y -= self.y_fly_velocity * dt

        # Move left and animate accordingly
        if keys[self.controls[1]] and not keys[self.controls[3]]:
            if self.rect.left >= 0:
                self.rect.x -= self.x_velocity * dt
            self.last_direction = "left"
            self.left_animation()
        
        # Fly down
        if keys[self.controls[2]]:
            if self.can_fly:
                self.rect.y += self.y_fly_velocity * dt

        # Move right and animate accordingly
        if keys[self.controls[3]] and not keys[self.controls[1]]:
            if self.rect.right <= position_x(100):
                self.rect.x += self.x_velocity * dt
            self.last_direction = "right"
            self.right_animation()

        # Use basic skill if the conditions are met
        if keys[self.controls[4]] and current_time - self.basic_skill_last_time > self.basic_skill_cooldown and not (self.doing_elemental_skill or self.doing_ultimate_skill):
            self.doing_basic_skill = True
            self.basic_skill_last_time = current_time
            self.basic_skill()
        self.skill("basic_skill")

        # Use elemental skill if the conditions are met
        if keys[self.controls[5]]: 
            if current_time - self.elemental_skill_last_time > self.elemental_skill_cooldown and not (self.doing_basic_skill or self.doing_ultimate_skill):
                self.doing_elemental_skill = True
                self.elemental_skill_last_time = current_time
                self.elemental_skill()
        self.skill("elemental_skill")

        # Use ultimate skill if the conditions are met
        if keys[self.controls[6]] and current_time - self.ultimate_skill_last_time > self.ultimate_skill_cooldown and not (self.doing_basic_skill or self.doing_elemental_skill):
            self.doing_ultimate_skill = True
            self.ultimate_skill_last_time = current_time
            self.ultimate_skill()
        self.skill("ultimate_skill")
        
        # Set idle animation if no movement and no skills are active
        if (self.rect.bottom >= self.ground_y and not keys[self.controls[1]] and not keys[self.controls[3]] and
             not self.doing_basic_skill and not self.doing_elemental_skill and not self.doing_ultimate_skill):
            self.idle_animation()

        # Apply gravity if the character is not flying
        if (self.rect.bottom < self.ground_y or self.y_velocity < 0) and not self.can_fly:
            self.y_velocity += self.gravity * dt
            self.rect.y += self.y_velocity * dt

        # Prevent the character from going below the ground
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.y_velocity = 0
        
        # Handle debuff for horizontal movement speed
        if self.x_velocity_debuffed:
            self.x_velocity_debuffed_time += dt
            if self.x_velocity_debuffed_time >= self.x_velocity_cooldown:
                self.x_velocity_debuffed = False
                self.x_velocity_debuffed_time = 0
                self.x_velocity = 800
        
        # Handle flying time for the elemental skill
        if self.can_fly:
            self.flying_time += dt
            if self.flying_time >= self.fly_time:
                self.can_fly = False
                self.flying_time = 0

        # Move the missile if it is active
        if self.missile:
            if self.missile.status:
                self.missile.move(dt)

        # Move the missiles if they are active
        if self.missiles:
            for missile in self.missiles:
                if missile.status:
                    missile.move(dt)

            self.missiles = [missile for missile in self.missiles if missile.status]

    def basic_skill(self):
        # Launch the basic skill missile
        self.fight.game.sound_manager.play_sound("BombardiroLaunch")
        self.missile = Proyectile(self.rect.center, size(15, 15), size(7, 7), 1000, 3, self.enemy, damage=self.basic_skill_damage, 
                                   animation_path="assets/images/fight/bombardiro_crocodilo/missile_{}.png", animation_cooldown=200,
                                     sprites_count=4, rotate=True, collision_sound="BombardiroExplosion", sound_manager=self.fight.game.sound_manager)
    
    def elemental_skill(self):
        # Activate flying for the elemental skill
        self.can_fly = True
        self.fight.game.sound_manager.play_sound("BombardiroLaunch")
    
    def ultimate_skill(self):
        # Launch multiple missiles for the ultimate skill
        pos = [0, 0]
        missiles_num = randint(5, 10)
        for i in range(missiles_num):
            self.fight.game.sound_manager.play_sound("BombardiroLaunch")
            missile = Proyectile(pos, size(15, 15), size(7, 7), 500, 2, self.enemy, damage=self.ultimate_skill_damage, 
                                   animation_path="assets/images/fight/bombardiro_crocodilo/missile_{}.png", animation_cooldown=200,
                                     sprites_count=4, rotate=True, collision_sound="BombardiroExplosion", sound_manager=self.fight.game.sound_manager)
            self.missiles.append(missile)
            pos[0] += position_x(100) // missiles_num

    def draw(self, screen):
        # Draw the current sprite and the active missiles on the screen
        img_rect = self.current_sprite.get_rect()
        img_rect.center = self.rect.center
        screen.blit(self.current_sprite, img_rect)
        if self.missile:
            if self.missile.status:
                self.missile.draw(screen)
        if self.missiles:
            for missile in self.missiles:
                if missile.status:
                    missile.draw(screen)
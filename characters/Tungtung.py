import pygame
from characters.Character import Character
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
from characters.Projectile import Proyectile

class TungTung(Character):
    def __init__(self, fight, controls, pos):
        self.sprite_size = size(20, 25)  # Set sprite size for the character

        # Profile image and skills' images (scaled)
        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/tungtung_sahur/marco_tungtung.png").convert_alpha(), size(7, 12))
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tungtung_sahur/tung_tung_basic_skill_image.png"), size(7, 10))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_image.png"), size(7, 10))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tungtung_sahur/tung_tung_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites for different actions (walking, idle, skills)
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_left_{}.png", 5, self.sprite_size)  # Walking left
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_right_{}.png", 5, self.sprite_size)  # Walking right
        
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_idle_left_{}.png", 3, self.sprite_size)  # Idle left
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_idle_right_{}.png", 3, self.sprite_size)  # Idle right
        
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_basic_skill_left_{}.png", 3, self.sprite_size)  # Basic skill left
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_basic_skill_right_{}.png", 3, self.sprite_size)  # Basic skill right

        # Elemental and ultimate skill animations
        self.elemental_skill_left_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_left_{}.png", 4, self.sprite_size)  # Elemental skill left
        self.elemental_skill_right_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_right_{}.png", 4, self.sprite_size)  # Elemental skill right
        
        self.ultimate_skill_left_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_left_{}.png", 4, self.sprite_size)  # Ultimate skill left
        self.ultimate_skill_right_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_right_{}.png", 4, self.sprite_size)  # Ultimate skill right

        # Indexes to track which sprite is currently being used
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Character hitbox size
        self.size = size(7, 20)
        super().__init__(fight, controls, pos)  # Initialize the parent class (Character)

        # Load sound effects for various actions
        self.fight.game.sound_manager.load_sound("TungTungHit", "assets/sounds/tung_tung_hit.mp3")  # Hit sound
        self.fight.game.sound_manager.load_sound("TungTungUlti", "assets/sounds/tung_tung_ulti.mp3")  # Ultimate skill sound
        self.fight.game.sound_manager.load_sound("TungTungLaunch", "assets/sounds/bombardiro_missile_launch.mp3")  # Launch sound
        self.fight.game.sound_manager.load_sound("TungTungExplosion", "assets/sounds/bombardiro_missile_explosion.mp3")  # Explosion sound

        # Initialize skills
        self.stick = None  # Stick for elemental skill
        self.elemental_skill_cooldown = 2000  # Cooldown for elemental skill

        # Ultimate skill setup
        self.spin_time = 7  # Time for ultimate skill
        self.spinning = False  # Flag for when the character is spinning
        self.spinning_time = 0  # Time tracking for spinning
        self.last_spin_damage_tick = 0  # Last time damage was dealt during spin
        self.ultimate_skill_damage = 5  # Damage for the ultimate skill
        self.ultimate_skill_cooldown = 20000  # Cooldown for ultimate skill
        self.ultimate_angle = 0  # Angle for ultimate skill spinning effect
        self.spinning_speed = 1000  # Speed of spinning

        # Set the initial time for skills
        current_time = pygame.time.get_ticks()
        self.basic_skill_last_time = current_time - self.basic_skill_cooldown
        self.elemental_skill_last_time = current_time - self.elemental_skill_cooldown
        self.ultimate_skill_last_time = current_time - self.ultimate_skill_cooldown

        # Set the initial sprite for the character (facing left)
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]

    def manage_events(self, dt):
        super().manage_events(dt)  # Call the parent class method for event management
        current_time = pygame.time.get_ticks()

        # Handle elemental skill (if active, move the stick)
        if self.stick:
            if self.stick.status:
                self.stick.move(dt)  # Move the stick
            else:
                self.stick = None  # If the stick is no longer active, remove it
        
        # Handle ultimate skill (spinning)
        if self.spinning:
            self.spinning_time += dt  # Increment spinning time
            self.ultimate_angle += self.spinning_speed * dt  # Increment angle of spinning
            if self.spinning_time >= self.spin_time:  # If the spin time is over, stop spinning
                self.spinning = False
                self.spinning_time = 0
            elif self.rect.colliderect(self.enemy.rect) and current_time - self.last_spin_damage_tick >= 300:  # Deal damage when colliding with enemy
                self.enemy.deal_damage(self.ultimate_skill_damage)
                self.last_spin_damage_tick = current_time

    def basic_skill(self):
        if self.rect.colliderect(self.enemy.rect):  # Check if the basic skill hits the enemy
            self.enemy.deal_damage(self.basic_skill_damage)
        self.fight.game.sound_manager.play_sound("TungTungHit")  # Play sound for basic skill

    def elemental_skill(self):
        pos = list(self.rect.center)  # Get the character's current position
        pos[1] -= position_y(10)  # Adjust position for projectile
        self.stick = Proyectile(pos, size(10, 15), size(6, 6), 600, 3, self.enemy, damage=self.elemental_skill_damage, 
                    animation_path="assets/images/fight/tungtung_sahur/stick_{}.png", animation_cooldown=100, sprites_count=3, rotate=True,
                    collision_sound="TungTungExplosion", sound_manager=self.fight.game.sound_manager)  # Launch elemental skill projectile
        self.fight.game.sound_manager.play_sound("TungTungLaunch")  # Play launch sound

    def ultimate_skill(self):
        self.spinning = True  # Start spinning for ultimate skill
        self.fight.game.sound_manager.play_sound("TungTungUlti")  # Play ultimate skill sound

    def draw(self, screen):
        if self.stick:  # If elemental skill is active, draw the stick
            if self.stick.status:
                self.stick.draw(screen)
        
        if self.spinning:  # If ultimate skill is active (spinning), rotate and draw the sprite
            rotated_image = pygame.transform.rotate(self.current_sprite, self.ultimate_angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, rotated_rect)  # Draw the rotated sprite
        else:  # If not spinning, draw the current sprite in the character's position
            img_rect = self.current_sprite.get_rect()
            img_rect.center = self.rect.center
            screen.blit(self.current_sprite, img_rect)
import pygame
import math
from functions import size, position, load_sprites, size_x, size_y
from characters.Character import Character

class Proyectile:
    def __init__(self, position, sprite_size, rect_size, speed, lifetime, 
                 enemy, objective=None, damage=0, debuff=(), animation_path=None, 
                 animation_cooldown=0, sprites_count=0, rotate=False, collision_sound=None, sound_manager=None):
        # Initialize projectile with all the parameters
        self.speed = speed  # Speed of the projectile
        self.objective = objective  # Objective position for the projectile to move towards
        self.enemy = enemy  # The enemy character that the projectile may collide with
        self.damage = damage  # Damage that the projectile will deal
        self.debuff_args = debuff  # Debuff effect that the projectile may apply on the enemy
        self.lifetime = lifetime  # How long the projectile will exist before disappearing
        self.time = 0  # Time that the projectile has been alive
        self.rotate = rotate  # Whether the projectile should rotate towards its movement direction
        self.animation_sprites = load_sprites(animation_path, sprites_count, sprite_size)  # Load animation sprites
        self.current_animation_sprite = 0  # Index of the current sprite being displayed
        self.rect = pygame.rect.Rect(position[0], position[1], rect_size[0], rect_size[1])  # Define the rectangle for the projectile's hitbox
        self.rect.center = position  # Set the center of the hitbox at the initial position
        self.last_animation_time = 0  # Keep track of the last animation time
        self.animation_cooldown = animation_cooldown  # Cooldown between sprite animations
        self.status = True  # Whether the projectile is still active or not
        self.angle = 0  # The angle at which the projectile is rotated (if applicable)
        self.collision_sound = collision_sound  # Sound that plays when the projectile collides with something
        self.sound_manager = sound_manager  # Sound manager to handle sounds
    
    def move(self, dt):
        # Function to handle the movement of the projectile over time (dt = delta time)
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        self.time += dt  # Increase the projectile's lifetime
        if self.time >= self.lifetime:
            self.status = False  # Deactivate the projectile when it exceeds its lifetime
            return

        # If the projectile collides with the enemy, deal damage and apply debuff
        if self.rect.colliderect(self.enemy.rect):
            self.enemy.deal_damage(self.damage)  # Deal damage to the enemy
            if self.debuff_args:
                self.enemy.debuff(*self.debuff_args)  # Apply debuff if any
            if self.collision_sound and self.sound_manager:
                self.sound_manager.play_sound(self.collision_sound)  # Play collision sound
            self.status = False  # Deactivate the projectile after collision
            return

        # If there is an objective, move towards it
        if self.objective:
            dx = self.objective[0] - self.rect.centerx  # X difference between objective and current position
            dy = self.objective[1] - self.rect.centery  # Y difference between objective and current position
            if self.rect.collidepoint(self.objective):  # If the projectile reaches the objective
                self.status = False  # Deactivate the projectile
                return
        else:
            # Otherwise, move towards the enemy
            dx = self.enemy.rect.centerx - self.rect.centerx  # X difference between enemy and current position
            dy = self.enemy.rect.centery - self.rect.centery  # Y difference between enemy and current position

        # Calculate the distance and normalize the direction
        length = (dx**2 + dy**2)**0.5  # Calculate the length of the vector (dx, dy)
        if length != 0:  # Avoid division by zero
            dx /= length  # Normalize the x direction
            dy /= length  # Normalize the y direction
            if self.rotate:
                self.angle = math.degrees(math.atan2(-dx, -dy))  # Calculate the angle for rotation if needed
        else:
            self.angle = 0  # If there's no movement, set angle to 0

        # Move the projectile in the direction towards the enemy or objective
        self.rect.x += dx * self.speed * dt  # Move in the x direction
        self.rect.y += dy * self.speed * dt  # Move in the y direction

        # Handle sprite animation (change sprites at the right time)
        if current_time - self.last_animation_time >= self.animation_cooldown:
            self.last_animation_time = current_time  # Update the last animation time
            if self.current_animation_sprite >= len(self.animation_sprites) - 1:
                self.current_animation_sprite = 0  # Loop back to the first sprite if all have been displayed
            else:
                self.current_animation_sprite += 1  # Move to the next sprite
    
    def draw(self, screen):
        # Function to draw the projectile on the screen
        if self.rotate:
            # If the projectile rotates, rotate the current sprite and draw it
            rotated_image = pygame.transform.rotate(self.animation_sprites[self.current_animation_sprite], self.angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)  # Adjust the position of the rotated image
            screen.blit(rotated_image, rotated_rect)  # Draw the rotated image on the screen
        else:
            # If the projectile doesn't rotate, simply draw the sprite as it is
            img_rect = self.animation_sprites[self.current_animation_sprite].get_rect(center=self.rect.center)
            screen.blit(self.animation_sprites[self.current_animation_sprite], img_rect)  # Draw the sprite on the screen
import pygame
import math
from functions import size, position, load_sprites, size_x, size_y
from characters.Character import Character

class Proyectile:
    def __init__(self, position, sprite_size, rect_size, speed, lifetime, 
    enemy, objective=None, damage=0, debuff=(), animation_path=None, animation_cooldown=0, sprites_count=0, rotate=False):
        self.speed = speed
        self.objective = objective
        self.enemy = enemy
        self.damage = damage
        self.debuff_args = debuff
        self.lifetime = lifetime
        self.time = 0
        self.rotate = rotate
        self.animation_sprites = load_sprites(animation_path, sprites_count, sprite_size)
        self.current_animation_sprite = 0
        self.rect = pygame.rect.Rect(position[0], position[1], rect_size[0], rect_size[1])
        self.rect.center = position
        self.last_animation_time = 0
        self.animation_cooldown = animation_cooldown
        self.status = True
    
    def move(self, dt):
        current_time = pygame.time.get_ticks()
        self.time += dt
        if self.time >= self.lifetime:
            self.status = False
            return

        if self.rect.colliderect(self.enemy.rect):
            self.enemy.health -= self.damage
            if self.debuff_args:
                self.enemy.debuff(*self.debuff_args)
            self.status = False
            return

        if self.objective:
            dx = self.objective[0] - self.rect.centerx
            dy = self.objective[1] - self.rect.centery
            if self.rect.collidepoint(self.objective):
                self.status = False
                return
        else:
            dx = self.enemy.rect.centerx - self.rect.centerx
            dy = self.enemy.rect.centery - self.rect.centery

        length = (dx**2 + dy**2)**0.5
        if length != 0:
            dx /= length
            dy /= length
            if self.rotate:
                self.angle = math.degrees(math.atan2(-dx, -dy))
        else:
            self.angle = 0
        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt

        if current_time - self.last_animation_time >= self.animation_cooldown:
            self.last_animation_time = current_time
            if self.current_animation_sprite >= len(self.animation_sprites) - 1:
                self.current_animation_sprite = 0
            else:
                self.current_animation_sprite += 1
    
    def draw(self, screen):
        if self.rotate:
            rotated_image = pygame.transform.rotate(self.animation_sprites[self.current_animation_sprite], self.angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, rotated_rect)
        else:
            img_rect = self.animation_sprites[self.current_animation_sprite].get_rect(center=self.rect.center)
            screen.blit(self.animation_sprites[self.current_animation_sprite], img_rect)
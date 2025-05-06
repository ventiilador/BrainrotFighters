import pygame
from characters.Character import Character
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
from characters.Projectile import Proyectile

class TungTung(Character):
    def __init__(self, fight, controls, pos):
        self.sprite_size = size(20, 25)

        # ASIGNARRRR!!!
        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/tungtung_sahur/marco_tungtung.png").convert_alpha(), size(7, 12))
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tungtung_sahur/tung_tung_basic_skill_image.png"), size(7, 10))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_image.png"), size(7, 10))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tungtung_sahur/tung_tung_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_left_{}.png", 5, self.sprite_size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_right_{}.png", 5, self.sprite_size)
        
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_idle_left_{}.png", 3, self.sprite_size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_idle_right_{}.png", 3, self.sprite_size)
        
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_basic_skill_left_{}.png", 3, self.sprite_size
        )
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_basic_skill_right_{}.png", 3, self.sprite_size
        )
        # ASIGNAR SUS SPRITES
        self.elemental_skill_left_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_left_{}.png", 4, self.sprite_size
        )
        self.elemental_skill_right_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_right_{}.png", 4, self.sprite_size
        )
        self.ultimate_skill_left_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_left_{}.png", 4, self.sprite_size
        )
        self.ultimate_skill_right_animation = load_sprites(
            "assets/images/fight/tungtung_sahur/tung_tung_elemental_skill_right_{}.png", 4, self.sprite_size
        )

        # Indexs
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Hitbox_size
        self.size = size(7, 20)
        super().__init__(fight, controls, pos)

        # Sounds
        self.fight.game.sound_manager.load_sound("TungTungHit", "assets/sounds/tung_tung_hit.mp3")
        self.fight.game.sound_manager.load_sound("TungTungUlti", "assets/sounds/tung_tung_ulti.mp3")
        self.fight.game.sound_manager.load_sound("TungTungLaunch", "assets/sounds/bombardiro_missile_launch.mp3")
        self.fight.game.sound_manager.load_sound("TungTungExplosion", "assets/sounds/bombardiro_missile_explosion.mp3")

        # Basic skill

        # Elemental skill
        self.stick = None
        self.elemental_skill_cooldown = 2000

        # Ultimate skill
        self.spin_time = 7
        self.spinning = False
        self.spinning_time = 0
        self.last_spin_damage_tick = 0
        self.ultimate_skill_damage = 5
        self.ultimate_skill_cooldown = 20000
        self.ultimate_angle = 0
        self.spinning_speed = 1000

        # 0 cooldowns
        current_time = pygame.time.get_ticks()
        self.basic_skill_last_time = current_time - self.basic_skill_cooldown
        self.elemental_skill_last_time = current_time - self.elemental_skill_cooldown
        self.ultimate_skill_last_time = current_time - self.ultimate_skill_cooldown

        # Set initial sprite
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]

    def manage_events(self, dt):
        super().manage_events(dt)
        current_time = pygame.time.get_ticks()

        if self.stick:
            if self.stick.status:
                self.stick.move(dt)
            else:
                self.stick = None
        
        if self.spinning:
            self.spinning_time += dt
            self.ultimate_angle += self.spinning_speed * dt
            if self.spinning_time >= self.spin_time:
                self.spinning = False
                self.spinning_time = 0
            elif self.rect.colliderect(self.enemy.rect) and current_time - self.last_spin_damage_tick >= 300:
                self.enemy.deal_damage(self.ultimate_skill_damage)
                self.last_spin_damage_tick = current_time

    def basic_skill(self):
        if self.rect.colliderect(self.enemy.rect):
            self.enemy.deal_damage(self.basic_skill_damage)
        self.fight.game.sound_manager.play_sound("TungTungHit")
    
    def elemental_skill(self):
        pos = list(self.rect.center)
        pos[1] -= position_y(10)
        self.stick = Proyectile(pos, size(10, 15), size(6, 6), 600, 3, self.enemy, damage=self.elemental_skill_damage, 
                    animation_path="assets/images/fight/tungtung_sahur/stick_{}.png", animation_cooldown=100, sprites_count=3, rotate=True,
                    collision_sound="TungTungExplosion", sound_manager= self.fight.game.sound_manager)
        self.fight.game.sound_manager.play_sound("TungTungLaunch")
    
    def ultimate_skill(self):
        self.spinning = True
        self.fight.game.sound_manager.play_sound("TungTungUlti")

    def draw(self, screen):
        if self.stick:
            if self.stick.status:
                self.stick.draw(screen)
        if self.spinning:
            rotated_image = pygame.transform.rotate(self.current_sprite, self.ultimate_angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, rotated_rect)
        else:
            img_rect = self.current_sprite.get_rect()
            img_rect.center = self.rect.center
            screen.blit(self.current_sprite, img_rect)
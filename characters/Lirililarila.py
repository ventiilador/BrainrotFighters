import pygame
from characters.Character import Character
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
from characters.Projectile import Proyectile

class Lirililarila(Character):
    def __init__(self, fight, controls, pos):
        self.sprite_size = size(25, 35)

        # ASIGNARRRR!!!
        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/lirili_larila/marco_lirili_larila.png"), size(7, 12))
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/lirili_larila/lirili_larila_basic_skill_image.png"), size(7, 10))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/lirili_larila/lirili_larila_elemental_skill_image.png"), size(7, 10))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/lirili_larila/lirili_larila_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_left_{}.png", 3, self.sprite_size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_right_{}.png", 3, self.sprite_size)
        
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_idle_left_{}.png", 3, self.sprite_size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_idle_right_{}.png", 3, self.sprite_size)
        
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_left_{}.png", 3, self.sprite_size
        )
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_right_{}.png", 3, self.sprite_size
        )
        # ASIGNAR SUS SPRITES
        self.elemental_skill_left_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_left_{}.png", 3, self.sprite_size
        )
        self.elemental_skill_right_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_right_{}.png", 3, self.sprite_size
        )
        self.ultimate_skill_left_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_left_{}.png", 3, self.sprite_size
        )
        self.ultimate_skill_right_animation = load_sprites(
            "assets/images/fight/lirili_larila/lirili_larila_elemental_skill_right_{}.png", 3, self.sprite_size
        )

        # Indexs
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Hitbox_size
        self.size = size(15, 20)
        super().__init__(fight, controls, pos)

        # Sounds
        self.fight.game.sound_manager.load_sound("LiriliLarilaPunch", "assets/sounds/lirili_larila_stand_punch.mp3")
        self.fight.game.sound_manager.load_sound("TomaApisonadora", "assets/sounds/toma_apisonadora.mp3")
        self.fight.game.sound_manager.load_sound("ExplosionApisonadora", "assets/sounds/bombardiro_missile_explosion.mp3")
        self.fight.game.sound_manager.load_sound("ZaWarudo", "assets/sounds/zawarudo.mp3")

        # Basic skill
        self.stand = None
        self.basic_skill_cooldown = 7000
        self.basic_skill_damage = 10

        # Elemental skill
        self.apisonadora = None
        self.elemental_skill_update_time = 700
        self.elemental_skill_cooldown = 5000
        self.elemental_skill_damage = 15

        # Ultimate skill
        self.time_stop = 12
        self.elapsed_time_stop = 0
        self.ultimate_skill_cooldown = 30000

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

        if self.apisonadora:
            if self.apisonadora.status:
                self.apisonadora.move(dt)
            else:
                self.apisonadora = None
        
        if self.stand:
            if self.stand.status:
                self.stand.move(dt)

        if not self.fight.time_running:
            self.elapsed_time_stop += dt
            if self.elapsed_time_stop >= self.time_stop:
                self.fight.time_running = True
                self.elapsed_time_stop = 0

    def basic_skill(self):
        path = "assets/images/fight/lirili_larila/lirili_larila_stand_" + self.last_direction + "_{}.png"
        pos = (self.rect.center[0] + position_x(10), self.rect.center[1]) if self.last_direction == "left" else (self.rect.center[0] - position_x(10), self.rect.center[1])
        self.stand = Proyectile(pos, size(25, 30), size(15, 15), 200, 9, self.enemy, damage=self.basic_skill_damage, 
                                   animation_path=path, animation_cooldown=150, sprites_count=9, collision_sound="LiriliLarilaPunch",
                                     sound_manager=self.fight.game.sound_manager)

    def elemental_skill(self):
        self.apisonadora = Proyectile((0, 0), size(30, 35), size(20, 20), 500, 5, self.enemy, damage=self.elemental_skill_damage, 
                                   animation_path="assets/images/fight/lirili_larila/apisonadora_{}.png", animation_cooldown=200, sprites_count=1, rotate=True,
                                   collision_sound="ExplosionApisonadora", sound_manager=self.fight.game.sound_manager)
        self.fight.game.sound_manager.play_sound("TomaApisonadora")
    
    def ultimate_skill(self):
        self.fight.time_running = False
        self.fight.game.sound_manager.play_sound("ZaWarudo")

    def draw(self, screen):
        img_rect = self.current_sprite.get_rect()
        img_rect.center = self.rect.center
        screen.blit(self.current_sprite, img_rect)
        if self.apisonadora:
            if self.apisonadora.status:
                self.apisonadora.draw(screen)
        
        if self.stand:
            if self.stand.status:
                self.stand.draw(screen)
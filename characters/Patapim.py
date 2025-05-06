import pygame
from characters.Character import Character
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
from characters.Projectile import Proyectile

class Patapim(Character):
    def __init__(self, fight, controls, pos):
        self.sprite_size = size(25, 30)

        # ASIGNARRRR!!!
        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/brbr_patapim/marco_patapim.png").convert_alpha(), size(7, 12))
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/brbr_patapim/patapim_basic_skill_image.png"), size(6, 9))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/brbr_patapim/patapim_elemental_skill_image.png"), size(6, 9))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/brbr_patapim/patapim_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_left_{}.png", 3, self.sprite_size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_right_{}.png", 3, self.sprite_size)
        
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_idle_left_{}.png", 3, self.sprite_size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_idle_right_{}.png", 3, self.sprite_size)
        
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_basic_skill_left_{}.png", 6, self.sprite_size
        )
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_basic_skill_right_{}.png", 6, self.sprite_size
        )
        # ASIGNAR SUS SPRITES
        self.elemental_skill_left_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_elemental_skill_left_{}.png", 5, self.sprite_size
        )
        self.elemental_skill_right_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_elemental_skill_right_{}.png", 5, self.sprite_size
        )
        self.ultimate_skill_left_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_ultimate_skill_left_{}.png", 3, self.sprite_size
        )
        self.ultimate_skill_right_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_ultimate_skill_right_{}.png", 3, self.sprite_size
        )

        # Indexs
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Hitbox_size
        self.size = size(10, 25)
        super().__init__(fight, controls, pos)

        # Sounds
        self.fight.game.sound_manager.load_sound("PatapimBasicSkill", "assets/sounds/patapim_basic_skill.mp3")
        self.fight.game.sound_manager.load_sound("PatapimElementalSkill", "assets/sounds/patapim_elemental_skill.mp3")
        self.fight.game.sound_manager.load_sound("PatapimUltimateSkill", "assets/sounds/patapim_ultimate_skill.mp3")

        # Basic skill

        # Elemental skill
        self.liana = None

        # Ultimate skill
        self.ultimate_buff = False
        self.ultimate_armor_buff = 0.5
        self.ultimate_buff_time = 10
        self.buff_time_elapsed = 0
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
        if self.liana:
            if self.liana.status:
                self.liana.move(dt)
            else:
                self.liana = None
        
        if self.ultimate_buff:
            self.buff_time_elapsed += dt
            if self.buff_time_elapsed >= self.ultimate_buff_time:
                self.ultimate_buff = False
                self.buff_time_elapsed = 0
                self.armor = 1

    def basic_skill(self):
        if self.rect.colliderect(self.enemy.rect):
            self.enemy.deal_damage(self.basic_skill_damage)
        self.fight.game.sound_manager.play_sound("PatapimBasicSkill")

    def elemental_skill(self):
        objective = (self.rect.center[0] - position_x(40), self.rect.center[1]) if self.last_direction == "left" else (self.rect.center[0] + position_x(40), self.rect.center[1])
        self.liana = Proyectile(self.rect.center, size(15, 30), size(10, 20), 300, 6, self.enemy, objective=objective, damage=self.elemental_skill_damage,
                                debuff=("x_velocity", 200, 3), animation_path="assets/images/fight/brbr_patapim/lianas_{}.png",
                                sprites_count=2, animation_cooldown=300, rotate=True)
        self.fight.game.sound_manager.play_sound("PatapimElementalSkill")
    
    def ultimate_skill(self):
        self.ultimate_buff = True
        self.armor = self.ultimate_armor_buff
        self.fight.game.sound_manager.play_sound("PatapimUltimateSkill")

    def draw(self, screen):
        img_rect = self.current_sprite.get_rect()
        img_rect.center = self.rect.center
        screen.blit(self.current_sprite, img_rect)
        if self.liana:
            if self.liana.status:
                self.liana.draw(screen)
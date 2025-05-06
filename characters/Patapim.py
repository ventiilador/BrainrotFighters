import pygame
from characters.Character import Character
from functions import load_sprites, size, position, position_x, position_y, size_x, size_y
from characters.Projectile import Proyectile

class Patapim(Character):
    def __init__(self, fight, controls, pos):
        self.sprite_size = size(25, 30)  # Set the size of the sprites for the character

        # ASIGNARRRR!!! (Loading profile images for UI or selection screens)
        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/brbr_patapim/marco_patapim.png").convert_alpha(), size(7, 12))
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/brbr_patapim/patapim_basic_skill_image.png"), size(6, 9))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/brbr_patapim/patapim_elemental_skill_image.png"), size(6, 9))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/brbr_patapim/patapim_ultimate_skill_image.png"), size(7, 10))

        # Load character sprites for walking in different directions
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_left_{}.png", 3, self.sprite_size)  # Left walking animation
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_right_{}.png", 3, self.sprite_size)  # Right walking animation
        
        # Load idle sprites (when the character is not moving)
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_idle_left_{}.png", 3, self.sprite_size)  # Left idle animation
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_idle_right_{}.png", 3, self.sprite_size)  # Right idle animation
        
        # Load basic skill sprites (for both left and right directions)
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_basic_skill_left_{}.png", 6, self.sprite_size)
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_basic_skill_right_{}.png", 6, self.sprite_size)
        
        # Load elemental skill sprites
        self.elemental_skill_left_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_elemental_skill_left_{}.png", 5, self.sprite_size)
        self.elemental_skill_right_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_elemental_skill_right_{}.png", 5, self.sprite_size)
        
        # Load ultimate skill sprites
        self.ultimate_skill_left_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_ultimate_skill_left_{}.png", 3, self.sprite_size)
        self.ultimate_skill_right_animation = load_sprites(
            "assets/images/fight/brbr_patapim/patapim_ultimate_skill_right_{}.png", 3, self.sprite_size)

        # Indexes to track the current sprite during animations
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Character hitbox size
        self.size = size(10, 25)
        
        # Initialize the parent class (Character)
        super().__init__(fight, controls, pos)

        # Sounds for skills (loaded through sound manager)
        self.fight.game.sound_manager.load_sound("PatapimBasicSkill", "assets/sounds/patapim_basic_skill.mp3")
        self.fight.game.sound_manager.load_sound("PatapimElementalSkill", "assets/sounds/patapim_elemental_skill.mp3")
        self.fight.game.sound_manager.load_sound("PatapimUltimateSkill", "assets/sounds/patapim_ultimate_skill.mp3")

        # Basic skill (damage, effects are handled in the method)
        # Elemental skill
        self.liana = None  # Variable for elemental skill (liana projectile)
        
        # Ultimate skill
        self.ultimate_buff = False  # Buff status for ultimate skill
        self.ultimate_armor_buff = 0.5  # Armor increase when ultimate is activated
        self.ultimate_buff_time = 10  # Duration of the ultimate buff
        self.buff_time_elapsed = 0  # Timer for how long the buff has been active
        self.ultimate_skill_cooldown = 30000  # Cooldown in milliseconds for ultimate skill

        # 0 cooldowns for skills at the start
        current_time = pygame.time.get_ticks()
        self.basic_skill_last_time = current_time - self.basic_skill_cooldown
        self.elemental_skill_last_time = current_time - self.elemental_skill_cooldown
        self.ultimate_skill_last_time = current_time - self.ultimate_skill_cooldown

        # Set the initial sprite to be walking left
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]

    def manage_events(self, dt):
        # Handle events, including movement and skill management
        super().manage_events(dt)  # Call the parent class's manage_events method
        current_time = pygame.time.get_ticks()
        
        if self.liana:
            if self.liana.status:
                self.liana.move(dt)  # Move the elemental projectile (liana)
            else:
                self.liana = None  # Reset liana if it is no longer active
        
        if self.ultimate_buff:
            self.buff_time_elapsed += dt  # Track the elapsed time of the ultimate buff
            if self.buff_time_elapsed >= self.ultimate_buff_time:
                self.ultimate_buff = False  # Deactivate the buff after the duration
                self.buff_time_elapsed = 0
                self.armor = 1  # Reset the armor to normal

    def basic_skill(self):
        # Basic skill that deals damage to the enemy
        if self.rect.colliderect(self.enemy.rect):  # Check for collision with enemy
            self.enemy.deal_damage(self.basic_skill_damage)  # Deal basic skill damage
        self.fight.game.sound_manager.play_sound("PatapimBasicSkill")  # Play sound for basic skill

    def elemental_skill(self):
        # Elemental skill that creates a liana projectile
        objective = (self.rect.center[0] - position_x(40), self.rect.center[1]) if self.last_direction == "left" else (self.rect.center[0] + position_x(40), self.rect.center[1])
        self.liana = Proyectile(self.rect.center, size(15, 30), size(10, 20), 300, 6, self.enemy, objective=objective, damage=self.elemental_skill_damage,
                                debuff=("x_velocity", 200, 3), animation_path="assets/images/fight/brbr_patapim/lianas_{}.png",
                                sprites_count=2, animation_cooldown=300, rotate=True)
        self.fight.game.sound_manager.play_sound("PatapimElementalSkill")  # Play sound for elemental skill
    
    def ultimate_skill(self):
        # Activate the ultimate skill, applying armor buff
        self.ultimate_buff = True
        self.armor = self.ultimate_armor_buff  # Apply armor buff from ultimate skill
        self.fight.game.sound_manager.play_sound("PatapimUltimateSkill")  # Play sound for ultimate skill

    def draw(self, screen):
        # Draw the character's sprite and elemental projectile if active
        img_rect = self.current_sprite.get_rect()
        img_rect.center = self.rect.center  # Position the sprite at the character's center
        screen.blit(self.current_sprite, img_rect)  # Draw the character's sprite

        # If the elemental skill (liana) is active, draw it too
        if self.liana:
            if self.liana.status:
                self.liana.draw(screen)  # Draw the liana projectile if it's still active
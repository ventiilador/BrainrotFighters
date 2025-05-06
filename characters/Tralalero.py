import pygame
from characters.Character import Character
from characters.Projectile import Proyectile
from functions import load_sprites, size, position_x, position_y
from random import randint

class Tralalero(Character):
    def __init__(self, fight, controls, pos):
        self.sprite_size = size(20, 25)  # Set sprite size for Tralalero

        """
        Here we load assets and components / control
        """

        # Load profile image and resize it
        self.profile_image = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/marco_tralalalero.png").convert_alpha(), size(7, 12))
        
        # Load images for each skill and resize
        self.basic_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/tralalero_basic_skill_image.png"), size(7, 10))
        self.elemental_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/tralalero_elemental_skill_image.png"), size(7, 10))
        self.ultimate_skill_img = pygame.transform.scale(pygame.image.load("assets/images/fight/tralalero_tralala/tralalero_ultimate_skill_image.png"), size(7, 10))

        # Load walking animations for both left and right directions
        self.left_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_left_{}.png", 3, self.sprite_size)
        self.right_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_right_{}.png", 3, self.sprite_size)
        
        # Load idle animations for both left and right directions
        self.idle_left_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_idle_left_{}.png", 2, self.sprite_size)
        self.idle_right_animation_sprites = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_idle_right_{}.png", 2, self.sprite_size)
        
        # Load basic skill animations for both directions
        self.basic_skill_left_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_basic_skill_left_{}.png", 4, self.sprite_size
        )
        self.basic_skill_right_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_basic_skill_right_{}.png", 4, self.sprite_size
        )
        
        # Load elemental skill animations for both directions
        self.elemental_skill_left_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_elemental_skill_left_{}.png", 5, self.sprite_size
        )
        self.elemental_skill_right_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_elemental_skill_right_{}.png", 5, self.sprite_size
        )

        # Load ultimate skill animations for both directions
        self.ultimate_skill_left_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_elemental_skill_left_{}.png", 5, self.sprite_size
        )
        self.ultimate_skill_right_animation = load_sprites(
            "assets/images/fight/tralalero_tralala/tralalero_elemental_skill_right_{}.png", 5, self.sprite_size
        )

        # Initialize animation indices
        self.current_walk_sprite = 0
        self.current_idle_sprite = 0
        self.current_basic_skill_sprite = 0
        self.current_elemental_skill_sprite = 0
        self.current_ultimate_skill_sprite = 0

        # Set hitbox size for the character
        self.size = size(10, 15)
        super().__init__(fight, controls, pos)

        # Load sound effects for various skills
        self.fight.game.sound_manager.load_sound("TralaleroBite", "assets/sounds/tralalero_bite.mp3")
        self.fight.game.sound_manager.load_sound("TralaleroBubbles", "assets/sounds/tralalero_bubbles.mp3")
        self.fight.game.sound_manager.load_sound("TralaleroWave", "assets/sounds/tralalero_wave.mp3")
        
        # Elemental skill setup (bubbles)
        self.bubbles = []  # List of active bubbles
        self.elemental_skill_damage = 5  # Set elemental skill damage

        # Ultimate skill setup (wave)
        self.wave = None  # Will hold the wave projectile instance
        self.ultimate_skill_damage = 20  # Set ultimate skill damage

        # Initialize cooldown timers
        current_time = pygame.time.get_ticks()
        self.basic_skill_last_time = current_time - self.basic_skill_cooldown
        self.elemental_skill_last_time = current_time - self.elemental_skill_cooldown
        self.ultimate_skill_last_time = current_time - self.ultimate_skill_cooldown

        # Set initial sprite
        self.current_sprite = self.left_animation_sprites[self.current_walk_sprite]
    
    def manage_events(self, dt):
        super().manage_events(dt)
        
        # Update each active bubble in the list
        for bubble in self.bubbles:
            if bubble.status:
                bubble.move(dt)

        # Remove bubbles that are no longer active
        self.bubbles = [b for b in self.bubbles if b.status]

        # If wave is active, move it
        if self.wave:
            if self.wave.status:
                self.wave.move(dt)
            else:
                self.wave = None  # Remove wave when it's inactive
    
    def basic_skill(self):
        # If Tralalero's hitbox collides with the enemy's hitbox, deal damage
        if self.rect.colliderect(self.enemy.rect):
            self.enemy.deal_damage(self.basic_skill_damage)
        # Play the sound for basic skill
        self.fight.game.sound_manager.play_sound("TralaleroBite")
    
    def elemental_skill(self):
        # Create a random number of bubble projectiles within a range around Tralalero
        for i in range(randint(2, 4)):
            bubble = Proyectile(
                (randint(self.rect.center[0] - position_x(5), self.rect.center[0] + position_x(5)), 
                 randint(self.rect.center[1] - position_y(5), self.rect.center[1] + position_y(5))),
                size(3, 5), size(3, 4), 300, 4, self.enemy, damage=self.elemental_skill_damage,
                animation_path="assets/images/fight/tralalero_tralala/bubble_{}.png", animation_cooldown=200, sprites_count=1
            )
            self.bubbles.append(bubble)  # Add the bubble to the list of active bubbles
        # Play the sound for elemental skill
        self.fight.game.sound_manager.play_sound("TralaleroBubbles")
    
    def ultimate_skill(self):
        # Set objective for wave projectile based on Tralalero's facing direction
        objective = (self.rect.center[0] - position_x(55), self.rect.center[1]) if self.last_direction == "left" else (self.rect.center[0] + position_x(55), self.rect.center[1])
        
        # Create wave projectile
        self.wave = Proyectile(
            self.rect.topleft, size(20, 25), size(16, 23), 300, 10, self.enemy, 
            damage=self.ultimate_skill_damage, debuff=("x_velocity", 400, 3), objective=objective,
            animation_path="assets/images/fight/tralalero_tralala/"+self.last_direction+"_wave_{}.png", 
            animation_cooldown=500, sprites_count=3
        )
        # Play the sound for ultimate skill
        self.fight.game.sound_manager.play_sound("TralaleroWave")

    def draw(self, screen):
        # Draw the current sprite at the character's position
        img_rect = self.current_sprite.get_rect()
        img_rect.center = self.rect.center
        screen.blit(self.current_sprite, img_rect)
        
        # Draw all active bubbles
        for bubble in self.bubbles:
            if bubble.status:
                bubble.draw(screen)
        
        # Draw the wave if it's active
        if self.wave:
            if self.wave.status:
                self.wave.draw(screen)
import pygame

class CharacterSelector:
    def __init__(self, game, position:tuple, size:tuple, rows, columns):
        self.game = game
        self.rect = pygame.rect.Rect(0, 0, size[0], size[1])
        self.rect.center = position
        self.slot_size = (size[0] // columns, size[1] // rows)
        self.slots = []
        self.characters = [[pygame.transform.scale(pygame.image.load("assets/images/character_selection/bombardiro_crocodilo.jpg"), self.slot_size), "bombardiro"], [pygame.transform.scale(pygame.image.load("assets/images/character_selection/br_patapim.jpg"), self.slot_size), "patapim"],
                    [pygame.transform.scale(pygame.image.load("assets/images/character_selection/tralalero_tralala.jpg"), self.slot_size), "tralalero"], [pygame.transform.scale(pygame.image.load("assets/images/character_selection/tum_sahur.jpeg"), self.slot_size), "sahur"]]
        counter = 0
        for row in range(rows):
            for column in range(columns):
                slot = pygame.rect.Rect(self.rect.left + self.slot_size[0] * column,
                                              self.rect.top + self.slot_size[1] * row, self.slot_size[0], self.slot_size[1])
                self.slots.append([slot, self.characters[counter]]) if counter < len(self.characters) else self.slots.append([slot])
                counter += 1
        
        self.cursor = pygame.transform.scale(pygame.image.load("assets/images/character_selection/cursor.png"), self.slot_size)
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_rect.center = self.slots[0][0].center
        self.last_time = 0
        self.game.sound_manager.load_sound("Switch", "assets/sounds/Switch.wav")
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255,180,0), self.rect.inflate(20, 20))
        for slot in self.slots:
            pygame.draw.rect(screen, (255,180,0), slot[0])
            if len(slot) > 1:
                screen.blit(slot[1][0], slot[0])
        screen.blit(self.cursor, self.cursor_rect)
    
    def check_input(self):
        pass

class CharacterSelectorWASD(CharacterSelector):
    def __init__(self, game, position, size, rows, columns):
        super().__init__(game, position, size, rows, columns)
    
    def check_input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_w] and self.cursor_rect.center[1] - self.slot_size[1] >= self.rect.top and current_time - self.last_time > 200:
            self.cursor_rect.y -= self.slot_size[1]
            self.game.sound_manager.play_sound("Switch")
            self.last_time = current_time
        if keys[pygame.K_a] and self.cursor_rect.center[0] - self.slot_size[0] >= self.rect.left and current_time - self.last_time > 200:
            self.cursor_rect.x -= self.slot_size[0]
            self.game.sound_manager.play_sound("Switch")
            self.last_time = current_time
        if keys[pygame.K_s] and self.cursor_rect.center[1] + self.slot_size[1] <= self.rect.bottom and current_time - self.last_time > 200:
            self.cursor_rect.y += self.slot_size[1]
            self.game.sound_manager.play_sound("Switch")
            self.last_time = current_time
        if keys[pygame.K_d] and self.cursor_rect.center[0] + self.slot_size[0] <= self.rect.right and current_time - self.last_time > 200:
            self.cursor_rect.x += self.slot_size[0]
            self.game.sound_manager.play_sound("Switch")
            self.last_time = current_time
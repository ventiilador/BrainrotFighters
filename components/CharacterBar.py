import pygame
from functions import size, position_x, position_y, size_x, render_text_with_border, grayscale_image

class CharacterBar:
    def __init__(self, character, position):
        self.character = character

        self.position = position

        self.background_bar = pygame.transform.scale(pygame.image.load("assets/images/components/character_bar_background.png"), size(30, 25))
        self.background_bar_rect = self.background_bar.get_rect()
        self.background_bar_rect.center = self.position

        self.health_rect_size = size(23, 3.75)
        self.health_rect = pygame.rect.Rect(0, 0, self.health_rect_size[0], self.health_rect_size[1])
        self.health_rect.center = self.position
        self.color = (0, 255, 0)
        self.original_left_pos = self.health_rect.left

        self.basic_skill_img = self.character.basic_skill_img
        self.basic_skill_img_gray = grayscale_image(self.basic_skill_img)
        self.basic_skill_rect = self.basic_skill_img.get_rect()
        self.elemental_skill_img = self.character.elemental_skill_img
        self.elemental_skill_img_gray = grayscale_image(self.elemental_skill_img)
        self.elemental_skill_rect = self.elemental_skill_img.get_rect()
        self.ultimate_skill_img = self.character.ultimate_skill_img
        self.ultimate_skill_img_gray = grayscale_image(self.ultimate_skill_img)
        self.ultimate_skill_rect = self.ultimate_skill_img.get_rect()
        
        self.basic_skill_rect.center = (position[0] - position_x(7), position[1] + position_y(10))
        self.elemental_skill_rect.center = (position[0], position[1] + position_y(10))
        self.ultimate_skill_rect.center = (position[0] + position_x(7), position[1] + position_y(10))

        if self.position[0] <= position_x(50):
            character_image_rect_x = self.background_bar_rect.left - position_x(1)

        else:
            character_image_rect_x = self.background_bar_rect.right + position_x(1)


        self.character_image = self.character.profile_image
        self.character_image_rect = self.character_image.get_rect()
        self.character_image_rect.center = (character_image_rect_x, self.position[1])

        self.font = pygame.font.Font("assets/fonts/MonkeyLand.otf", 20)
        

    def update(self, dt):
        if self.character.health >= 75:
            self.color = (0, 255, 0)
        elif self.character.health >= 50:
            self.color = (255, 255, 0)
        elif self.character.health >= 25:
            self.color = (255, 128, 0)
        else:
            self.color = (255, 0, 0)
        last_health_rect_size = self.health_rect.size
        self.health_rect.size = (self.health_rect_size[0] * self.character.health / 100, self.health_rect_size[1])
        if self.position[0] > position_x(50) and self.health_rect.size != last_health_rect_size:
            self.health_rect.left = self.original_left_pos + (self.health_rect_size[0] - self.health_rect.size[0])
        

    def draw(self, screen):
        screen.blit(self.background_bar, self.background_bar_rect)
        pygame.draw.rect(screen, self.color, self.health_rect, border_radius=2)
        screen.blit(self.character_image, self.character_image_rect)
        self.draw_skills(screen, "basic")
        self.draw_skills(screen, "elemental")
        self.draw_skills(screen, "ultimate")
    
    def draw_skills(self, screen, skill_name):
        skill_time_rest = getattr(self.character, f"{skill_name}_skill_objective_ticks") - pygame.time.get_ticks()
        skill_img = getattr(self, f"{skill_name}_skill_img")
        skill_img_gray = getattr(self, f"{skill_name}_skill_img_gray")
        skill_rect = getattr(self, f"{skill_name}_skill_rect")

        if skill_time_rest >= 0:
            screen.blit(skill_img_gray, skill_rect)
            cooldown_text = render_text_with_border("{:.2f}".format(skill_time_rest / 1000),
                                                    self.font, (255, 180, 0), (0, 0, 0))
            text_rect = cooldown_text.get_rect(center=skill_rect.center)
            screen.blit(cooldown_text, text_rect)
        else:
            screen.blit(skill_img, skill_rect)

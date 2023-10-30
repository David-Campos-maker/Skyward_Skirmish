import pygame
from settings import screen_width , screen_height

class Background:
    def __init__(self, image_path, x, y):
        
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        self.image = pygame.transform.scale(self.image , (screen_width , screen_height))
        surface.blit(self.image, self.rect.topleft)
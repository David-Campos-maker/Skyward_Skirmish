import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self , size , x , y):
        super().__init__(size , x , y , path = '../graphics/enemy/run')
        
        self.speed = randint(3 , 4)
        self.rect.y -= 30

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image , True , False)
            
    def reverse(self):
        self.speed *= -1
        
    def update(self , shift):
        self.rect.x += shift
        self.animate()

        new_image = pygame.Surface((80, 80), pygame.SRCALPHA) 

        scaled_image = pygame.transform.scale(self.image, (self.image.get_width() + 21, self.image.get_height() + 21))

        new_image.blit(scaled_image, ((80 - scaled_image.get_width()) // 2, (80 - scaled_image.get_height()) // 2))

        self.image = new_image
        self.move()
        self.reverse_image()
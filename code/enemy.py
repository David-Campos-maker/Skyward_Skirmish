import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self , size , x , y):
        super().__init__(size , x , y , path = '../graphics/enemy/run')
        
        self.speed = randint(3 , 4)
        self.rect.y -= 38

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
        self.image = pygame.transform.scale(self.image, (round(self.image.get_width() * 1.5), round(self.image.get_height() * 1.5)))
        self.move()
        self.reverse_image()
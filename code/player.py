import pygame
import os
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self , pos):
        super().__init__()
        
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['walk'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # Player Movement
        self.direction = pygame.math.Vector2(0 , 0)
        self.speed = 6
        self.gravity = 0.6
        self.jump_speed = -12
        
    def import_character_assets(self):
        character_path = os.path.join('..', 'graphics', 'character')
        self.animations = {
            # "idle": [] ,
            "walk": [] ,
            "jump": [] 
            # "attack": [] ,
            # "shield_up": [] ,
            # "shield_idle": [] ,
            # "drinking": [] ,
            # "fall": [] ,
            # "hurt": [] ,
            # "dying" : [] , 
            # "win": []
        }
        
        for animation in self.animations.keys():
            full_path = os.path.join(character_path, animation)
            self.animations[animation] = import_folder(full_path)
            
    def animate(self):
        animation = self.animations['walk']
        
        # Loop over frame index
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.rect.x += self.speed
        
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.rect.x -= self.speed
        
        else:
            self.direction.x = 0
            
        if keys[pygame.K_SPACE]:
            self.jump()
    
    def applay_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed
            
    def update(self):
        self.get_input()
        self.animate()
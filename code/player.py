import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self , pos):
        super().__init__()
        
        self.image = pygame.Surface((32 , 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        
        # Player Movement
        self.direction = pygame.math.Vector2(0 , 0)
        self.speed = 6
        self.gravity = 0.6
        self.jump_speed = -12
        
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
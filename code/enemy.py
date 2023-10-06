import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Defina as dimensões do inimigo
        self.width = 32
        self.height = 64

        # Crie uma imagem vermelha para o sprite do inimigo
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))  # Vermelho

        # Defina o retângulo de colisão do inimigo
        self.rect = self.image.get_rect(topleft=pos)
        
    def update(self , x_shift):
        self.rect.x += x_shift

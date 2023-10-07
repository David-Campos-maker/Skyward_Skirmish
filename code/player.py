import pygame
import os
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self , pos , surface , create_jump_particle , attack_check_function):
        super().__init__()
        
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # Dust particle
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particle = create_jump_particle
        
        # Player Movement
        self.direction = pygame.math.Vector2(0 , 0)
        self.speed = 6
        self.gravity = 0.6
        self.jump_speed = -16
        
        # Attack
        self.attack_hitbox_color = (0, 0, 255)  # Azul
        self.is_attacking = False
        self.attack_check_function = attack_check_function  # Configurar a função de verificação de ataque
        self.attack_timer = 0
        self.attack_animation_timer = 0
        self.attack_animation_duration = len(self.animations['attack']) / self.animation_speed  # Calcule a duração da animação de ataque
        self.animation_ended = True
        
        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
    def import_character_assets(self):
        character_path = os.path.join('..', 'graphics', 'character')
        self.animations = {
            "idle": [] ,
            "walk": [] ,
            "jump": [] ,
            "fall": [] ,
            "attack": [] 
            # "shield_up": [] ,
            # "shield_idle": [] ,
            # "drinking": [] ,
            # "hurt": [] ,
            # "dying" : [] , 
            # "win": []
        }
        
        for animation in self.animations.keys():
            full_path = os.path.join(character_path, animation)
            self.animations[animation] = import_folder(full_path)
            
    def import_dust_run_particles(self):
        self.dust_run_particle = import_folder('../graphics/character/dust_particles/walk')
            
    def animate(self):
        animation = self.animations[self.status]
        
        # Loop over frame index
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            
        else:
            flipped_image = pygame.transform.flip(image , True , False)
            self.image = flipped_image
            
        # Set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
            
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
            
        if self.is_attacking:
            # Aqui você pode adicionar o código para executar a animação de ataque
            # Quando a animação de ataque estiver concluída, defina self.is_attacking como False
            
            self.animation_speed = 0.19
            
            if self.attack_animation_timer <= 0:
                self.is_attacking = False
                self.animation_speed = 0.15
            
    def run_dust_animation(self):
        if self.status == 'walk' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            
            if self.dust_frame_index >= len(self.dust_run_particle):
                self.dust_frame_index = 0
                
            dust_particle = self.dust_run_particle[int(self.dust_frame_index)]
            
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6 , 10)
                self.display_surface.blit(dust_particle , pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6 , 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle , True , False)
                self.display_surface.blit(flipped_dust_particle , pos)
            
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RSHIFT] and (not self.is_attacking) and self.on_ground and self.attack_animation_timer <= 0:
            self.is_attacking = True
            self.attack_animation_timer = self.attack_animation_duration
            self.attack()  # Chama o método attack quando o jogador atacar

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
            self.rect.x += self.speed
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
            self.rect.x -= self.speed
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particle(self.rect.midbottom)
    
    def get_status(self):
        if self.direction.y < 0:
           self.status = 'jump' 
           
        elif self.direction.y > 1:
            self.status = 'fall'
            
        else:
            if self.direction.x != 0:
                self.status = 'walk'
            
            else:
                self.status = 'idle'
                
        if self.is_attacking:
            self.status = 'attack'
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed
        
    def draw_attack_hitbox(self):
        attack_width = 34
        attack_height = 64
        if self.facing_right:
            attack_rect = pygame.Rect(self.rect.right, self.rect.centery - attack_height // 2, attack_width, attack_height)
        else:
            attack_rect = pygame.Rect(self.rect.left - attack_width, self.rect.centery - attack_height // 2, attack_width, attack_height)

        pygame.draw.rect(self.display_surface, self.attack_hitbox_color, attack_rect, 2)
        
    def attack(self):
        if self.is_attacking:
            attack_width = 34
            attack_height = 64
            if self.facing_right:
                attack_hitbox = pygame.Rect(self.rect.right, self.rect.centery - attack_height // 2, attack_width, attack_height)
            else:
                attack_hitbox = pygame.Rect(self.rect.left - attack_width, self.rect.centery - attack_height // 2, attack_width, attack_height)

            # Desenhe a hitbox de ataque para fins de teste e depuração
            self.draw_attack_hitbox()

            # Chame a função de verificação de ataque do nível (Level)
            if self.attack_check_function:
                self.attack_check_function(attack_hitbox)
            
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        
       # Adicione isso para atualizar o temporizador de ataque e verificar se o ataque terminou
        if self.attack_animation_timer > 0:
            self.attack_animation_timer -= 1
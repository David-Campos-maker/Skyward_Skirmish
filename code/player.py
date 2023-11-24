import pygame
import os
from support import import_folder
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self , pos , surface , create_jump_particle , attack_check_function , change_health):
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
        
        #Attack
        self.is_attacking = False
        self.attack_cooldown = 30
        self.attack_cooldown_timer = 0
        self.attack_hitbox_color = (0, 255, 0)
        self.attack_check_function = attack_check_function
        
        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
        # Health Management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 400
        self.hurt_time = 0
        
    def import_character_assets(self):
        character_path = os.path.join('..', 'graphics', 'character')
        self.animations = {
            "idle": [] ,
            "walk": [] ,
            "jump": [] ,
            "fall": [] ,
            "attack": []
        }
        
        for animation in self.animations.keys():
            full_path = os.path.join(character_path, animation)
            self.animations[animation] = import_folder(full_path)
            
    def import_dust_run_particles(self):
        self.dust_run_particle = import_folder('../graphics/character/dust_particles/walk')
            
    def animate(self):
        animation = self.animations[self.status]
    
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animation):
            self.frame_index = 0
            self.is_attacking = False
            
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image , True , False)
            self.image = flipped_image
            
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
                  
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
            
    def draw_attack_hitbox(self):
        attack_width = 64
        attack_height = 64
        offset = 30  # Ajuste este valor para mover a hitbox de ataque para dentro do sprite do jogador

        if self.facing_right:
            attack_rect = pygame.Rect(self.rect.right - offset, self.rect.centery - attack_height // 2, attack_width, attack_height)
        else:
            attack_rect = pygame.Rect(self.rect.left - attack_width + offset, self.rect.centery - attack_height // 2, attack_width, attack_height)

        pygame.draw.rect(self.display_surface, (255, 0, 0), attack_rect)  # A cor vermelha é representada por (255, 0, 0)
        
    def attack(self):
        if self.is_attacking:
            attack_width = 64
            attack_height = 64
            offset = 30  # Ajuste este valor para mover a hitbox de ataque para dentro do sprite do jogador

            if self.facing_right:
                attack_hitbox = pygame.Rect(self.rect.right - offset, self.rect.centery - attack_height // 2, attack_width, attack_height)
            else:
                attack_hitbox = pygame.Rect(self.rect.left - attack_width + offset, self.rect.centery - attack_height // 2, attack_width, attack_height)

            self.draw_attack_hitbox()

            if self.attack_check_function:
                self.attack_check_function(attack_hitbox)
            
    def get_input(self):
        keys = pygame.key.get_pressed()

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
            
        if keys[pygame.K_RSHIFT] and self.on_ground and self.direction.x == 0:
            if not self.is_attacking and self.attack_cooldown_timer <= 0:
                self.is_attacking = True
                self.frame_index = 0
                self.attack()
                self.attack_cooldown_timer = self.attack_cooldown
    
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
            self.animation_speed = 0.25
        else:
            self.animation_speed = 0.15
            
    def update_attack_cooldown(self):
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= 1
        elif self.attack_cooldown_timer < 0:
            self.attack_cooldown_timer = 0
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed
       
    def get_damage(self):
        if not self.invincible:
            self.change_health(-5)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
           
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False
                
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        
        if value >= 0: return 255
        else: return 0
            
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.update_attack_cooldown()
        self.invincibility_timer()
        self.wave_value()
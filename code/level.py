import pygame
from support import import_csv_layout , import_cut_graphic
from settings import tile_size , screen_width , screen_height
from tiles import Tile , StaticTile , AnimatedTile , Trees
from enemy import Enemy
from player import Player
from particle import ParticleEffect
from background import Background
from game_data import levels

class Level:
    def __init__(self , current_level , surface , create_overworld , change_health):
        
        # General Setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        
        # Overworld Connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']
        
        # Player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout , change_health)
        
        # Dust Particles
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
        # Explosion Particles
        self.explosion_sprites = pygame.sprite.Group()
        
        #Terrain Setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout , 'terrain')
        
        # Grass Setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout , 'grass')
        
        # Flowers
        flowers_layout = import_csv_layout(level_data['flowers'])
        self.flowers_sprites = self.create_tile_group(flowers_layout , 'flowers')
        
        # Butterflies
        butterflies_layout = import_csv_layout(level_data['butterflies'])
        self.butterfly_sprites =  self.create_tile_group(butterflies_layout , 'butterflies')
        
        # Backgroud Trees
        bg_trees_layout = import_csv_layout(level_data['bg_trees'])
        self.bg_trees_sprites = self.create_tile_group(bg_trees_layout , 'bg_trees')
        
        # Enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout , 'enemies')
        
        # Constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout , 'constraints')
        
        # Background
        self.background = Background('../graphics/decorations/background/Background.png' , 0 , 0)
        
    def create_tile_group(self , layout , type):
        sprite_group = pygame.sprite.Group()
        
        for row_index , row in enumerate(layout):
            for col_index , val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('../graphics/terrain/terrain.png')
                        tile_surface = terrain_tile_list[int(val)]
                        
                        sprite = StaticTile(tile_size , x , y , tile_surface)
                        
                    if type == 'grass':
                        grass_tile_list = import_cut_graphic('../graphics/decorations/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size , x , y , tile_surface)
                        
                    if type == 'flowers':
                        flowers_tile_list = import_cut_graphic('../graphics/decorations/flowers/flowers.png')
                        tile_surface = flowers_tile_list[int(val)]
                        sprite = StaticTile(tile_size , x , y , tile_surface)
                        
                    if type == 'butterflies':
                        if val == '0': sprite = AnimatedTile(tile_size , x , y , '../graphics/decorations/butterflies/pink')
                        if val == '1': sprite = AnimatedTile(tile_size , x , y , '../graphics/decorations/butterflies/blue')
                        
                    if type == 'bg_trees':
                        if val == '0': sprite = Trees(x , y , '../graphics/terrain/bg_trees_1/1.png' , 128)
                        if val == '1': sprite = Trees(x , y , '../graphics/terrain/bg_trees_2/bg_tree_2.png' , 128)
                        if val == '2': sprite = Trees(x , y , '../graphics/terrain/bg_trees_3/bg_tree_3.png' , 174)
                        
                    if type == 'enemies':
                        sprite = Enemy(tile_size , x , y)
                    
                    if type == 'constraints':
                        sprite = Tile(tile_size , x , y)
                    
                    sprite_group.add(sprite)
        
        return sprite_group
    
    def create_jump_particle(self , pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(8 , 6)
        else:
            pos += pygame.math.Vector2(8 , -6)
        
        jump_particle_sprite = ParticleEffect(pos , 'jump')
        self.dust_sprite.add(jump_particle_sprite)
    
    def attack_check_function(self, attack_hitbox):
        for enemy in self.enemy_sprites:
            if attack_hitbox.colliderect(enemy):
                explosion_sprites = ParticleEffect(enemy.rect.center , 'explosion')
                self.explosion_sprites.add(explosion_sprites)
                
                enemy.kill()
    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        
        new_rect = player.rect.copy()
        new_rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if new_rect.colliderect(sprite.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.on_left = True
                    self.current_x = player.rect.left
                    
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
                    
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
            
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
            
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        new_rect = player.rect.copy()
        new_rect.y += player.direction.y

        for sprite in self.terrain_sprites.sprites():
            if new_rect.colliderect(sprite.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
            
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False
    
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
        
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10 , 15)
            else:
                offset = pygame.math.Vector2(-10 , 15)
                
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle) 
    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx   
        direction_x = player.direction.x    
        
        if player_x < screen_width / 2 and direction_x < 0:
            self.world_shift = 6
            player.speed = 0 
            
        elif player_x > screen_width - (screen_width / 2) and direction_x > 0:
            self.world_shift = -6
            player.speed = 0  
            
        else:
            self.world_shift = 0
            player.speed = 6 
    
    def player_setup(self , layout , change_health):
        for row_index , row in enumerate(layout):
            for col_index , val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if val == '0':
                    sprite = Player((x , y) , self.display_surface , self.create_jump_particle , self.attack_check_function , change_health)
                    self.player.add(sprite)
                
                if val == '1':
                    idle_surface = pygame.image.load('../graphics/character/Icon.png')
                    sprite = StaticTile(tile_size , x , y , idle_surface)
                    self.goal.add(sprite)
    
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy , self.constraint_sprites , False):
                enemy.reverse()
        
    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level , 0)
            
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite , self.goal , False):
            self.create_overworld(self.current_level , self.new_max_level)
        
    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite , self.enemy_sprites , False)
        
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_left = enemy.rect.left
                enemy_right = enemy.rect.right

                player_left = self.player.sprite.rect.left
                player_right = self.player.sprite.rect.right

                if player_right > enemy_left or player_left < enemy_right:
                    self.player.sprite.get_damage()
        
    def run(self):
        # Run the entire game / level
        #Level Background
        self.background.draw(self.display_surface)
        
        # Backgroud Trees
        self.bg_trees_sprites.update(self.world_shift)
        self.bg_trees_sprites.draw(self.display_surface)
        
        # Terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        # Grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        
        # Flowers
        self.flowers_sprites.update(self.world_shift)
        self.flowers_sprites.draw(self.display_surface)
        
        # Butterflies
        self.butterfly_sprites.update(self.world_shift)
        self.butterfly_sprites.draw(self.display_surface)
        
        # Enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.check_enemy_collisions()
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)
        
        # Dust Particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)
        
        # Player
        self.player.update()
        self.horizontal_movement_collision()
        
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        
        self.check_death()
        self.check_win()
import pygame
from support import import_csv_layout , import_cut_graphic
from settings import tile_size
from tiles import Tile , StaticTile , AnimatedTile , Trees

class Level:
    def __init__(self , level_data , surface):
        
        # General Setup
        self.display_surface = surface
        self.world_shift = 0
        
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
                    
                    sprite_group.add(sprite)
        
        return sprite_group
        
    def run(self):
        # Run the entire game / level
        
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
        












# import pygame
# from settings import tile_size , screen_width
# from tiles import Tile
# from player import Player
# from enemy import Enemy
# from particle import ParticleEffect

# class Level:
#     def __init__(self , level_data , surface):
#         # Level setup
#         self.display_surface = surface
#         self.setup_level(level_data)
#         self.world_shift = 0
#         self.current_x = 0
        
#         # Dust
#         self.dust_sprite = pygame.sprite.GroupSingle()
#         self.player_on_ground = False
     
#     def create_jump_particle(self , pos):
#         if self.player.sprite.facing_right:
#             pos -= pygame.math.Vector2(8 , 6)
#         else:
#             pos += pygame.math.Vector2(8 , -6)
        
#         jump_particle_sprite = ParticleEffect(pos , 'jump')
#         self.dust_sprite.add(jump_particle_sprite)
     
#     def get_player_on_ground(self):
#         if self.player.sprite.on_ground:
#             self.player_on_ground = True
#         else:
#             self.player_on_ground = False
            
#     def create_landing_dust(self):
#         if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            
#             if self.player.sprite.facing_right:
#                 offset = pygame.math.Vector2(10 , 15)
#             else:
#                 offset = pygame.math.Vector2(-10 , 15)
                
#             fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
#             self.dust_sprite.add(fall_dust_particle) 
     
#     def setup_level(self , layout): 
#         self.tiles = pygame.sprite.Group()
#         self.player = pygame.sprite.GroupSingle()
#         self.enemies = pygame.sprite.Group()
        
#         for row_index , row in enumerate(layout):
#             for col_index , cell in enumerate(row):
#                 x = col_index * tile_size
#                 y = row_index * tile_size
                
#                 if cell == 'X':
#                     tile = Tile((x , y) , tile_size)
#                     self.tiles.add(tile)
                    
#                 if cell == 'P':
#                     player_sprite = Player((x , y) , self.display_surface , self.create_jump_particle , self.attack_check_function)
#                     self.player.add(player_sprite)      
                    
#                 if cell == 'E':
#                     enemy_sprite = Enemy((x , y))
#                     self.enemies.add(enemy_sprite)
       
#     def scroll_x(self):
#         player = self.player.sprite
#         player_x = player.rect.centerx   
#         direction_x = player.direction.x    
        
#         if player_x < screen_width / 4 and direction_x < 0:
#             self.world_shift = 6
#             player.speed = 0 
            
#         elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
#             self.world_shift = -6
#             player.speed = 0  
            
#         else:
#             self.world_shift = 0
#             player.speed = 6            
        
#     def horizontal_movement_collision(self):
#         player = self.player.sprite
        
#         new_rect = player.rect.copy()
#         new_rect.x += player.direction.x * player.speed

#         for sprite in self.tiles.sprites():
#             if new_rect.colliderect(sprite.rect):
#                 if player.direction.x < 0:
#                     player.rect.left = sprite.rect.right
#                     self.on_left = True
#                     self.current_x = player.rect.left
                    
#                 elif player.direction.x > 0:
#                     player.rect.right = sprite.rect.left
#                     player.on_right = True
#                     self.current_x = player.rect.right
                    
#         if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
#             player.on_left = False
            
#         if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
#             player.on_right = False
                
#     def vertical_movement_collision(self):
#         player = self.player.sprite
#         player.apply_gravity()
        
#         new_rect = player.rect.copy()
#         new_rect.y += player.direction.y

#         for sprite in self.tiles.sprites():
#             if new_rect.colliderect(sprite.rect):
#                 if player.direction.y > 0:
#                     player.rect.bottom = sprite.rect.top
#                     player.direction.y = 0
#                     player.on_ground = True
                    
#                 elif player.direction.y < 0:
#                     player.rect.top = sprite.rect.bottom
#                     player.direction.y = 0
#                     player.on_ceiling = True
                    
#         if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
#             player.on_ground = False
            
#         if player.on_ceiling and player.direction.y > 0.1:
#             player.on_ceiling = False
                   
#     def attack_check_function(self, attack_hitbox):
#         for enemy in self.enemies:
#             if attack_hitbox.colliderect(enemy):
#                 print('Hit')
                   
#     def run(self):
#         # Dust particle
#         self.dust_sprite.update(self.world_shift)
#         self.dust_sprite.draw(self.display_surface)
        
#         # Level Tiles
#         self.tiles.update(self.world_shift)
#         self.tiles.draw(self.display_surface)
#         self.scroll_x()
        
#         # Player
#         self.player.update()
#         self.horizontal_movement_collision()
#         self.get_player_on_ground()
#         self.vertical_movement_collision()
#         self.create_landing_dust()
#         self.player.draw(self.display_surface)
        
#         # Enemy
#         self.enemies.update(self.world_shift)
#         self.enemies.draw(self.display_surface)
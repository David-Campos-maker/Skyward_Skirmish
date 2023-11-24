import pygame , sys
from settings import *
from overworld import Overworld
from level import Level
from ui import UI

class Game:
    def __init__(self):
        
        # Game Attributes
        self.max_level = 5
        self.max_health = 100
        self.cur_health = 100
        
        # Overworld Creation
        self.overworld = Overworld(0 , self.max_level , screen , self.create_level)
        self.status = 'overworld'
        
        # User Interface
        self.ui = UI(screen)
        
    def create_level(self , current_level):
        self.level = Level(current_level , screen , self.create_overworld , self.change_health)
        self.status = 'level'
        
    def create_overworld(self , current_level , new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
            
        self.overworld = Overworld(current_level , self.max_level , screen , self.create_level)
        self.status = 'overworld'
       
    def change_health(self , amount):
        self.cur_health += amount
      
    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.max_level = 0
            self.overworld = Overworld(0 , self.max_level , screen , self.create_level)
            self.status = 'overworld'
        
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health , self.max_health)
            self.check_game_over()

# Pygame setup
pygame.init()

screen = pygame.display.set_mode((screen_width , screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill('gray')
    game.run()
    
    pygame.display.update()
    clock.tick(60)
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 15:45:02 2021

@author: Jerry
"""


import sys, pygame
import numpy as np
from collections import OrderedDict 
import random
import time
from numpy.random import choice
#%%
class Color:
    BLUE = (0,0,255)
    RED = (255,0,0) 
    WHITE = (255,255,255)
    BLACK = (0,0,0) 
    YELLOW = (255,255,0) 
    SLATE_GREY = (112,128,144)
    TRANSPARENT = (0, 0, 0, 0)
    TRACE_0 =  (204,255,255) #light blue
    
class Nest:
    rect = None
    @staticmethod 
    def set_image(image,size):
        Nest.size = size
        Nest.image = pygame.transform.scale(image,size)
        
    @staticmethod
    def set_position(position):
        Nest.position = position
        Nest.rect = Nest.image.get_rect(topleft=position)
        
         
class Food():
    
    all_food = []
    @staticmethod
    def add_food(food):
        Food.all_food.append(food)
        
    @staticmethod
    def remove_all_food():
        Food.all_food.clear()
    
    @staticmethod 
    def set_image(image,size):
        Food.size = size
        Food.image = pygame.transform.scale(image,size)
        
    @staticmethod    
    def collided_with_Food(pos):  
        for food in Food.all_food:
            if(food.rect.collidepoint(pos)):
                return True
        else:
            return False
                    
    def __init__(self,position):
        self.position = position
        self.rect = self.image.get_rect(topleft=position)
        Food.add_food(self)
     
    
class Ant():
    all_ant = []
    max_steps = 50
    all_directions = []
    #0.1機率往-45度走 0.8機率直走 0.1往45度走
    proba_direction = [0.1,.8, 0.1]
    @staticmethod
    def add_ant(ant):
        Ant.all_ant.append(ant)
        
    @staticmethod    
    def remove_all_ant():
        Ant.all_ant.clear()
        
    @staticmethod
    def rev_dir(direction):
        index = Ant.all_directions.index(direction)
        return Ant.all_directions[(index+4)%8]
        
    @staticmethod 
    def set_image(up,down,left,right,
                  upper_left,upper_right,lower_left,lower_right):
        
        Ant.images = {"up":up,"upper_right":upper_right,"right":right,"lower_right":lower_right,
                      "down":down,"upper_left":upper_left,"left":left,"lower_left":lower_left}
        Ant.all_directions = list(Ant.images.keys())
    
    @staticmethod
    def set_size(size):
        Ant.size = size
        for d,img in Ant.images.items():
            Ant.images[d] = pygame.transform.scale(img,size)
    
    def __init__(self,position,direction):
        self.position = position
        self.direction = direction
        self.image = self.images[direction]
        self.rect = self.image.get_rect(topleft=position)
        self.step = 0
        self.role = "seeker"
        self.path = [""]*Ant.max_steps
        Ant.add_ant(self)
        self._id = len(Ant.all_ant)
        
    def get_new_pos(self):
        if(self.role == "seeker"):
            ant.change_direction()
            self._seeker_get_new_pos()
        else:
            pass
            self.path[self.step]
        
        self.image = self.images[self.direction]
        
    def _seeker_get_new_pos(self):
        if(self.direction == "up"):
            new_left = self.position[0]
            new_top = self.position[1] -Ant.size[1]
        
        elif(self.direction == "upper_right"):
            new_left = self.position[0]+ Ant.size[0]
            new_top = self.position[1] -Ant.size[1] 
           
        elif(self.direction == "right"):
            new_left = self.position[0]+ Ant.size[0]
            new_top = self.position[1]
        
        elif(self.direction == "lower_right"):
            new_left = self.position[0]+Ant.size[0]
            new_top = self.position[1] +Ant.size[1]
            
        elif(self.direction == "down"):
            new_left = self.position[0]
            new_top = self.position[1] + Ant.size[1]
    
        elif(self.direction == "lower_left"):
            new_left = self.position[0] - Ant.size[0]
            new_top = self.position[1] + Ant.size[1]   
            
        elif(self.direction == "left"):
            new_left = self.position[0] - Ant.size[0]
            new_top = self.position[1] 
            
        elif(self.direction == "upper_left"):
            new_left = self.position[0]-Ant.size[0]
            new_top = self.position[1] -Ant.size[1]
        
        return new_left,new_top
    
    def decide_new_direction(self,peripheral_probability):
        #if collided with border/nest change direction
        #+- 45c
        index = Ant.all_directions.index(self.direction)
        last  = Ant.all_directions[index-1]
        next_ = Ant.all_directions[index+1] if index==len(Ant.all_directions)-1 else Ant.all_directions[0]
        self.direction = choice(a=[last,self.direction,next_],p=[0.1,0.8,0.1])
            
            
    def move(self,peripheral_probability): 
        #self.decide_new_direction()
        self.position = pos
        self.rect = self.image.get_rect(topleft=self.position)
        if(self.role == "seeker"):
            self.path[self.step] = (self.position,self.direction)
            self.step += 1
            if(self.step == Ant.max_steps):
                self.role = "return"
                self.step = -1
        
class Map:
    screen = None
    right = 0
    bottom = 0
    peripheral_probability = [0]*8
    
    @staticmethod
    def set_screen(screen):
        Map.screen = screen
        
    @staticmethod    
    def draw_image(image,rect):
        Map.screen.blit(image, rect)   
        
    @staticmethod
    def draw_line(color,size,pos):
        pygame.draw.line(Map.screen,color,size,pos)
        pygame.display.flip()
        
    @staticmethod
    def draw_rect(color,rect):
         pygame.draw.rect(Map.screen,color,rect)
    
    @staticmethod
    def set_border(right,bottom):
        Map.right = right
        Map.bottom = bottom
        
    @staticmethod
    def is_outside_border(point):
        if(point[0]<0 or point[0]> Map.right or
           point[1]<0 or point[1]> Map.bottom):
            return True
        else:
            return False
        
    @staticmethod    
    def get_peripheral_probability(pos):
         #螞蟻朝外圍八格的行走機率
         #若有障礙物則0
        index = 0
        for i in range(3):
            top = (pos[0]-Ant.height)*Ant.height*i
            for j in range(3):
                if(i==j==1):continue
                left = (pos[0]-Ant.width)*Ant.width*i
                p = (left,top)
                if(Map._is_allowed_to_pass(p)):
                    Map.peripheral_probability[index] = 1
                else:
                    Map.peripheral_probability[index] = 0
                 
                index += 1
                
    @staticmethod            
    def  _is_allowed_to_pass(pos):
         if(Food.collided_with_Food(pos) or 
            Nest.rect.collidepoint(pos) or
            Map.is_outside_border(pos)):
             return False
         return True
      
        
class Button():
    def __init__(self,position,size,image,callback):
        self.position = position
        self.size = size
        self.image = image
        self.image = pygame.transform.scale(image,size)
        self.rect = self.image.get_rect(topleft=position)
        self.callback = callback
        
    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
#%%
#variable
FOOD_WIDTH = 50
FOOD_HEIGHT = 50

NEST_WIDTH = 50
NEST_HEIGHT = 50

ANT_WIDTH = 10
ANT_HEIGHT = 10
ANTS_COUNT = 5

SCREEN = None
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

MAP_WIDTH = 800
MAP_HEIGHT = 600
Map.set_border(MAP_WIDTH,MAP_HEIGHT)
IS_START = False
current_time = 0
DEFAULT_BG_COLOR = Color.WHITE
screen = None
Map.screen = screen
maps = []

for w in range(int(MAP_WIDTH/FOOD_WIDTH)):
    for h in range(int(MAP_HEIGHT/FOOD_HEIGHT)):
        maps.append((w*FOOD_WIDTH,h*FOOD_HEIGHT))
#%%
#resources
random_map_img = pygame.image.load('image/random_map.png')
start_img = pygame.image.load("image/start.png")
nest_img = pygame.image.load("image/nest.png")
food_img = pygame.image.load("image/fruit.png")

load_img = lambda path:pygame.image.load("image/ant2/"+path)

Ant.set_image(load_img("up.png"),load_img("down.png"),load_img("left.png"),load_img("right.png"),
              load_img("upper_left.png"),load_img("upper_right.png"),load_img("lower_left.png"),load_img("lower_right.png"))
Ant.set_size((ANT_WIDTH,ANT_HEIGHT))

Nest.set_image(nest_img,(NEST_WIDTH,NEST_HEIGHT))

Food.set_image(food_img,(FOOD_WIDTH,FOOD_HEIGHT))
#%%  
        
def random_generate_map():
    clear_map()
    
    possible_positions = random.sample(maps,6)
    
    #nest
    Nest.set_position(possible_positions.pop())
    Map.draw_image(Nest.image,Nest.rect)
    
     #food
    for pos in possible_positions:
        food = Food(pos)
        Map.draw_image(Food.image,food.rect)
    
    #ant
    left = Nest.position[0]-ANT_HEIGHT
    top = Nest.position[1]-ANT_WIDTH
    right = Nest.position[0]+NEST_WIDTH
    bottom = Nest.position[1]+NEST_HEIGHT
    
    possible_positions = [(w,top) for w in range(left,right,ANT_WIDTH)]
    possible_positions.extend([(w,bottom) for w in range(left,right,ANT_WIDTH)])
    possible_positions.extend([(left,h) for h in range(top,bottom,ANT_HEIGHT)])
    possible_positions.extend([(right,h) for h in range(top,bottom,ANT_HEIGHT)])
    
    possible_positions =  [
        pos for pos 
        in set(possible_positions)
        if (Map.is_outside_border(pos)+Map.is_outside_border((pos[0],pos[1]+Ant.size[1]))==0)
    ]
    
    sample_count = min(len(possible_positions),ANTS_COUNT)
    ants_positions = random.sample(possible_positions,sample_count)
   
    for pos in ants_positions:  
        ant = Ant(pos,"up")
        Map.draw_image(ant.image,ant.rect)
        
def clear_map():
    #remove nest
    if Nest.rect:
        Map.draw_rect(DEFAULT_BG_COLOR,Nest.rect)
        
    #remove food
    for food in Food.all_food:
        Map.draw_rect(DEFAULT_BG_COLOR,food.rect)
    Food.remove_all_food()
    
    #remove ant
    for ant in Ant.all_ant:
        Map.draw_rect(DEFAULT_BG_COLOR,ant.rect)
    Ant.remove_all_ant()
    
def start():
    global IS_START,current_time
    IS_START = True
    current_time = time.time()
   
def is_collide_point(pos):
    if(pos[1]<=0 or pos[1]>=MAP_HEIGHT or pos[0]<=0 or pos[0]>=MAP_WIDTH):
        return True
    else:
        return False
 
def main():  
    global SCREEN,IS_START,current_time 
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(DEFAULT_BG_COLOR)
    Map.set_screen(screen)
    
    random_generate_map()
    
    #draw line
    Map.draw_line(Color.SLATE_GREY, (0,MAP_HEIGHT), (SCREEN_WIDTH, MAP_HEIGHT))
    
    #button
    ##ramdom map
    random_map = Button((0,MAP_HEIGHT),(80,50),random_map_img,random_generate_map)
    Map.draw_image(random_map.image,random_map.rect)
    
    ## start
    start_btn = Button((random_map.position[0]+random_map.size[0],MAP_HEIGHT),
                              (80,50),start_img,start)
    Map.draw_image(start_btn.image,start_btn.rect)
    
    # Run until the user asks to quit
    running = True
    
    while running:
        end  = time.time()
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
              #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                random_map.on_click(event)
                start_btn.on_click(event) 
       
        if (IS_START and (end-current_time>0.5)):
            for ant in Ant.all_ant:
                Map.draw_rect(DEFAULT_BG_COLOR,ant.rect)
                Map.draw_rect(Color.TRACE_0,ant.rect)
                ant.move(Map.get_peripheral_probability(ant.position))
                Map.draw_image(ant.image,ant.rect)
                
            current_time = end
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()
    
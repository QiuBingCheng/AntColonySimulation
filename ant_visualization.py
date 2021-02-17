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
from debug import print_log
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
    
    @classmethod 
    def set_image(cls,image,size):
        cls.size = size
        cls.image = pygame.transform.scale(image,size)
        
    @classmethod
    def set_position(cls,position):
        cls.position = position
        cls.rect = cls.image.get_rect(topleft=position)
        
         
class Food():
    
    all_food = []
    
    @classmethod
    def add_food(cls,food):
        cls.all_food.append(food)
        
    @classmethod
    def remove_all_food(cls):
        cls.all_food.clear()
    
    @classmethod
    def set_image(cls,image,size):
        cls.size = size
        cls.image = pygame.transform.scale(image,size)
        
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
     
    
class Ant():
    all_ant = []
    max_steps = 50
    all_directions = ["upper_left","up","upper_right","right",
                      "lower_right","down","lower_left","left"]
    
    probability_of_direction = {}
    
    #0.05機率往-45度走 0.8機率直走 0.05往45度走
    @classmethod
    def construct_proba_of_direction(cls):
        cls.probability_of_direction["up"] = [0.05,0.8,0.05,0,0,0,0.05]
        
        length = len(Ant.all_directions)
        for i in range(1,length):
            proba = [0]*length
            for j in range(0,i):
                proba[j] = cls.probability_of_direction["up"][length-i+j]
                
            for k in range(i,length):
                proba[k] = cls.probability_of_direction["up"][k-i]
                
            cls.probability_of_direction[Ant.all_directions[i]] = proba
                     
    @classmethod
    def add_ant(cls,ant):
        cls.all_ant.append(ant)
        ant._id = len(cls.all_ant)
        
    @classmethod  
    def remove_all_ant(cls):
        cls.all_ant.clear()
        
    @classmethod
    def rev_dir(direction):
        index = Ant.all_directions.index(direction)
        return Ant.all_directions[(index+4)%8]
        
    @classmethod
    def set_image(cls,up,down,left,right,
                  upper_left,upper_right,lower_left,lower_right):
        
        Ant.images = {"up":up,"upper_right":upper_right,"right":right,"lower_right":lower_right,
                      "down":down,"upper_left":upper_left,"left":left,"lower_left":lower_left}
        
        for d,img in Ant.images.items():
            cls.images[d] = pygame.transform.scale(img,(cls.width,cls.height))     
    
    @staticmethod
    @print_log()
    def _choice(a,p):
        rand = random.random()*sum(p)
        acc = 0
        for i,ele in enumerate(p):
            acc += ele
            if(acc>=rand):
                return a[i]
            
    def __init__(self,position,direction):
        self.position = position
        self.direction = direction
        self.image = self.images[direction]
        self.rect = self.image.get_rect(topleft=position)
        self.step = 0
        self.role = "seeker"
        self.path = [""]*Ant.max_steps
        self.current_proba_directions = Ant.probability_of_direction[direction]

            
    @print_log()     
    def _decide_new_direction(self,peripheral_probability):
       
        #if collided with border/nest change direction
        #+- 45c
        for i in range(len(Ant.all_directions)):
            self.current_proba_directions[i] = Ant.probability_of_direction[self.direction][i]*peripheral_probability[i]
    
        return Ant._choice(a=Ant.all_directions,p=self.current_proba_directions)
      
        
    @print_log()    
    def _decide_new_position(self, peripheral_positions):
         index = Ant.all_directions.index(self.direction)
         return peripheral_positions[index] 
     
    @print_log()
    def move(self,peripheral_positions,peripheral_probability): 
        #print(peripheral_positions)
       # print(peripheral_probability)
        self.direction = self._decide_new_direction(peripheral_probability)
        self.position = self._decide_new_position(peripheral_positions)
        self.image = self.images[self.direction]
      
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
    peripheral_positions = [0]*8
    
    @classmethod
    def set_screen(cls,screen):
        cls.screen = screen
        
    @classmethod    
    def draw_image(cls,image,rect):
        cls.screen.blit(image, rect)   
        
    @staticmethod
    def draw_line(color,size,pos):
        pygame.draw.line(Map.screen,color,size,pos)
        pygame.display.flip()
        
    @staticmethod
    def draw_rect(color,rect):
         pygame.draw.rect(Map.screen,color,rect)

    @staticmethod
    def is_outside_border(point):
        if(point[0]<0 or point[0]> Map.width or
           point[1]<0 or point[1]> Map.height):
            return True
        else:
            return False
    
        
    @classmethod
    @print_log()    
    def calculate_peripheral_probability(cls,pos):
         #螞蟻朝外圍八格的行走機率
         #若有障礙物則0
        index = 0
        for i in range(3):
            top = (pos[1]-Ant.height)+Ant.height*i
            for j in range(3):
                if(i==j==1):continue
                left = (pos[0]-Ant.width)+Ant.width*j
                p = (left,top)
                cls.peripheral_positions[index] = p
                if(Map._is_allowed_to_pass(p)):
                    cls.peripheral_probability[index] = 1
                else:
                    cls.peripheral_probability[index] = 0
                
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
DEBUG = True

#variable
Food.width = 50
Food.height = 50

Nest.width = 50
Nest.height = 50

Ant.width  = 10
Ant.height = 10
Ant.count = 2

Map.width = 800
Map.height = 600

SCREEN_WIDTH = Map.width
SCREEN_HEIGHT = Map.height+100

IS_START = False
current_time = 0
DEFAULT_BG_COLOR = Color.WHITE
screen = None
Map.screen = screen
maps = []

for w in range(int(Map.width/Food.width)):
    for h in range(int(Map.height/Food.height)):
        maps.append((w*Food.width,h*Food.height))
#%%
#resources
random_map_img = pygame.image.load('image/random_map.png')
start_img = pygame.image.load("image/start.png")
nest_img = pygame.image.load("image/nest.png")
food_img = pygame.image.load("image/fruit.png")

load_img = lambda path:pygame.image.load("image/ant2/"+path)

Ant.set_image(load_img("up.png"),load_img("down.png"),load_img("left.png"),load_img("right.png"),
              load_img("upper_left.png"),load_img("upper_right.png"),load_img("lower_left.png"),load_img("lower_right.png"))
Ant.construct_proba_of_direction()

Nest.set_image(nest_img,(Nest.width,Nest.height))

Food.set_image(food_img,(Food.width,Food.height))
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
        Food.add_food(food)
        Map.draw_image(Food.image,food.rect)
    
    #ant
    left = Nest.position[0]-Ant.height
    top = Nest.position[1]-Ant.width
    right = Nest.position[0]+Nest.width
    bottom = Nest.position[1]+Nest.height
    
    possible_positions = [(w,top) for w in range(left,right,Ant.width)]
    possible_positions.extend([(w,bottom) for w in range(left,right,Ant.width)])
    possible_positions.extend([(left,h) for h in range(top,bottom,Ant.height)])
    possible_positions.extend([(right,h) for h in range(top,bottom,Ant.height)])
    
    possible_positions =  [
        pos for pos 
        in set(possible_positions)
        if (Map.is_outside_border(pos)+Map.is_outside_border((pos[0],pos[1]+Ant.height))==0)
    ]
    
    sample_count = min(len(possible_positions),Ant.count)
    ants_positions = random.sample(possible_positions,sample_count)
   
    for pos in ants_positions:  
        ant = Ant(pos,"up")
        Ant.add_ant(ant)
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
 
def main():  
    global SCREEN,IS_START,current_time 
    
    pygame.init()
    screen = pygame.display.set_mode((Map.width, Map.height+100))
    screen.fill(DEFAULT_BG_COLOR)
    Map.set_screen(screen)
    
    random_generate_map()
    
    #draw line
    Map.draw_line(Color.SLATE_GREY, (0,Map.height), (SCREEN_WIDTH, Map.height))
    
    #button
    ##ramdom map
    random_map = Button((0,Map.height),(80,50),random_map_img,random_generate_map)
    Map.draw_image(random_map.image,random_map.rect)
    
    ## start
    start_btn = Button((random_map.position[0]+random_map.size[0],Map.height),
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
       
        if (IS_START and (end-current_time>1)):
            for ant in Ant.all_ant:
                Map.draw_rect(DEFAULT_BG_COLOR,ant.rect)
                Map.draw_rect(Color.TRACE_0,ant.rect)
                Map.calculate_peripheral_probability(ant.position)
                ant.move(Map.peripheral_positions,Map.peripheral_probability)
                Map.draw_image(ant.image,ant.rect)
                
            current_time = end
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()
    
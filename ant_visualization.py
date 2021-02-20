# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 15:45:02 2021

@author: Jerry
"""
import sys, os,pygame
import random
from util import Button,Direction,Color,Role,Action
import time
from collections import defaultdict
from debug import print_log
#%%

class Nest:
    rect = None
    food_amount = 0
    
    @classmethod 
    def set_image(cls,image,size):
        cls.size = size
        cls.image = pygame.transform.scale(image,size)
        
    @classmethod
    def set_position(cls,position):
        cls.position = position
        cls.rect = cls.image.get_rect(topleft=position)
    
    @staticmethod
    def collided(pos,enlarged_scope):
        print("nest collided")
        print(pos,enlarged_scope)
        rect = pygame.Rect(Nest.rect.left-enlarged_scope, Nest.rect.top-enlarged_scope,
                           Nest.rect.width+2*enlarged_scope,Nest.rect.height+2*enlarged_scope)
        print(rect.left,rect.top,rect.right,rect.bottom)
        if(rect.collidepoint(pos)):
            print(True)
            return True
        return False
        
        
         
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
        cls.image = pygame.transform.scale(image,size)
        
    @staticmethod
    def collided_with_empty_food(pos):
        food = Food.collided_with_food(pos)
        if(food and food.size == 0):
            return True
        else:
            return False
       
    @staticmethod 
    def collided_with_food(pos,enlarged_scope=None):  
        for food in Food.all_food:
            rect = food.rect
            if enlarged_scope:
                rect = pygame.Rect(food.rect.left-enlarged_scope, food.rect.top-enlarged_scope,
                                   food.rect.width+2*enlarged_scope,food.rect.height+2*enlarged_scope)
                
            if(rect.collidepoint(pos)):
                return food
        else:
            return None
                    
    def __init__(self,position):
        self.position = position
        self.rect = self.image.get_rect(topleft=position)
        self.size = 150
    
    def is_empty(self):
        return self.size == 0
  

class AntColony(list):
    
    def  __init__(self):
        self.pheromones = defaultdict(int)
        
    def add_pheromones(self,ant_id,amount):
        self.pheromones[ant_id] += amount
        
    def add_ant(self,ant):
        self.append(ant)
    
    def remove_all_ant(self):
        self.clear()
    
    def evaporate_pheromones(self,evaporation_rate):
        for ant in self.pheromones:
            self.pheromones[ant] *= (1-evaporation_rate)
            if (self.pheromones[ant]<0.001):
                self.pheromones[ant] = 0
                
class Ant():
   
    max_steps = 5
    default_probability_of_direction = {}
    images = {}

    @classmethod
    def construct_proba_of_direction(cls):
        length = len(Direction)
        for item in Direction:
            proba = [0]*length
            proba[item.value] = 8
            proba[item.value-1] = 1
            proba[item.value+1 if item.value<length-1 else 0] = 1
            proba[item.value-2] = 0.01
            proba[item.value+2 if item.value<length-2 else (item.value+1)%7] = 0.01
            cls.default_probability_of_direction[item.name] = proba
        print(cls.default_probability_of_direction)
        
    @classmethod
    def set_image(cls,folder):
        filesname = os.listdir(folder)
        for file in filesname:
            direction = file.split(".")[0]
            image =  pygame.image.load(f"{folder}/{file}")
            Ant.images[direction] = pygame.transform.scale(image,(cls.width,cls.height))    
    
    @staticmethod
    @print_log()
    def _choice(p):
        rand = random.random()*sum(p)
        acc = 0
        for i,ele in enumerate(p):
            acc += ele
            if(acc>=rand):
                return i
                 
    def __init__(self,_id,start_pos,direction): 
        self._id = _id
        self.role = Role.FORAGER
        self.action = Action.FORAGE
        self.drop_amount = 2
        self.direction = direction
        self.position = start_pos
        self.peripheral_positions = [""]*len(Direction)
        
        self.path = [""]*(Ant.max_steps+1)
        self.path[0] = (start_pos,direction)
        self.current_proba_directions = Ant.default_probability_of_direction[direction]
    
    def follow_leader(self,leader):
        print("follower_leader")
        #set leader
        self.leader_id = leader._id
        self._action = Action.GO
        #print(leader._id)
        #print(leader.role)
        #print(leader._action)
        
        self.destination_step = leader.destination_step
        self.food = leader.food
        
        #change to leader route
        for i,path in enumerate(leader.path):
            print(path)
            self.path[i]  = path
            
            #set current step
            if path!="" and path[0] == self.position:
                self.current_step = i
                break
        else:
            self.current_step = 1
            
    
    def has_reached_maximum_step(self):
        print("has_reached_maximum_step")
        return self.current_step == self.max_steps+1
    
    def has_arrived_at_nest(self):
        print("has_arrived_at_nest")
        print(self.current_step)
        return self.current_step == -1
    
    def has_arrived_at_food(self):
        print("has_arrived_at_food")
        return self.current_step == self.destination_step
    
    
    @property
    def action(self):
        return self._action
    
    @action.setter
    def action(self,value):
        print("===action===")
        print(value)
        if(value == Action.FORAGE):
            self.current_step = 1
            
        elif(value == Action.RETURN):
            self.current_step -= 1
        
        elif(value == Action.TRANSPORT):
            self.destination_step = self.current_step #food
            self.current_step -= 1
            
        elif(value == Action.GO):
            self.current_step = 1
        
        self._action = value
        print(self._action)
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self,direction):
        self._direction = direction
        self.image = Ant.images[self.direction]
    
    @property
    def position(self):
        return self._position
        
    @position.setter
    def position(self,position):
        self._position = position
        self.rect = self.image.get_rect(topleft=self._position)
        
    def forager_move(self,prohibited_positions,positions_of_pheromones):
        print("forager_move")
        #1.往周圍八格費洛蒙濃度最高的方向移動 or
        #2.若沒有費洛蒙則以預設機率決定方向
        
        highest_concentration = max(positions_of_pheromones)
        if(highest_concentration>0):
            index = positions_of_pheromones.index(highest_concentration)
        else:
            # if position is prohibited , probability is 0
            for i in range(len(Direction)):
                self.current_proba_directions[i] = Ant.default_probability_of_direction[self.direction][i]*prohibited_positions[i]
            print(self.current_proba_directions)
            index = Ant._choice(p=self.current_proba_directions)
        
        self.direction = Direction(index).name
        self.position = self.peripheral_positions[index]
       
        self.path[self.current_step] = (self.position,self.direction)
        self.current_step += 1
    
    def reverse_move(self):
        print("reverse_move")
        pos,direction = self.path[self.current_step]
        #reversed direction 
        self.direction = Direction((Direction[direction].value+4)%len(Direction)).name
        self.position = pos
        self.current_step -= 1
        
    
    def move_to_food(self):
        #carrier move to find food along with same way
        print("move to food")
        #print(self.path)
        #print(self.current_step)
        pos,direction = self.path[self.current_step]
        self.direction = direction
        self.position = pos
        self.current_step += 1
        
    def perceive_peripheral_positions(self):
        #east
        left = self.position[0]+Ant.width
        top = self.position[1]
        self.peripheral_positions[Direction.EAST.value] = (left,top)
      
        #south east
        left = self.position[0]+Ant.width
        top = self.position[1]+Ant.height
        self.peripheral_positions[Direction.SOUTHEAST.value] = (left,top)
        
        #south
        left = self.position[0]
        top = self.position[1]+Ant.height
        self.peripheral_positions[Direction.SOUTH.value] = (left,top)      
        
        #south west
        left = self.position[0]-Ant.width
        top = self.position[1]+Ant.height
        self.peripheral_positions[Direction.SOUTHWEST.value] = (left,top)
            
        #west
        left = self.position[0]-Ant.width
        top = self.position[1]
        self.peripheral_positions[Direction.WEST.value] = (left,top)     
        
        #north west
        left = self.position[0]-Ant.width
        top = self.position[1]-Ant.height
        self.peripheral_positions[Direction.NORTHWEST.value] = (left,top)
            
        #NORTH
        left = self.position[0]
        top = self.position[1]-Ant.height
        self.peripheral_positions[Direction.NORTH.value] = (left,top)
        
        #NORTH east
        left = self.position[0]+Ant.width
        top = self.position[1]-Ant.height
        self.peripheral_positions[Direction.NORTHEAST.value] = (left,top)
        
        return self.peripheral_positions
    
class Map:
    #[1,0,1,..] 1表示可以通行
    prohibited_positions = [0]*len(Direction)
    #費洛蒙
    positions_of_pheromones = [0]*len(Direction)
   
    pheromones = defaultdict(dict)
        
    @staticmethod
    def is_outside_border(point):
        if(point[0]<=0 or point[0]+Ant.width>= Map.width or
           point[1]<=0 or point[1]+Ant.height>= Map.height):
            return True
        else:
            return False
        
    @classmethod
    @print_log()    
    def decide_prohibited_positions(cls,positions):
        #決定螞蟻外圍路徑是否可以通行(有無障礙物)
        for d,pos in enumerate(positions):
            cls.prohibited_positions[d] = 1 if(Map._is_allowed_to_pass(pos)) else 0
    
    @classmethod
    @print_log()    
    def decide_pheromones_of_positions(cls,positions):
        #決定螞蟻外圍路徑的費洛蒙
        for d,pos in enumerate(positions):
            pher = 0
            for leader in cls.pheromones[pos]:
                pher += cls.pheromones[pos][leader]
            
            cls.positions_of_pheromones[d] = pher
            
    @classmethod
    def add_pheromones(cls, position, leader_id, amount):
        print("add_pheromones")
        print(f"{leader_id} drop {amount} on {position}")
        
        if leader_id not in cls.pheromones[position]:
            cls.pheromones[position] = {leader_id:amount}
        else:
            cls.pheromones[position][leader_id] += amount
            
            
    
    @classmethod
    def evaporate_pheromones(cls,evaporation_rate):
        #positions is collections
        for pos in cls.pheromones:
            for leader in cls.pheromones[pos]:
                cls.pheromones[pos][leader] *= (1-evaporation_rate)
                if cls.pheromones[pos][leader]< 0.01:
                    cls.pheromones[pos][leader] = 0
      
    @staticmethod 
    def get_leader_of_food_trace(position):
        for leader in Map.pheromones[position]:
            if Map.pheromones[position][leader]>0:
                return leader
        else:
            return False
        
    
    @staticmethod           
    def  _is_allowed_to_pass(pos):
         if(Food.collided_with_empty_food(pos) or 
            Nest.collided(pos,enlarged_scope=Ant.width) or
            Map.is_outside_border(pos)):
             return False
         return True
        

#%%
DEBUG = True

#variable
Food.width = 50
Food.height = 50
Food.count = 5

Nest.width = 50
Nest.height = 50

ANT_COLONY = AntColony()

Ant.width  = 10
Ant.height = 10
Ant.count = 30
Ant.max_steps = 100

#screen
DEFAULT_BG_COLOR = Color.WHITE

Map.width = 800
Map.height = 600
SCREEN = None
SCREEN_WIDTH = Map.width
SCREEN_HEIGHT = Map.height+100

EVAPORATION_RATE = 0.01

#action
start_btn = None
IS_START = False
CURRENT_TIME = 0

maps = []
for w in range(int(Map.width/Food.width)):
    for h in range(int(Map.height/Food.height)):
        maps.append((w*Food.width,h*Food.height))
#%%
#resources
random_map_img = pygame.image.load('image/random_map.png')
start_img = pygame.image.load("image/start.png")
stop_img = pygame.image.load("image/stop.png")

nest_img = pygame.image.load("image/nest.png")
food_img = pygame.image.load("image/fruit.png")

Ant.set_image("image/ant2")
Ant.construct_proba_of_direction()

Nest.set_image(nest_img,(Nest.width,Nest.height))

Food.set_image(food_img,(Food.width,Food.height))
#%%  
        
def random_generate_map():
    if (IS_START):
        return
    
    clear_map()
    #clear pheromones
    Map.pheromones.clear()
    
    possible_positions = random.sample(maps,Food.count)
    
    #nest
    Nest.set_position(possible_positions.pop())
    SCREEN.blit(Nest.image,Nest.rect) 
    
     #food
    for pos in possible_positions:
        food = Food(pos)
        Food.add_food(food)
        SCREEN.blit(Food.image,food.rect) 
    
    #ant
    left = Nest.position[0]-2*Ant.height
    top = Nest.position[1]-2*Ant.width
    right = Nest.position[0]+Nest.width+Ant.height
    bottom = Nest.position[1]+Nest.height+Ant.height
    
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
   
    for i,pos in enumerate(ants_positions):  
        ant = Ant(i,pos,Direction.NORTH.name)
        ANT_COLONY.add_ant(ant)
        SCREEN.blit(ant.image,ant.rect) 
        
def clear_map():
    map_rect = pygame.Rect(0, 0,Map.width,Map.height)
    pygame.draw.rect(SCREEN,DEFAULT_BG_COLOR,map_rect)
    
    ANT_COLONY.remove_all_ant()
    Food.remove_all_food()
    
def start():
    global IS_START,CURRENT_TIME,start_btn
    
    #start->stop
    if(IS_START):
        IS_START = False
        start_btn.change_image(start_img)
        
    else:
        IS_START = True
        CURRENT_TIME = time.time()
        start_btn.change_image(stop_img)
     
    SCREEN.blit(start_btn.image,start_btn.rect) 
    
   
def main():  
    global SCREEN,IS_START,CURRENT_TIME ,start_btn
    
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
     
    SCREEN = pygame.display.set_mode((Map.width, Map.height+100))
    SCREEN.fill(DEFAULT_BG_COLOR)
    
    random_generate_map()
    
    #draw line
    pygame.draw.line(SCREEN,Color.SLATE_GREY, (0,Map.height), (SCREEN_WIDTH, Map.height))
    
    #button
    ##ramdom map
    random_map = Button((0,Map.height),(80,50),random_map_img,random_generate_map)
    SCREEN.blit(random_map.image,random_map.rect)   
    
    ## start
    start_btn = Button((random_map.position[0]+random_map.size[0],Map.height),
                              (80,50),start_img,start)
    SCREEN.blit(start_btn.image,start_btn.rect) 
    
    #font
    text_width, text_height = myfont.size("Collected Food: xxxxx")
    text_rect = pygame.Rect(start_btn.rect.right+5, start_btn.position[1]+2,
                               text_width, text_height)
    textsurface = myfont.render("Collected Food: 0", False, (0, 0, 0))
    SCREEN.blit(textsurface, (text_rect.left, text_rect.top))
   
    
    # Run until the user asks to quit
    running = True
    
    while running:
        end  = time.time()
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
              #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                random_map.on_click(event)
                start_btn.on_click(event) 
        
        if (IS_START and (end-CURRENT_TIME>0.5)):
            for ant in ANT_COLONY:
                print("===new iteration===")
                print(ant.role,ant.action)
                #overwrite original image
                pygame.draw.rect(SCREEN,DEFAULT_BG_COLOR,ant.rect)
                if(ant.role == Role.FORAGER):
                    if(ant.action == Action.FORAGE):                                         
        
                        #往周圍八格費洛蒙濃度最高的方向移動
                        #若沒有費洛蒙則隨機移動
                        ant.perceive_peripheral_positions()
                        Map.decide_pheromones_of_positions(ant.peripheral_positions)
                        Map.decide_prohibited_positions(ant.peripheral_positions)    
                        ant.forager_move(Map.prohibited_positions,Map.positions_of_pheromones)
                        
                        food = Food.collided_with_food(pos=ant.position,enlarged_scope=2*Ant.width)
                        leader_id  = Map.get_leader_of_food_trace(ant.position)
                        
                        if(food):
                            #Ant.leaders.append(ant._id)
                            ant.role = Role.LEADER
                            ant.action = Action.TRANSPORT
                            ant.food  = food
                            ant.food.size -= 1
                                
                        elif(leader_id):
                            #follow path
                            ant.role = Role.FOLLOWER
                            ant.follow_leader(ANT_COLONY[leader_id])
                            
                        elif(ant.has_reached_maximum_step()):
                            ant.action = Action.RETURN
                            print(f"path:\n{ant.path}")
                            
                    elif(ant.action == Action.RETURN):
                        pygame.draw.rect(SCREEN,DEFAULT_BG_COLOR,ant.rect)
                        ant.reverse_move()
                        
                        leader_id  = Map.get_leader_of_food_trace(ant.position)
                        
                        if(leader_id):
                            #follow path
                            ant.role = Role.FOLLOWER
                            ant.follow_leader(ANT_COLONY[leader_id])
                            
                        elif (ant.has_arrived_at_nest()):     
                            ant.action = Action.FORAGE
                            
                elif(ant.role == Role.LEADER):
                    if(ant.action == Action.GO):
                        Map.add_pheromones(ant.position,ant._id,ant.drop_amount)
                        ANT_COLONY.add_pheromones(ant._id,ant.drop_amount)
                        ant.move_to_food()
                        
                        if(ant.has_arrived_at_food()):
                            if(ant.food.is_empty()):
                                ant.role = Role.FORAGER
                                ant.action == Action.FORAGE
                            else:
                                ant.food.size -= 1                              
                                ant.action = Action.TRANSPORT
                    
                    elif(ant.action == Action.TRANSPORT):
                        Map.add_pheromones(ant.position,ant._id,ant.drop_amount)
                        ANT_COLONY.add_pheromones(ant._id,ant.drop_amount)
                        ant.reverse_move()
                        
                        if (ant.has_arrived_at_nest()):
                            Nest.food_amount += 1
                            ant.action = Action.GO
                            
                elif(ant.role == Role.FOLLOWER):
                        if(ant.action == Action.TRANSPORT):
                            Map.add_pheromones(ant.position,ant._id,ant.drop_amount)
                            ANT_COLONY.add_pheromones(ant.leader_id,ant.drop_amount)
                            ant.reverse_move()
                            
                            if (ant.has_arrived_at_nest()):
                                Nest.food_amount += 1
                                ant.action = Action.GO
                                
                                #evaluate different route for same food
                                better_id = ant.leader_id
                                for leader_id in ANT_COLONY.pheromones:
                                    if leader_id == ant.leader_id:continue
                                    if(ANT_COLONY.pheromones[leader_id]>ANT_COLONY.pheromones[better_id]):
                                        better_id = leader_id
                                        
                                if(ant.leader_id != better_id):
                                    #switch to better route
                                    ant.follow_leader(ANT_COLONY[better_id])
                    
                                    
                        elif(ant.action == Action.GO):
                            Map.add_pheromones(ant.position,ant._id,ant.drop_amount)
                            ANT_COLONY.add_pheromones(ant.leader_id,ant.drop_amount)
                            pygame.draw.rect(SCREEN,Color.TRACE_2,ant.rect)
                            ant.move_to_food()
                            
                            if(ant.has_arrived_at_food()):
                                if(ant.food.is_empty()):
                                    ant.role = Role.FORAGER
                                    ant.action == Action.FORAGE
                                else:
                                    ant.food.size -= 1
                                    ant.action = Action.TRANSPORT
            

            #redraw map
            for pos in Map.pheromones:
                pher = 0
                for leader in Map.pheromones[pos]:
                    pher += Map.pheromones[pos][leader]
                 
                rect = pygame.Rect(pos[0],pos[1],Ant.width,Ant.height)
                
                if pher>15:
                    pygame.draw.rect(SCREEN,Color.TRACE_5, rect)
                elif(pher>10):
                    pygame.draw.rect(SCREEN,Color.TRACE_4, rect)
                elif(pher>5):
                    pygame.draw.rect(SCREEN,Color.TRACE_3, rect)
                elif(pher>0):
                    pygame.draw.rect(SCREEN,Color.TRACE_2, rect)
                else:
                    pygame.draw.rect(SCREEN,DEFAULT_BG_COLOR, rect)
                    
            #redraw ant
            for ant in ANT_COLONY:
                SCREEN.blit(ant.image,ant.rect)
            
            #evaporate
            Map.evaporate_pheromones(EVAPORATION_RATE)
            ANT_COLONY.evaporate_pheromones(EVAPORATION_RATE)
            
            #collected food
            pygame.draw.rect(SCREEN,DEFAULT_BG_COLOR, text_rect)
            textsurface = myfont.render(f"Collected Food: {Nest.food_amount}", False, (0, 0, 0))
            SCREEN.blit(textsurface, (text_rect.left, text_rect.top))
            
            CURRENT_TIME = end
        pygame.display.update()           

if __name__ == "__main__":
    main()
    
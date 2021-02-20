# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 10:43:00 2021

@author: Jerry
"""
import pygame
from enum import Enum

class Direction(Enum):
    EAST = 0
    SOUTHEAST = 1
    SOUTH = 2
    SOUTHWEST = 3
    WEST = 4
    NORTHWEST = 5
    NORTH = 6
    NORTHEAST = 7
     
class Color:
    BLUE = (0,0,255)
    RED = (255,0,0) 
    WHITE = (255,255,255)
    BLACK = (0,0,0) 
    YELLOW = (255,255,0) 
    SLATE_GREY = (112,128,144)
    TRANSPARENT = (0, 0, 0, 0)
    TRACE_1 =  (240,248,255) #light blue
    TRACE_2 = (245,222,179) #Salmon1
    TRACE_3 = (244,164,96) #TOMATO
    TRACE_4 = (210,105,30) #TOMATO
    TRACE_5 = (178,34,34) #TOMATO
    
class Role:
    FORAGER = 0
    LEADER = 1
    FOLLOWER  = 2

class Action:
    #FORAGER
    FORAGE = 0
    RETURN = 1
    
    #LEADER, FOLLOWER
    TRANSPORT = 2
    GO = 3
    
    
    
        
class Button():
    def __init__(self,position,size,image,callback):
        self.position = position
        self.size = size
        self.image = image
        self.image = pygame.transform.scale(image,size)
        self.rect = self.image.get_rect(topleft=position)
        self.callback = callback
        
    def change_image(self,image): 
        self.image = image
        self.image = pygame.transform.scale(image,self.size)
        self.rect = self.image.get_rect(topleft=self.position)
        
    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
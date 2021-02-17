# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:09:36 2021

@author: Jerry
"""


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
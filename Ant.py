from Element import Element
import random
from enum import Enum
import pygame
# global

RelativeDirection = Enum('RelativeDirection', ["top", "top_right", "right", "down_right", "down", "down_left", "left", "top_left"])
OrdinalDirection = Enum('OrdinalDirection', ["north", "northeast", "east", "southeast","south", "southwest", "west", "northwest"])

def random_choice(candidates,weights):
    rand = random.random()
    sum_ = 0
    for can,wei in zip(candidates,weights):
        sum_ += wei
        if sum_>=rand:
            return can

# global
class Ant(Element):
    def __init__(self,image, rect, nest):
        super().__init__(image, rect)
        self.nest = nest
        # self.nest = Nest(self.nest_img, pygame.Rect(x, y, self.nest_width, self.nest_height))

        # attribute
        self.ant_width = 10
        self.ant_height = 10

        self.ant_imgs = [pygame.image.load(f"image/ant{i}.png") for i in range(1,9)]
        #self.ant_imgs = pygame.transform.scale(self.ant_img, (self.ant_width, self.ant_height))

        self.ordinal_dir =  OrdinalDirection.north
        self.relative_dir = RelativeDirection.top

        self.dir_prob = [0.6,0.15,0.05,0,0,0,0.05,0.15]

    def detect_env(self):
        # check nearby object food/nest/Pheromones/wall

        pass


    def move(self):
        print("move")

        # decide direction
        rand = random.random()
        sum_ = 0
        for direction, wei in zip(RelativeDirection, self.dir_prob):
            sum_ += wei
            if sum_ >= rand:
                self.relative_dir = direction
                break

        offset = self.relative_dir.value-1
        new_ordinal_val = (self.ordinal_dir.value + offset)
        if  new_ordinal_val>8:
            new_ordinal_val -= 8

        self.ordinal_dir = OrdinalDirection(new_ordinal_val)
        self.change_image(self.ant_imgs[new_ordinal_val-1])

        print(self.relative_dir,self.ordinal_dir)

        if self.ordinal_dir == OrdinalDirection.north:
            self.rect.top -= self.rect.height

        elif self.ordinal_dir == OrdinalDirection.northeast:
            self.rect.top -= self.rect.height
            self.rect.left += self.rect.width

        elif self.ordinal_dir == OrdinalDirection.east:
            self.rect.left += self.rect.width

        elif self.ordinal_dir == OrdinalDirection.southeast:
            self.rect.top += self.rect.height
            self.rect.left += self.rect.width

        elif self.ordinal_dir == OrdinalDirection.south:
            self.rect.top += self.rect.height

        elif self.ordinal_dir == OrdinalDirection.southwest:
            self.rect.top += self.rect.height
            self.rect.left -= self.rect.width

        elif self.ordinal_dir == OrdinalDirection.west:
            self.rect.left -= self.rect.width

        elif self.ordinal_dir == OrdinalDirection.northwest:
            self.rect.top -= self.rect.height
            self.rect.left -= self.rect.width
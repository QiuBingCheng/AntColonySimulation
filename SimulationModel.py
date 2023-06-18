import pygame
from Button import Button
from Color import Color
from Food import Food
from Nest import Nest
from Ant import Ant
import random

class SimulationModel:
    def __init__(self, rect):
        self.rect = rect
        self.panel_width = self.rect.width
        self.panel_height = self.rect.height

        # background image
        self.back_image = pygame.image.load("image/background.png")
        self.back_image = pygame.transform.scale(self.back_image, (self.panel_width, self.panel_height))

        self.food_num = 5
        self.food_width = 50
        self.food_height = 50
        self.food_capacity = 50
        self.food_img = pygame.image.load("image/fruit.png")
        self.food_img = pygame.transform.scale(self.food_img, (self.food_width, self.food_height))
        self.foods = []

        self.nest = None
        self.nest_width = 50
        self.nest_height = 50
        self.nest_img = pygame.image.load("image/nest.png")
        self.nest_img = pygame.transform.scale(self.nest_img, (self.nest_width, self.nest_height))

        self.ants = []
        self.ant_num = 10
        self.ant_width = 10
        self.ant_height = 10
        self.ant_count = 50
        self.max_steps = 100
        self.ant_img = pygame.image.load("image/ant1.png")
        self.ant_img = pygame.transform.scale(self.ant_img, (self.ant_width, self.ant_height))


    def create_nest_and_food(self):

        # create possible positions of nest and food
        max_width = self.nest_width if self.nest_width > self.food_width else self.food_width
        max_height = self.nest_height if self.nest_height > self.food_height else self.food_height
        w_count = self.panel_width // max_width
        h_count = self.panel_height // max_height

        possible_start_points = []
        for w in range(w_count):
            for h in range(h_count):
                possible_start_points.append((w * max_width, h * max_height))
        random.shuffle(possible_start_points)

        # create nest
        x, y = possible_start_points.pop()
        self.nest = Nest(self.nest_img, pygame.Rect(x, y, self.nest_width, self.nest_height))

        self.foods.clear()
        # create food
        for i in range(self.food_num):
            x, y = possible_start_points.pop()
            self.foods.append(Food(self.food_img, pygame.Rect(x, y, self.food_width, self.food_height)))

    def reset(self):
        # generate ant
        self.create_nest_and_food()
        self.create_ants()

    # ant controller
    def create_ants(self):
        x, y = self.nest.rect.right , self.nest.rect.top
        self.ants = [Ant(self.ant_img, pygame.Rect(x, y, self.ant_width, self.ant_height),self.nest)]

    def run_event(self):
        print("run_one_event called")
        for ant in self.ants:
            ant.move()

    def draw(self, surface):
        # background
        surface.blit(self.back_image, self.rect)

        # nest
        self.nest.draw(surface)
        for food in self.foods:
            food.draw(surface)

        for ant in self.ants:
            ant.draw(surface)
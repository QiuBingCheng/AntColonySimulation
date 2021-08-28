import pygame
from Button import Button
from Color import Color
from Food import Food
from Nest import Nest
import random

class SimulationModel:
    def __init__(self, panel_width, panel_height):
        self.panel_width = panel_width
        self.panel_height = panel_height

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

    def reset(self):
        # create object and location

        # nest and food
        max_width = self.nest_width if self.nest_width > self.food_width else self.food_width
        max_height = self.nest_height if self.nest_height > self.food_height else self.food_height
        w_count = self.panel_width // max_width
        h_count = self.panel_height // max_height

        possible_start_points = []
        for w in range(w_count):
            for h in range(h_count):
                possible_start_points.append((w * max_width, h * max_height))
        random.shuffle(possible_start_points)

        # nest
        x, y = possible_start_points.pop()
        self.nest = Nest(self.nest_img, pygame.Rect(x, y, self.nest_width, self.nest_height))

        self.foods.clear()
        # food
        for i in range(self.food_num):
            x, y = possible_start_points.pop()
            self.foods.append(Food(self.food_img, pygame.Rect(x, y, self.food_width, self.food_height)))

    def run_one_event(self):
        # each ant move
        pass

    def draw(self, surface):
        # nest
        self.nest.draw(surface)
        for food in self.foods:
            food.draw(surface)

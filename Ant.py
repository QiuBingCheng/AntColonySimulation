from Element import Element
import pygame

class Ant(Element):
    def __init__(self,image, rect, nest):
        super().__init__(image, rect)
        self.nest = nest
        # self.nest = Nest(self.nest_img, pygame.Rect(x, y, self.nest_width, self.nest_height))

    def move(self):
        pass


